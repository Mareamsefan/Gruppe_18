from sqlalchemy import Table, Column, String, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from Gruppe_18.src.main.database.app_config import db

tour_account_association = Table(
    'tour_account_association', db.metadata,
    Column('tour_id', String, ForeignKey('Tour.id')),
    Column('account_id', String, ForeignKey('User.id'))
)


guide_tour_association = Table(
    'guide_tour_association', db.metadata,
    Column('tour_id', String, ForeignKey('Tour.id')),
    Column('guide_id', String, ForeignKey('User.id')),
)


class Account(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.String, primary_key=True)
    usertype = Column("usertype", String)
    username = Column("username", String)
    password = Column("password", String)
    phoneNumber = Column("phoneNumber", String)
    emailAddress = Column("emailAddress", String)
    tours = relationship("Tour", secondary=tour_account_association, back_populates="participants")
    guide_tours = relationship("Tour", secondary=guide_tour_association , back_populates="owners")

    def get_id(self):
        return str(self.id)

    def __init__(self, id, usertype, username, password, phoneNumber, emailAddress):
        self.id = id
        self.usertype = usertype
        self.username = username
        self.password = password
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress

    def __repr__(self):
        return f"({self.id}) {self.usertype} {self.username} {self.password} {self.phoneNumber} {self.emailAddress}"


class Tour(db.Model):
    # duration in hours
    # cost in dollars
    __tablename__ = "Tour"
    id = Column("id", String, primary_key=True)
    title = Column("title", String)
    date = Column("date", DATETIME)
    destination = Column("destination", String)
    duration = Column("duration", Integer)
    cost = Column("cost", Integer)
    max_travelers = Column("max_travelers", Integer)
    language = Column("language", String)
    pictureURL = Column("pictureURL", String)
    booked = Column("booked", Integer, default=0)
    participants = relationship("Account", secondary=tour_account_association, back_populates="tours")
    owners = relationship("Account", secondary=guide_tour_association, back_populates="guide_tours")

    def __init__(self, id,  title, date, destination, duration, cost, max_travelers, language, pictureURL):
        self.id = id
        self.title = title
        self.date = date
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.language = language
        self.max_travelers = max_travelers
        self.pictureURL = pictureURL

    def __repr__(self):
        return f"({self.id}) {self.title} {self.destination} {self.duration} {self.cost} {self.language} {self.max_travelers} {self.pictureURL} {self.booked}"

    def get_id(self):
        return str(self.id)
