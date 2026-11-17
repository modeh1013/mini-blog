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

        title = request.data.get("title")    
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
            {"message": "Post created successfully", "post": post.to_dict()},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        print(f"Create post error: {e}") 
        return Response(
            {"message": "Server error creating post"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
def delete_post(request, post_id):
    try:
        user_id = request.headers.get("x-user-id")
        if not user_id:
            return Response(
                {"message": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user_id = int(user_id)
        except ValueError:
            return Response(
                {"message": "Invalid user ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response(
                {"message": "Post doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.author_id != user_id:
            return Response(
                {"message": "You are not authorized to delete this post"},
                status=status.HTTP_403_FORBIDDEN,
            )

        post.delete()
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print(f"Delete post error: {e}") 
        return Response(
            {"message": "Server error deleting post"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )