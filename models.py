from sqlalchemy.ext.asyncio import async_sessionmaker , AsyncAttrs , create_async_engine
from sqlalchemy.orm import DeclarativeBase , Mapped ,mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
from sqlalchemy import BIGINT
from sqlalchemy.sql import select

class Base(AsyncAttrs , DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id : Mapped[int] = mapped_column(BIGINT() , unique=True)
    user_name : Mapped[str] = mapped_column(nullable=True , default= None)
    first_name:Mapped[str] = mapped_column(nullable=True, default=None)
    last_name:Mapped[str] = mapped_column(nullable=True, default=None)
    join_date:Mapped[datetime] = mapped_column(default=datetime.now)
    is_blocked:Mapped[bool] = mapped_column(default=False)
    max_number:Mapped[int] = mapped_column(BIGINT,default=100)
    min_number:Mapped[int] = mapped_column(BIGINT,default=0)

    


_engine = create_async_engine("sqlite+aiosqlite:///database.db")
Session = async_sessionmaker(_engine,expire_on_commit=False)

async def create_table()->None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_user(
        user_id:int,
        user_name:str | None=None,
        first_name:str | None=None,
        last_name:str | None=None,
        join_date:datetime | None=None,
        max_number:int | None=None,
        min_number:int | None=None
        )->User:
    user = User(user_id=user_id,user_name=user_name,first_name=first_name,last_name=last_name,join_date=join_date,max_number=max_number,min_number=min_number)
    async with Session.begin() as session:
        session.add(user)
        print("\n\n user inserted in session. add \n\n\n")
    return user

async def get_user(user_id:int)->User:
    query = select(User).where(User.user_id==user_id)
    async with Session.begin() as session:
        user = await session.scalar(query)
    return user

async def change_max(user_id:int , max_number:int)->User:
    async with Session.begin() as session:
        query = select(User).where(User.user_id == user_id)
        user = await session.scalar(query)
        if user is None:
            return
        user.max_number=max_number

async def change_min(user_id:int , min_number:int)->User:
    async with Session.begin() as session:
        query = select(User).where(User.user_id == user_id)
        user = await session.scalar(query)
        if user is None:
            return
        user.min_number=min_number