from datetime import datetime, timedelta
from ..models import db, Customer, MenuItem
from .point_system import send_email
from flask import current_app

def should_send_weekly_reminder(customer):
    # Send only if a week has passed since last reminder
    if not customer.last_reminder_sent:
        return True
    return datetime.utcnow() - customer.last_reminder_sent >= timedelta(weeks=1)

def send_weekly_reminders(app):
    with app.app_context():
        customers = Customer.query.all()
        for customer in customers:
            # Check eligible rewards
            rewards = MenuItem.query.filter(MenuItem.required_points <= customer.points).all()
            if rewards and should_send_weekly_reminder(customer):
                send_reminder_email(customer.email, rewards, customer.points)
                customer.last_reminder_sent = datetime.utcnow()
               
        db.session.commit()

from textwrap import dedent

def send_reminder_email(to_email, rewards, points):
    reward_list = "\n".join(f"    - {r.name} ({r.required_points} points)" for r in rewards)

    body = dedent(f"""\
    You currently have {points} points!

    Here are rewards you can claim right now:
    \n{reward_list}

    Visit us soon to redeem your rewards.
    """)

    try:
        send_email(to_email, "Rewards available for you!", body)
        current_app.logger.info(f"Reminder sent to {to_email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send reminder to {to_email}: {str(e)}")


