import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    #Comando Django para pausar la ejecucion hasta que la DB este disponible.
    
    def handle(self, *args, **options):
        self.stdout.write('\nEsperando a la base de datos, aguarde por favor.')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Base de datos no disponible, reintentando...')
                time.sleep(2)
        self.stdout.write(self.style.SUCCESS('¡La base de datos se ha iniciado!'))
