import os
from dotenv import load_dotenv; load_dotenv()
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Numeric, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from password_hash import get_hashed_password

db_uri = os.environ.get("DB_URI")
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id = Column('id', Integer, primary_key = True)
    title = Column("title", String)
    description = Column("description", String)
    image = Column('image', String)
    genres = Column('tags', String)

    def __init__(self, 
                 id_,
                 title_, description_,
                 image_, genres_):
        self.id = id_; self.title = title_; self.description = description_; self.image = image_; self.genres = genres_

    def __repr__(self):
        return f'{self.title} : {self.description}'

class User(Base):
    __tablename__ = "users"

    user_id = Column('user_id', Integer, primary_key = True, autoincrement = True)
    user_name = Column('user_name', String, unique = True)
    user_email = Column('user_email', String, unique = True)
    user_password_hash = Column('password', VARCHAR)

    def __init__(self, name, email, password):
        self.user_name = name; self.user_email = email
        self.user_password_hash = get_hashed_password(password)

    def __repr__(self):
        return f'{self.user_name} : {self.user_email}'

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column('booking_id', Integer, primary_key = True, autoincrement = True)
    user_id = Column('user_id', Integer)
    movie_id = Column('movie_id', Integer)
    booking_date = Column('booking_date', String)
    
    def __init__(self, u_id, m_id, b_date):
        self.user_id = u_id; self.movie_id = m_id; self.booking_date = b_date

    def __repr__(self):
        return f'{self.booking_id} : {self.user_id} : {self.movie_id}'

engine = create_engine(db_uri, echo = False)
Base.metadata.create_all(bind = engine) # creates the tables in the database

Session = sessionmaker(bind = engine)
session = Session()