import enum
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flaskapp.sqlite_database import db

class Train(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    number_of_seats: Mapped[int]
    tatkal_seats: Mapped[int] = mapped_column(default=0)
    schedules: Mapped[List["TrainSchedule"]] = relationship(back_populates="train")

class TrainStation(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

class TrainSchedule(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    train_id: Mapped[int] = mapped_column(ForeignKey(Train.id))
    source_station_id: Mapped[int] = mapped_column(ForeignKey(TrainStation.id))
    destination_station_id: Mapped[int] = mapped_column(ForeignKey(TrainStation.id))
    arrival: Mapped[datetime]
    departure: Mapped[datetime]

    train: Mapped["Train"] = relationship(back_populates="schedules", foreign_keys=[train_id])
    source_station: Mapped["TrainStation"] = relationship(foreign_keys=[source_station_id])
    destination_station: Mapped["TrainStation"] = relationship(foreign_keys=[destination_station_id])
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="schedule")


class TicketStatusEnum(enum.Enum):
    booked = "BOOKED"
    cancelled = "CANCELLED"
    waiting = "WAITING"

class TicketTypeEnum(enum.Enum):
    normal = "GENERAL"
    tatkal =  "TATKAL"

class Ticket(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    schedule_id: Mapped[int] = mapped_column(ForeignKey(TrainSchedule.id))
    status = Column(Enum(TicketStatusEnum), nullable=False)
    ticket_type = Column(Enum(TicketTypeEnum), nullable=False)
    passengers: Mapped[int]
    booked_time: Mapped[datetime]

    user: Mapped["User"] = relationship(back_populates="tickets")
    schedule: Mapped["TrainSchedule"] = relationship(back_populates="tickets")

from flaskapp.user_management.models import User
