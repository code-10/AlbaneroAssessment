import datetime

import click
from flask import current_app
from sqlalchemy import select, cast, Date, func
from sqlalchemy.orm import joinedload

from flaskapp.train.models import Train, TrainStation, TrainSchedule, Ticket, TicketStatusEnum
from flaskapp.sqlite_database import db
from flaskapp.user_management.models import User


def get_all_stations():
    stmt = select(TrainStation.name, TrainStation.id)
    res = db.session.execute(stmt)
    return res.all()

def get_all_schedules_based_on_meta(src_id, dest_id, book_date):
    res = (db.session.query(TrainSchedule)
           .join(Train, TrainSchedule.train)
           .filter(
                TrainSchedule.source_station_id == src_id,
                TrainSchedule.destination_station_id == dest_id,
                cast(TrainSchedule.arrival, Date) == cast(book_date, Date)
            )
           .all())
    return res

def get_available_seats(schedule_id):
    total_seats = db.session.query(Train.number_of_seats).join(Train, TrainSchedule.train).filter(TrainSchedule.id == schedule_id).scalar()
    seats_taken = (db.session.query(func.count(Ticket.id))
                     .join(TrainSchedule, Ticket.schedule)
                     .filter(Ticket.status == TicketStatusEnum.booked, Ticket.schedule_id == schedule_id)
                     .scalar())
    res = total_seats - seats_taken
    return 0 if res <= 0 else res

def get_user_tickets(user):
    tickets = (db.session.query(Ticket)
               .join(TrainSchedule, Ticket.schedule)
               .filter(Ticket.user_id == user.id)
               .all())
    return tickets

def mark_ticket_as_cancelled(ticket):
    ticket.status = TicketStatusEnum.cancelled
    db.session.commit()

def promote_waiting_ticket(schedule_id):
    keep_going = True

    while keep_going:
        available_seats = get_available_seats(schedule_id)
        eligible_ticket = (db.session.query(Ticket)
                           .order_by(Ticket.booked_time.desc())
                           .filter(Ticket.passengers <= available_seats, Ticket.status == TicketStatusEnum.waiting)
                           .first()
                           )
        if eligible_ticket is not None:
            current_app.logger.info("Ticket %s promoted", eligible_ticket.id)
            eligible_ticket.status = TicketStatusEnum.booked
            db.session.commit()
        else:
            keep_going = False

def init_db(db):
    Train.query.delete()
    TrainStation.query.delete()
    TrainSchedule.query.delete()
    Ticket.query.delete()

    train1 = Train(name="Train 1", number_of_seats=5, tatkal_seats=3)
    train2 = Train(name="Train 2", number_of_seats=3, tatkal_seats=2)

    bangalore = TrainStation(name="Bangalore")
    mysore = TrainStation(name="Mysore")
    delhi = TrainStation(name="Delhi")

    ts1 = TrainSchedule(
        arrival = datetime.datetime(2023, 11, 12, 12, 00, 00),
        departure = datetime.datetime(2023, 11, 12, 12, 15, 00),
        train = train1,
        source_station = bangalore,
        destination_station = mysore
    )
    ts2 = TrainSchedule(
        arrival = datetime.datetime(2023, 11, 12, 16, 00, 00),
        departure = datetime.datetime(2023, 11, 12, 16, 15, 00),
        train = train2,
        source_station = mysore,
        destination_station = delhi
    )
    db.session.add_all([train1, train2])
    db.session.add_all([bangalore, mysore, delhi])
    db.session.add_all([ts1])
    db.session.commit()
