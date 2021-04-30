from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer



RECIPES_URL = reverse('recipe:recipe-list')




def detail_url(recipe_id):
    """Devuelve una url detallada de receta."""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='Vegano'):
    """Crea y retorna una tag de prueba."""
    return Tag.objects.create(user=user,name=name)

def sample_ingredient(user, name='Pepino'):
    """Crea y retorna un ingrediente de prueba."""
    return Ingredient.objects.create(user=user,name=name)


def sample_recipe(user, **params):
    """Crea y retorna una receta de prueba."""
    defaults = {
        'title': 'Receta X',
        'time_minutes': 30,
        'price': 300.00
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)




class PublicRecipeApiTests(TestCase):
    """Testea la API de recetas sin un usuario."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Testea que las peticiones a la API requieran un usuario"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    


class PrivateRecipeApiTests(TestCase):
    """Testea funciones de la API con un usuario autenticado."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@francorueta.com',
            'test1234'
        )
        self.client.force_authenticate(self.user)
    

    def test_retrieve_recipes(self):
        """Testea retornar una lista de usuarios."""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipes_limited_to_user(self):
        """Testea retornar las recetas para un usuario"""
        usuario2 = get_user_model().objects.create_user(
            'test2@francorueta.com',
            'test1234'
        )
        sample_recipe(user=usuario2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data,serializer.data)
    

    def test_view_recipe_detail(self):
        """Testea la visualizacion de un detalle de receta."""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_basic_recipe(self):
        """Testea la creacion de una receta."""
        parametros = {
            'title':'Milanesa',
            'time_minutes':120,
            'price':450.00
        }
        res = self.client.post(RECIPES_URL, parametros)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in parametros.keys():
            self.assertEqual(parametros[key], getattr(recipe, key))
        
    def test_create_recipe_with_tags(self):
        """Testea la creacion de una receta con tags."""
        tag1 = sample_tag(user=self.user,name='Veraniego')
        tag2 = sample_tag(user=self.user,name='Calorico')
        parametros = {
            'title':'Helado',
            'tags': [tag1.id, tag2.id],
            'time_minutes':45,
            'price':330.00
        }

        res = self.client.post(RECIPES_URL, parametros)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(),2)
        self.assertIn(tag1,tags)
        self.assertIn(tag2,tags)
    

    def test_create_recipe_with_ingredients(self):
        """Testea la creacion de una receta con ingredientes."""
        ingrediente1 = sample_ingredient(user=self.user,name='Jamon')
        ingrediente2 = sample_ingredient(user=self.user,name='Salame')
        parametros = {
            'title':'Picada',
            'ingredients':[ingrediente1.id,ingrediente2.id],
            'time_minutes':20,
            'price':550.00
        }

        res = self.client.post(RECIPES_URL,parametros)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(),2)
        self.assertIn(ingrediente1,ingredients)
        self.assertIn(ingrediente2,ingredients)


        