from rest_framework.test import APITestCase,APIRequestFactory
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .views import PostListCreateView

User = get_user_model()

class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        # the reverse function returns the url with
        # the specified name.
        response = self.client.get(reverse("posts_home"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Hello World")

class PostListCreateTestCase(APITestCase):
    # the setup method allows us to set up our test cases, it runs first everytime we run our test cases.

    # the request factory allows us to create request that we attach to various views

    # when we use client provided by APITestCase, 
    # litte or no set up is required i.e., the 
    # client is robust that the request factory.

    def setUp(self):
        self.url = reverse("list_posts")

    # def setUp(self):
    #     self.factory = APIRequestFactory()
    #     self.view = PostListCreateView.as_view()
    #     self.url = reverse("list_posts")
    #     self.user = User.objects.create(username="johnny",email="john@gmail.com",password="john1234")
        
    # def text_list_posts(self):
    #     request = self.factory.get(self.url)
    #     response = self.view(request)

    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
    #     self.assertEqual(response.data["count"],0)
    #     self.assertEqual(response.data["result"],[])

    def text_list_posts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["count"],0)
        self.assertEqual(response.data["result"],[])

    # note this test is in doubt
    # def test_post_creation(self):
    #     sample_post = {
    #         "title":"Sample post",
    #         "content":"Sample content"
    #     }
    #     request = self.factory.post(self.url,sample_post)
    #     request.user = self.user
    #     response = self.view(request)

    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_post_creation(self):
        self.authenticate()
        sample_data = {
            "title":"Sample title",
            "content":"Sample content"
        }
        response = self.client.post(reverse(self.url),sample_data)

        self.assertEqual(response.status_code,status=status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"],sample_data["title"])


    def authenticate(self):
        self.client.post(reverse("signup"),{
            "email":"john@gmail.com",
            "password":"password123",
            "username":"johnny"
        })

        response = self.client.post(reverse("login"),{
            "email":"john@gmail.com",
            "password":"password123",
        })

        #print(response.data)
        token = response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")