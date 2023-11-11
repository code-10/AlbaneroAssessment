import datetime

from flask import render_template, request, flash, current_app, url_for, redirect, abort

from flaskapp.sqlite_database import db
from flaskapp.train import blueprint
from flask_login import login_required, current_user

from flaskapp.train.forms import TicketMetaForm
from flaskapp.train.models import Ticket, TicketStatusEnum, TicketTypeEnum, TrainSchedule
from flaskapp.train.service import get_all_stations, get_all_schedules_based_on_meta, get_available_seats, \
    get_user_tickets, mark_ticket_as_cancelled, promote_waiting_ticket


@blueprint.get("/")
@login_required
def index():
    return render_template("train/ticket_meta.html")

@blueprint.route("/ticket_meta", methods=["GET", "POST"])
@login_required
def ticket_meta():
    stations = [(x[1], x[0]) for x in get_all_stations()]
    current_app.logger.info(str(stations))
    form = TicketMetaForm()
    form.source_station.choices = stations
    form.destination_station.choices = stations

    if request.method == "POST" and form.validate_on_submit():
        return redirect(url_for(
            "train.list_ticket",
            source_station=form.source_station.data,
            destination_station=form.destination_station.data,
            book_on=form.book_on.data
        ))
    return render_template("train/ticket_meta.html", form=form)

@blueprint.route("/list_ticket", methods=["GET", "POST"])
@login_required
def list_ticket():
    source_station = request.args.get("source_station")
    destination_station = request.args.get("destination_station")
    book_on = datetime.datetime.strptime(request.args.get("book_on"), '%Y-%m-%d')
    train_schedules = get_all_schedules_based_on_meta(source_station, destination_station, book_on)
    current_app.logger.info(str(train_schedules))
    return render_template("train/list_ticket.html", train_schedules=train_schedules)

@blueprint.route("/book_ticket/<ticket_type>/<schedule_id>")
@login_required
def book_ticket(ticket_type, schedule_id, passenger_count=1):
    current_app.logger.info("book_ticket: %s %s", ticket_type, schedule_id)
    ticket_type_enum = TicketTypeEnum(ticket_type)
    print(ticket_type_enum)
    if ticket_type_enum == TicketTypeEnum.tatkal:
        departure_time = TrainSchedule.query.get_or_404(schedule_id).departure
        current_time = datetime.datetime.now()
        minutes_till_departure = (current_time - departure_time) // datetime.timedelta(minutes=1)
        if not (120 >= minutes_till_departure and minutes_till_departure <= 110):
            flash("Tatkal window not open yet re")
            return redirect(url_for("train.ticket_meta"))

    seat_count = get_available_seats(schedule_id)

    current_app.logger.info(seat_count)

    seat_status = None

    if passenger_count <= seat_count:
        seat_status = TicketStatusEnum.booked
    else:
        seat_status = TicketStatusEnum.waiting
    ticket = Ticket(
        user = current_user,
        schedule_id = schedule_id,
        status = seat_status,
        ticket_type = TicketTypeEnum.normal,
        passengers = 1,
        booked_time = datetime.datetime.now()
    )

    db.session.add(ticket)
    db.session.commit()
    return redirect(url_for("train.ticket_history"))

@blueprint.get("/cancel_ticket/<ticket_id>")
@login_required
def cancel_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.user_id != current_user.id:
        return abort(401)

    mark_ticket_as_cancelled(ticket)
    promote_waiting_ticket(ticket.schedule_id)
    flash("Ticket Cancelled")

    return redirect(url_for("train.ticket_history"))


@blueprint.get("/ticket_history")
def ticket_history():
    tickets = get_user_tickets(current_user)
    return render_template("train/ticket_history.html", tickets=tickets)
