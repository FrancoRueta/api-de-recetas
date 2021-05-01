from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializador para objetos tipo tag"""

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)




class IngredientSerializer(serializers.ModelSerializer):
    """Serializador para objetos tipo ingrediente"""

    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)
    


class RecipeSerializer(serializers.ModelSerializer):
    """Serializador para objetos tipo receta."""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id','title','ingredients','tags',
            'time_minutes','price','link'
        )
        read_only_fields = ('id',)
    

class RecipeDetailSerializer(RecipeSerializer):
    """Serializa un detalle de receta."""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)




class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializador para subir imagenes a recetas."""

    class Meta:
        model = Recipe
        fields = ('id','image')
        read_only_fields = ('id',)