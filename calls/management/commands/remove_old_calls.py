import os
import sys
import datetime
import time

from django.core.management.base import BaseCommand
import django.utils.timezone
from django.conf import settings

from users.utils import lock
from calls.models import Call

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

class Command(BaseCommand):

    @lock(os.path.join(CURRENT_FILE_DIR, os.path.basename(__file__)+".lock"))
    def handle(self, *args, **options):
        now = datetime.datetime.utcnow()
        last_day = now - datetime.timedelta(365*2)
        Call.objects.filter(solved_date__lte=last_day).exclude(solved=True).delete()
        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__)+"_exec.log"), "a") as f:
            f.write(str(datetime.datetime.utcnow())+" ==> Elapsed %s" % (datetime.datetime.utcnow() - now)+"\n")

