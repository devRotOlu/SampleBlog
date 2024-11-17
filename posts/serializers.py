from rest_framework import serializers

from .models import Post 

# The serializer validate our data and serializes it.
class PostSerializser(serializers.ModelSerializer):
    # validating model data.
    title=serializers.CharField(max_length=50)
    class Meta:
        model = Post
        fields = ["id","title","content","created"]
    