from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    """Clase padre para las tags e ingredientes.
    Contiene los atributos que comparten ambas clases."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retorna objetos para el usuario autenticado"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Crea un nuevo objeto"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Maneja las TAGS en la base de datos."""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Maneja los INGREDIENTES en la base de datos."""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer



class RecipeViewSet(viewsets.ModelViewSet):
    """Maneja las recetas en la base de datos."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retorna la receta para el usuario autenticado."""
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """retorna correctamente la clase serializer."""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
            
        return self.serializer_class

    def perform_create(self, serializer):
        """Crea una nueva receta."""
        serializer.save(user=self.request.user)
    

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Sube una imagen a la receta."""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        



