from langchain_core.tools import tool
from config.db_config import SessionLocal
from models.db.Tables import Booking, Client, Service, BookingService
from datetime import datetime, date, time
import uuid


@tool
def list_bookings(status: str | None = None, date_str: str | None = None) -> str:
    """List all bookings, optionally filtered by status or date.
    Based on this you can figure out which appointments are available or which times are not booked"""
    db = SessionLocal()
    try:
        query = db.query(Booking)
        if status:
            query = query.filter(Booking.status == status)
        if date_str:
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(Booking.appointment_date == booking_date)

        bookings = query.all()
        if not bookings:
            return "No bookings found."

        result = []
        for b in bookings:
            client = db.query(Client).filter(Client.id == b.client_id).first()
            result.append(
                f"ID: {b.id}, Ref: {b.booking_ref}, Date: {b.appointment_date}, Time: {b.appointment_time}, Status: {b.status}, Client: {client.name if client else 'Unknown'}"
            )
        return "\n".join(result)
    finally:
        db.close()


@tool
def get_booking(booking_id: int | None = None, booking_ref: str | None = None) -> str:
    """Get a specific booking by ID or reference."""
    db = SessionLocal()
    try:
        if booking_id:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
        elif booking_ref:
            booking = (
                db.query(Booking).filter(Booking.booking_ref == booking_ref).first()
            )
        else:
            return "Error: Please provide either booking_id or booking_ref"

        if not booking:
            return "Booking not found."

        client = db.query(Client).filter(Client.id == booking.client_id).first()
        services = (
            db.query(BookingService)
            .filter(BookingService.booking_id == booking.id)
            .all()
        )
        service_names = []
        for bs in services:
            svc = db.query(Service).filter(Service.id == bs.service_id).first()
            if svc:
                service_names.append(svc.name)

        result = f"""Booking Details:
ID: {booking.id}
Reference: {booking.booking_ref}
Client: {client.name if client else "Unknown"} ({client.phone if client else "N/A"})
Date: {booking.appointment_date}
Time: {booking.appointment_time}
Status: {booking.status}
Services: {", ".join(service_names) if service_names else "None"}
Notes: {booking.notes or "None"}
Created: {booking.created_at}"""
        return result
    finally:
        db.close()


@tool
def create_booking(
    client_name: str,
    client_phone: str,
    client_email: str | None = None,
    date_str: str | None = None,
    time_str: str | None = None,
    service_ids: str | None = None,
    notes: str | None = None,
) -> str:
    """Create a new booking. Dates should be in YYYY-MM-DD format, times in HH:MM format.
    Returns conflict error if there's already a booking at the same date and time."""
    db = SessionLocal()
    try:
        booking_date = (
            date.today()
            if not date_str
            else datetime.strptime(date_str, "%Y-%m-%d").date()
        )
        booking_time = (
            time(10, 0) if not time_str else datetime.strptime(time_str, "%H:%M").time()
        )

        existing = (
            db.query(Booking)
            .filter(
                Booking.appointment_date == booking_date,
                Booking.appointment_time == booking_time,
                Booking.status != "cancelled",
            )
            .first()
        )

        if existing:
            client = db.query(Client).filter(Client.id == existing.client_id).first()
            print(
                f"[CONFLICT CHECK] Found existing booking at {booking_date} {booking_time}: {existing.booking_ref}"
            )
            return f"CONFLICT: There's already a booking at {booking_date} {booking_time}. Existing booking: {existing.booking_ref} by {client.name if client else 'Unknown'}. Please suggest an alternative time or date."

        print(
            f"[CONFLICT CHECK] No conflict found for {booking_date} {booking_time}, proceeding with booking"
        )

        existing_client = db.query(Client).filter(Client.phone == client_phone).first()
        if existing_client:
            client = existing_client
        else:
            client = Client(name=client_name, phone=client_phone, email=client_email)
            db.add(client)
            db.commit()
            db.refresh(client)

        booking_ref = f"BK{uuid.uuid4().hex[:8].upper()}"

        booking = Booking(
            booking_ref=booking_ref,
            client_id=client.id,
            appointment_date=booking_date,
            appointment_time=booking_time,
            notes=notes,
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        if service_ids:
            for svc_id in service_ids.split(","):
                try:
                    bs = BookingService(
                        booking_id=booking.id, service_id=int(svc_id.strip())
                    )
                    db.add(bs)
                except ValueError:
                    pass
            db.commit()

        return (
            f"Booking created successfully. Reference: {booking_ref}, ID: {booking.id}"
        )
    except Exception as e:
        db.rollback()
        return f"Error creating booking: {str(e)}"
    finally:
        db.close()


@tool
def update_booking(
    booking_id: int | None = None,
    booking_ref: str | None = None,
    date_str: str | None = None,
    time_str: str | None = None,
    status: str | None = None,
    notes: str | None = None,
) -> str:
    """Update an existing booking's date, time, status, or notes."""
    db = SessionLocal()
    try:
        if booking_id:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
        elif booking_ref:
            booking = (
                db.query(Booking).filter(Booking.booking_ref == booking_ref).first()
            )
        else:
            return "Error: Please provide either booking_id or booking_ref"

        if not booking:
            return "Booking not found."

        if date_str:
            booking.appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if time_str:
            booking.appointment_time = datetime.strptime(time_str, "%H:%M").time()
        if status:
            booking.status = status
        if notes is not None:
            booking.notes = notes

        db.commit()
        return f"Booking {booking.booking_ref} updated successfully."
    except Exception as e:
        db.rollback()
        return f"Error updating booking: {str(e)}"
    finally:
        db.close()


@tool
def cancel_booking(
    booking_id: int | None = None, booking_ref: str | None = None
) -> str:
    """Cancel a booking by setting its status to cancelled."""
    db = SessionLocal()
    try:
        if booking_id:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
        elif booking_ref:
            booking = (
                db.query(Booking).filter(Booking.booking_ref == booking_ref).first()
            )
        else:
            return "Error: Please provide either booking_id or booking_ref"

        if not booking:
            return "Booking not found."

        booking.status = "cancelled"
        db.commit()
        return f"Booking {booking.booking_ref} has been cancelled."
    except Exception as e:
        db.rollback()
        return f"Error cancelling booking: {str(e)}"
    finally:
        db.close()
