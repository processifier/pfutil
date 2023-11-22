import pandas as pd
from logging import getLogger
from pfr.config.schema import Eventlog

from pfr.engine.helpers import get_business_durtation_h, trim_if_string, get_working_time_calculator, get_duration_h
pd.set_option('display.max_columns', None)

LOG = getLogger(__name__)


class FakeActivities:
    START = 'start'
    END = 'end'


class EventlogEtl:
    def __init__(self, input_config):
        self._config = input_config
        self._businesshrs = get_working_time_calculator(self._config['workingCalendar']['workingDays'],
                                                        self._config['workingCalendar']['workStart'],
                                                        self._config['workingCalendar']['workEnd'],
                                                        self._config['workingCalendar']['holidayCalendar'])

    def _add_fake_activities(self, eventlog) -> pd.DataFrame:
        return (eventlog.groupby([Eventlog.case_id.name], as_index=False)
                .apply(self._add_fake_start_end)
                .reset_index(drop=True))

    def _add_fake_start_end(self, sublog):
        first_row = sublog.iloc[[0]]
        last_row = sublog.iloc[-1:]
        new_first_row = first_row.copy(deep=True)
        new_first_row[Eventlog.activity.name] = FakeActivities.START
        new_first_row[Eventlog.activity_end_ts.name] = first_row[Eventlog.activity_start_ts.name]
        new_first_row[Eventlog.activity_business_duration_h.name] = 0
        new_first_row[Eventlog.activity_duration_h.name] = 0
        new_first_row[Eventlog.resource.name] = ""
        new_last_row = last_row.copy(deep=True)
        new_last_row[Eventlog.activity.name] = FakeActivities.END
        new_last_row[Eventlog.activity_start_ts.name] = last_row[Eventlog.activity_end_ts.name]
        new_last_row[Eventlog.activity_business_duration_h.name] = 0
        new_first_row[Eventlog.activity_duration_h.name] = 0
        new_last_row[Eventlog.resource.name] = ""
        result = pd.concat([pd.concat([new_first_row, sublog]), new_last_row])
        return result

    def _get_case_edge(self, sublog):
        sublog[Eventlog.activity_next.name] = sublog[Eventlog.activity.name].shift(-1)
        sublog[Eventlog.transition_start_ts.name] = sublog[Eventlog.activity_end_ts.name]
        value_for_NaT = sublog.iloc[-1].at[Eventlog.transition_start_ts.name]
        sublog[Eventlog.transition_end_ts.name] = (sublog[Eventlog.activity_start_ts.name]
                                                   .shift(-1, fill_value=value_for_NaT))
        return sublog

    def create(self, raw_eventlog):
        timestamp_mask = self._config["timestampMask"]
        eventlog = pd.DataFrame()
        eventlog[Eventlog.case_id.name] = raw_eventlog[self._config['eventlogInputColumns']['caseId']].astype(str)
        eventlog[Eventlog.resource.name] = raw_eventlog[self._config['eventlogInputColumns']['resource']]
        eventlog[Eventlog.activity.name] = raw_eventlog[self._config['eventlogInputColumns']['activity']]
        eventlog[Eventlog.activity.name] = eventlog.apply(lambda row: trim_if_string(row[Eventlog.activity.name]), axis=1)
        eventlog[Eventlog.id.name] = range(0, len(eventlog))
        eventlog[Eventlog.activity_end_ts.name] = raw_eventlog[self._config['eventlogInputColumns']['endTimestamp']]
        eventlog[Eventlog.activity_end_ts.name] = pd.to_datetime(eventlog[Eventlog.activity_end_ts.name],
                                                            errors='raise',
                                                            format=timestamp_mask,
                                                            utc=True).dt.tz_localize(None)
        if "startTimestamp" in self._config['eventlogInputColumns'].keys():
            eventlog[Eventlog.activity_start_ts.name] = pd.to_datetime(
                raw_eventlog[self._config['eventlogInputColumns']['startTimestamp']],
                errors='raise',
                format=timestamp_mask,
                utc=True).dt.tz_localize(None)
        else:
            eventlog[Eventlog.activity_start_ts.name] = eventlog[Eventlog.activity_end_ts.name]

        eventlog[Eventlog.activity_business_duration_h.name] = eventlog.apply(
            lambda row: get_business_durtation_h(row[Eventlog.activity_start_ts.name], row[Eventlog.activity_end_ts.name], self._businesshrs),
            axis=1)
        eventlog[Eventlog.activity_duration_h.name] = eventlog.apply(
            lambda row: get_duration_h(row[Eventlog.activity_start_ts.name], row[Eventlog.activity_end_ts.name]), axis=1)
        eventlog[Eventlog.activity_start_date.name] = eventlog[Eventlog.activity_start_ts.name].dt.date.astype("datetime64[ns]")
        eventlog[Eventlog.activity_end_date.name] = eventlog[Eventlog.activity_end_ts.name].dt.date.astype("datetime64[ns]")
        eventlog.sort_values(by=[Eventlog.case_id.name, Eventlog.activity_start_ts.name], inplace=True)
        eventlog = self._add_fake_activities(eventlog)
        eventlog = (eventlog
                    .groupby(Eventlog.case_id.name, group_keys=True)
                    .apply(self._get_case_edge)
                    .reset_index(drop=True))
        eventlog[Eventlog.transition_business_duration_h.name] = eventlog.apply(
            lambda row: get_business_durtation_h(row[Eventlog.transition_start_ts.name],
                                                 row[Eventlog.transition_end_ts.name], self._businesshrs), axis=1)
        eventlog[Eventlog.transition_duration_h.name] = eventlog.apply(
            lambda row: get_duration_h(row[Eventlog.transition_start_ts.name], row[Eventlog.transition_end_ts.name]), axis=1)
        eventlog[Eventlog.transition_name.name] = eventlog[Eventlog.activity.name] + ' -> ' + eventlog[
            Eventlog.activity_next.name]
        eventlog[Eventlog.id.name] = range(0,  + len(eventlog))
        return eventlog
