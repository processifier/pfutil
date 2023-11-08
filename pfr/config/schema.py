from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Variant(Base):
    __tablename__ = "variant"
    id = Column(Integer, name=__tablename__ + '_id', primary_key=True, autoincrement=False)
    variant_rank = Column(Integer)
    variant_freq = Column(Integer)
    variant_hash = Column(String(256))



class Case(Base):
    __tablename__ = "case_"
    id = Column(Integer, name=__tablename__ + 'id', primary_key=True, autoincrement=False)
    variant_id = Column(Integer, name=Variant.id.name, nullable=False)
    start_node = Column(String(128))
    end_node = Column(String(128))
    start_ts = Column(DateTime)
    end_ts = Column(DateTime)
    start_date = Column(Date)
    end_date = Column(Date)
    business_duration_h = Column(Float)
    duration_h = Column(Float)


class Eventlog(Base):
    __tablename__ = "eventlog"
    id = Column(Integer, name=__tablename__ + '_id', primary_key=True, autoincrement=False)
    case_id = Column(Integer, name=Case.id.name, nullable=False)
    activity = Column(String(128))
    activity_next = Column(String(128))
    activity_start_ts = Column(DateTime)
    activity_end_ts = Column(DateTime)
    activity_start_date = Column(Date)
    activity_end_date = Column(Date)
    activity_business_duration_h = Column(Float)
    activity_duration_h = Column(Float)
    transition_name = Column(String(256))
    transition_start_ts = Column(DateTime)
    transition_end_ts = Column(DateTime)
    transition_business_duration_h = Column(Float)
    transition_duration_h = Column(Float)
    resource = Column(String(128))


class GlobalStats(Base):
    __tablename__ = "global_stats"
    id = Column(Integer, name=__tablename__ + '_id', primary_key=True, autoincrement=False)
    number_of_variants = Column(Integer)
    number_of_cases = Column(Integer)
