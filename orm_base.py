from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base(metadata=MetaData(schema=(input('Schema name [028199975]-->') or "028199975")))
metadata = Base.metadata