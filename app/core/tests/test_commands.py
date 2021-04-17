from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from unittest.mock import patch


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        #Testea la espera de la db cuando la db esta activa. 
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)
    
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        #Testea la espera de la database
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)