from sqlalchemy.orm import DeclarativeBase , sessionmaker , relationship
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String , create_engine , ForeignKey
from typing import Optional
from sqlalchemy.sql import select

class Base(DeclarativeBase):
    pass

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    fullname: Mapped[Optional[str]]
    def __repr__(self):
        return f"\n\nid: {self.id}\nname: {self.name}\nfullname: {self.fullname}\n\n"
    __tablename__ = "userss"


class Address(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    emailaddress: Mapped[str]
    user_id: Mapped[int] = ForeignKey("userss.id")
    def __repr__(self):
        return f"Addres: (id={self.id} email_address={self.emailaddress})"
    __tablename__ = "Addresses"


engine = create_engine("sqlite:///database.db" , echo=True)
Base.metadata.create_all(engine)

#ساخت اتصال به دیتابیس
Session = sessionmaker(engine , expire_on_commit=False)

#افزودن مقدار به جدول
#with Session() as session:
 #  user = User(name = "ali" , fullname="ali sadeghi")
   #session.add(user)
  # session.commit()


#خواندن مقدار از جدول
with Session() as session:
    stmt = select(User).where(User.fullname=="ali sadeghi")
    result, = session.execute(stmt).first()
    result.name= "mohammad"
    session.commit()

   # session.delete(result)