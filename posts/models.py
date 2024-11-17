from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    # Associates users with posts
    # The related name creates a reverse 
    # helps us to be able to access the posts
    # on the user.  
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts",default=None,null=True)

    # string representation of the post.
    def __str__(self) -> str:
        return self.title
    