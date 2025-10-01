# DB models
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from db.DbConfig import Base, Engine


class TableNames:
    USERS = "users" # Table name for users

class ColumnNames:
    ID = "id"
    EMAIL = "email"
    HASHED_PASSWORD = "hashed_password"
    NAME = "name"
    IS_ACTIVE = "is_active"
    CRATED_AT = "created_at"

class UserDBModel(Base):
    __tablename__ = TableNames.USERS    

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(ColumnNames.EMAIL, String, unique=True, index=True, nullable=False)
    hashed_password = Column(ColumnNames.HASHED_PASSWORD, String, nullable=False)
    name = Column(ColumnNames.NAME, String, nullable=True)
    is_active = Column(ColumnNames.IS_ACTIVE, Integer, default=1)  # 1 for active, 0 for inactive
    created_at = Column(ColumnNames.CRATED_AT, TIMESTAMP(True), default=func.now(), nullable=False)

Base.metadata.create_all(bind=Engine)
print("Tables created successfully")
