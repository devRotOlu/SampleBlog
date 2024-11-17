from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status,generics,mixins
from rest_framework.decorators import api_view,APIView,permission_classes
from .models import Post
from .serializers import PostSerializser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

from accounts.serializers import UserPostSerializer
from .permissions import ReadOnly,AuthorOrReadOnly

# The response class helps customize the way we return http response.
# The api_view decorator tells django_rest framework that this is an api view.
@api_view(http_method_names=["GET","POST"])
def homepage(request:Request):
    response = {"message":"Hello World"}
    if request.method == "POST":
        data = request.data
        response["data"] = data
        return Response(data=response,status=status.HTTP_201_CREATED)
    return Response(data=response,status=status.HTTP_200_OK)

# to get all posts and to add post
# @api_view(http_method_names=["GET","POST"])
# def list_posts(request:Request):
#     if request.method == "POST":
#         data = request.data
#         serializer = PostSerializser(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message":"Post Created",
#                 "data":serializer.data
#             }
#             return Response(data=response,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     # querying for posts
#     posts = Post.objects.all()
#     # serializing posts
#     serializer = PostSerializser(instance=posts,many=True)
#     response = {
#         "message":"posts",
#         "data":serializer.data
#     }
#     return Response(data=response,status=status.HTTP_200_OK);

# class PostListCreateView(APIView):

#     # The searilizer_class allows us to convert our object to JSON and to create our post object to some validation of the various field to be passed to our API.   
#     serializer_class = PostSerializser

#     def get(self,request:Request,*args,**kwargs):
#        posts = Post.objects.all()
#        serializer = self.serializer_class(instance=posts,many=True)
#        return Response(data=serializer.data,status=status.HTTP_200_OK)

#     def post(self,request:Request,*args,**kwargs):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#             "message":"Post created",
#             "data":serializer.data
#             }
#             return Response(data=response,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=["GET"])
# def get_post(request:Request,post_id:int):
#     post = get_object_or_404(Post,pk=post_id)
#     serializer = PostSerializser(instance=post)
#     response = {
#         "message":"post",
#         "data":serializer.data
#     }
#     return Response(data=response,status=status.HTTP_200_OK)


# @api_view(http_method_names=["PUT"])
# def update_post(request:Request,post_id:int):
#     post = get_object_or_404(Post,pk=post_id)
#     serializer = PostSerializser(instance=post,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         response = {
#             "message":"Post updated successfully",
#             "data":serializer.data
#         }
#         return Response(data=response,status=status.HTTP_200_OK)
#     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=["DELETE"])
# def delete_post(request:Request,post_id:int):
#     post = get_object_or_404(Post,pk=post_id)
#     post.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# class PostRetrieveUpdateAndDeleteView(APIView):
#     serilizer_class = PostSerializ ser

#     def get(self,request:Request,post_id:int):
#         post = get_object_or_404(Post,pk=post_id)
#         seriliazer = self.serilizer_class(instance=post)
#         return Response(data=seriliazer.data,status=status.HTTP_200_OK)

#     def put(self,request:Request,post_id:int):
#         post = get_object_or_404(Post,pk=post_id)
#         data = request.data
#         serializer = self.serilizer_class(instance=post,data = data)

#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                "message":"Post updated",
#                "data":serializer.data 
#             }
#             return Response(data=response,status=status.HTTP_200_OK)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request:Request,post_id:int):
#         post = get_object_or_404(Post,pk=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        

# Django rest framework provides mixins classes taht we use with class based views to help carry out functionalities that we may write with very many lines of codes.

class PostListCreateView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):   
    serializer_class = PostSerializser
    queryset = Post.objects.all()

    # this ensures all routes within this class 
    # are protected. 
    permission_classes = [IsAuthenticatedOrReadOnly]

    #permission_classes = [ReadOnly]

    # this mixin hook is used so as to associate a created
    # post with a user.
    def perform_create(self,serializer): 
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)
    
    def get(self,request:Request,*args,**kwargs):
        # mixins allows us to carry out functionalities such as list out our post without having to query the database ourself.
        return self.list(request,*args,**kwargs)

    def post(self,request:Request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class PostRetrieveUpdateAndDeleteView(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,
mixins.DestroyModelMixin):
    serializer_class = PostSerializser
    queryset = Post.objects.all()

    permission_classes = [AuthorOrReadOnly]

    def get(self,request:Request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request:Request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request:Request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

# gives details of a user with all 
# their posts.
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_user_posts(request:Request):
    user = request.user

    # the context argument is used cause we are using 
    # HyperlinkedRelatedField in UserPostSerializer
    serializer = UserPostSerializer(instance=user,context={
        "request":request
    })

    return Response(data=serializer.data,status=status.HTTP_200_OK)

class AuthorPosts(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializser
    permission_classes = [IsAuthenticated]

    # The get_query set method allows 
    # us to define how we want to return
    # a list of posts.
    # def get_queryset(self):
    #     user = self.request.user
    #     return Post.objects.filter(author=user)

    # a second approach to get list of posts
    # based on a username is to modify the
    # url.
    def get_queryset(self):
        username = self.kwargs.get("username")
        # field lookup to access author with the
        # username
        return Post.objects.filter(author__username=username)
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)




