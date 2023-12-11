import pandas as pd
from pfr.config.schema import Eventlog, Case
from pfr.engine.helpers import get_business_durtation_h, get_working_time_calculator, get_duration_h
from pfr.engine.etl_eventlog import FakeActivities


class CasesFactory:
    def __init__(self, config):
        self._config = config
        self._businesshrs = get_working_time_calculator(self._config['workingCalendar']['workingDays'],
                                                        self._config['workingCalendar']['workStart'],
                                                        self._config['workingCalendar']['workEnd'],
                                                        self._config['workingCalendar']['holidayCalendar'])

    def create(self, eventlog, case2variant):
        df = eventlog.copy(deep=True)
        columns = [Eventlog.case_id.name, Eventlog.activity.name,
                   Eventlog.activity_start_ts.name, Eventlog.activity_end_ts.name]
        df = df[columns]
        df_first_and_last_event = self._get_first_and_last(df)
        df_case_to_variants = pd.DataFrame(list(case2variant.items()),
                                           columns=[Case.id.name, Case.variant_id.name])
        result = pd.merge(df_first_and_last_event, df_case_to_variants, how='left', on=Case.id.name)
        result[Case.duration_h.name] = result.apply(
            lambda row: get_duration_h(row[Case.start_ts.name], row[Case.end_ts.name]), axis=1)
        result[Case.business_duration_h.name] = result.apply(
            lambda row: get_business_durtation_h(row[Case.start_ts.name], row[Case.end_ts.name], self._businesshrs), axis=1)
        result[Case.start_date.name] = result[Case.start_ts.name].dt.date.astype("datetime64[ns]")
        result[Case.end_date.name] = result[Case.end_ts.name].dt.date.astype("datetime64[ns]")
        return result

    def _get_first_and_last(self, eventlog):
        df = eventlog.copy(deep=True)
        df = df[~df[Eventlog.activity.name].isin([FakeActivities.START, FakeActivities.END])]
        df_first = df.groupby(Eventlog.case_id.name, as_index=False).first()
        df_last = df.groupby(Eventlog.case_id.name, as_index=False).last()
        df_first.rename(columns={Eventlog.activity.name: Case.start_node.name,
                                 Eventlog.activity_start_ts.name: Case.start_ts.name,
                                 Eventlog.case_id.name: Case.id.name},
                        inplace=True)
        df_last.rename(columns={Eventlog.activity.name: Case.end_node.name,
                                Eventlog.activity_end_ts.name: Case.end_ts.name,
                                Eventlog.case_id.name: Case.id.name},
                       inplace=True)
        columns_first = [Case.id.name, Case.start_node.name, Case.start_ts.name]
        df_first = df_first[columns_first]
        columns_last = [Case.id.name, Case.end_node.name, Case.end_ts.name]
        df_last = df_last[columns_last]
        result = pd.merge(df_first, df_last, how='left', on=Case.id.name)
        return result
