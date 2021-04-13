from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
#---------------------------------------------//


class AdminSiteTests(TestCase):
    
    def setUp(self):
        # setUp() realiza una configuracion inicial para el resto de
        # tests dentro de una clase test.
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@testeo.com',
            password='12345678'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='pleb@testeo.com',
            password='12345678', 
            name='Pepito pepon'
        )
    
    def test_users_listed(self):
        #Testea que los usuarios esten enlistados en la user page.
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_user_change_page(self):
        #Testea que la edicion en la pagina del usuario funcione.
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/'ID'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        #Testea que la pagina de creacion de usuarios funcione.
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    

