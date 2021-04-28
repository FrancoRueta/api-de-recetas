from rest_framework import serializers

from core.models import Tag, Ingredient


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