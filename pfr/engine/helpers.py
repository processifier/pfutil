import datetime
import businesstimedelta
import pandas as pd
from holidays import country_holidays


def get_duration_seconds(duration):
    return datetime.timedelta(**duration).total_seconds()


def get_duration_h(start_ts, end_ts):
    duration = end_ts - start_ts
    duration_h = duration.days * 24 + duration.seconds / 3600
    return round(duration_h, 6)


def get_working_time_calculator(working_days=(0, 1, 2, 3, 4), work_start=8, work_end=16, holidays='PL'):
    holidays = businesstimedelta.HolidayRule(country_holidays(holidays))
    WORKDAY = businesstimedelta.WorkDayRule(
        start_time=datetime.time(work_start),
        end_time=datetime.time(work_end),
        working_days=list(working_days))
    businesshrs = businesstimedelta.Rules([WORKDAY, holidays])
    return businesshrs


def get_business_durtation_h(start_ts, end_ts, businesshrs):
    bdiff = businesshrs.difference(start_ts, end_ts)
    hours = bdiff.hours + bdiff.seconds/3600
    return round(hours, 6)


def trim_if_string(s: str):
    return s.strip() if isinstance(s, str) else s


def get_empty_dataframe(table):
    columns = [str(col).split('.')[1] for col in table.__table__.columns]
    return pd.DataFrame(columns=columns)
