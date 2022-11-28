"""
Handle crons
"""
import datetime
import string

from enum import Enum
from crontab import CronTab


class ExecutionPlan(Enum):
    """
    Available execution plans
    """
    hourly = 1
    daily = 2
    weekly = 3


def create_cron(name, command: string, start: datetime.datetime = datetime.datetime.now(),
    interval: ExecutionPlan = ExecutionPlan.daily):
    """
    Create new cron
    """
    cron = CronTab(user=True)
    for job in cron:
        if job.comment == name:
            cron.remove(job)
            cron.write()

    task = cron.new(comment=name, command=command +
                    " >> /var/log/cron.log 2>&1")

    if interval is not None:
        if interval == ExecutionPlan.hourly:
            task.hour.every(1)
        elif interval == ExecutionPlan.daily:
            task.hour.on(start.hour)
            task.minute.on(start.minute)
            task.day.every(1)
        elif interval == ExecutionPlan.weekly:
            task.hour.on(start.hour)
            task.minute.on(start.minute)
            task.hour.on(start.hour)
            task.day.every(7)

    cron.write()


def list_crons():
    """
    List all crons
    """
    result = []
    cron = CronTab(user=True)
    for job in cron:
        result.append(job.render())

    return result
