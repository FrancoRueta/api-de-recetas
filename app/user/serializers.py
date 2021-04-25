from django.contrib.auth import get_user_model , authenticate
from django.utils.translation import ugettext_lazy as _T
#Django 
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializador para el objeto Usuario."""

    class Meta:
        model = get_user_model()
        #FIELDS: Los campos agregados aqui podran luego ser usados
        #mediante read/write por nuestra API. si se desea agregar, por
        #ejemplo, fechaNacimiento deberia agregarse como valor aqui.
        fields = ('email','password','name')
        extra_kwargs = {'password': {'write_only': True,'min_length':6}}
    
    def create(self, validated_data):
        """#Crea un nuevo usuario con la contraseña encriptada."""
        return get_user_model().objects.create_user(**validated_data)

    
    def update(self, instance, validated_data):
        """Actualiza un usuario, utilizando la contraseña correctamente y devolviendola."""
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """#Serializador para el token de autenticacion de usuario"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        """#Valida y autentifica el usuario."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _T('No ha sido posible autenticar con los datos otorgados.')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user'] = user
        return attrs


