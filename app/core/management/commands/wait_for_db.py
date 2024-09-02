"""
Django command to wait for database to available
"""

import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to for database to be available"""

    def handle(self, *args, **kwargs):
        """Entrypoint for command"""

        self.stdout.write("Waiting for database to be available.....")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write(
                    self.style.ERROR(
                        "Database is unavailable Retrying in 5 seconds."))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is available!"))
