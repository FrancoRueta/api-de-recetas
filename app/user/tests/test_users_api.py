from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status



CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Testea pedidos a la API que no requieren autenticacion."""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """ Testea que la creacion de un usuario 
        con parametros validos sea correcta."""
        parametros = {
            'email': 'test@francorueta.com',
            'password': 'test1234',
            'name': 'Pepito'
        }
        res = self.client.post(CREATE_USER_URL,parametros)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(parametros['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Testea la creacion de un usuario ya existente."""
        parametros = {'email': 'test@francorueta.com','password': 'test1234'}
        create_user(**parametros)

        res = self.client.post(CREATE_USER_URL, parametros)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Testea que el password deba ser de mas de 6 caracteres."""
        parametros = {'email':'test@francorueta.com','password':'pw'}
        res = self.client.post(CREATE_USER_URL, parametros)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=parametros['email']
        ).exists()
        self.assertFalse(user_exists)

    
    def test_create_token_for_user(self):
        """Testea la creacion valida de un token de usuario."""
        parametros = {'email':'test@francorueta.com','password':'test1234'}
        create_user(**parametros)
        res = self.client.post(TOKEN_URL, parametros)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Testea la no creacion de un token de usuario
         debido al uso de datos invalidos."""
        create_user(email='test@francorueta.com',password='test1234')
        parametros = {'email': 'test@francorueta.com','password': 'test123'}
        res = self.client.post(TOKEN_URL, parametros)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """ Testea la no creacion de un token
         cuando no existe un usuario."""
        parametros = {'email':'test@francorueta.com','password':'test1234'}
        res = self.client.post(TOKEN_URL, parametros)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Testea que un email y password sean 
        requeridos para crear un token."""
        res = self.client.post(TOKEN_URL, {'email':'mal','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """Testea que la autenticacion es requerida para los usuarios."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Testea pedidos a la API que requieren autenticacion."""

    def setUp(self):
        self.user = create_user(
            email='test@francorueta.com',
            password='test1234',
            name='ejemplo'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Testea retornar el perfil para el usuario logeado."""
        res = self.client.get(ME_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name' : self.user.name,
            'email': self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """Testea que POST no este permitido en la url ME"""
        res = self.client.post(ME_URL,{})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """Testea la actualizacion del perfil para un usuario autenticado."""
        parametros = {'name': 'nuevoNom', 'password': 'pass1234'}
        res = self.client.patch(ME_URL,parametros)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, parametros['name'])
        self.assertTrue(self.user.check_password(parametros['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)






