from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models



def sample_user(email='test@londonappdev.com',password='testpass'):
    """Crea un usuario de prueba"""
    return get_user_model().objects.create_user(email,password)



class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """#Testea la creacion de un nuevo usuario via email."""
        email = 'prueba@hotmail.com'
        password = 'Prueba123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """#Testea que el email para un nuevo usuario este normalizado."""
        email = 'testeo@HOTMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """#Testea que crear un usuario sin email tire error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_super_user(self):
        """#Testea la creacion efectiva de un nuevo superusuario."""
        user = get_user_model().objects.create_superuser(
            'test@superusuario.com',
            'test123'
        )
 
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_tag_str(self):
        """Testea la representacion de la tag en string."""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegano'
        )

        self.assertEqual(str(tag), tag.name)



    def test_ingredient_str(self):
        """Testea la representacion del ingrediente en string."""
        ingrediente = models.Ingredient.objects.create(
            user=sample_user(),
            name='Lechuga'
        )

        self.assertEqual(str(ingrediente), ingrediente.name)

    
    def test_recipe_str(self):
        """Testea la representacion de la receta en string."""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Fideos a la pomarola',
            time_minutes=5,
            price=200.00
        )
    
        self.assertEqual(str(recipe), recipe.title)


    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Testea que la imagen se guarde en la ubicacion correcta"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)