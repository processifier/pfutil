import datetime
import pandas as pd


def get_duration_seconds(duration):
    return datetime.timedelta(**duration).total_seconds()


def get_duration_h(start_ts, end_ts):
    duration = end_ts - start_ts
    duration_h = duration.days * 24 + duration.seconds / 3600
    return round(duration_h, 6)


def trim_if_string(s: str):
    return s.strip() if isinstance(s, str) else s


def get_empty_dataframe(table):
    columns = [str(col).split('.')[1] for col in table.__table__.columns]
    return pd.DataFrame(columns=columns)
