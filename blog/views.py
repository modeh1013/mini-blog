from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Post


@api_view(["GET"])
def list_posts(request):
    posts = Post.objects.all().order_by("-created_at")
    return Response({"posts": [post.to_dict() for post in posts]})


@api_view(["POST"])
def create_post(request):
    try:
        user_id = request.headers.get("x-user-id")
        if not user_id:
            return Response(
                {"message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        title = request.data.get("title")     #comment this line out
        content = request.data.get("content")
        category = request.data.get("category")

        if not title or not content or not category:
            return Response(
                {"message": "Title, content, and category are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            author_id=int(user_id),
        )

        return Response(
            {"message": "Post created successfully", "post": post()},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        print(f"Create post error: {e}") 
        return Response(
            {"message": "Server error creating post"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )