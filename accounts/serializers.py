from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8,write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password']
    
    def validate(self,attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)
    
    # this is overriden so that password would be hashed    
    def create(self,validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data=validated_data)
        user.set_password(password)
        user.save()
        # use to create tokens when doing token authentication
        Token.objects.create(user=user)
        return user

# this serializer returns information about a user and his/her posts.
class UserPostSerializer(serializers.ModelSerializer):
    # StringRelatedField returns a field representation
    # of the posts.
    #posts = serializers.StringRelatedField(many=True)

    posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name = "get_post",
        queryset = User.objects.all()
    )
    class Meta:
        model = User
        fields = ["id","username","email","posts"]



