from django.shortcuts import render
from .models import Blog, Like, Comment
from .serializer import BlogSerializer, LikeSerializer, CommentSerializer
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import decorators, permissions as rest_permission
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    # max_page_size = 10000


@decorators.permission_classes([rest_permission.IsAuthenticated])
class BlogView(APIView):
    paginate_class = CustomPageNumberPagination

    def get(self, request):
        user = request.user
        blogs = Blog.objects.filter(author=user)
        paginate = self.paginate_class()
        result = paginate.paginate_queryset(blogs, request)
        serializer = BlogSerializer(result, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=user)
            if blog.is_published():
                self.send_publieshed(user)
                return Response({
                    "message": "blog created and not published",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED
                })
            else:
                self.send_not_publieshed(user)
                return Response({
                    "message": "blog created but not published",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED
                })

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_publieshed(self, user):
        subject = "Blog Created and published"
        message = (
            f"hi {user.first_name}{user.last_name}/n"
            f"your blog is created and Published"
        )
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def send_not_publieshed(self, user):
        subject = "Blog Created but not published"
        message = (
            f"hi {user.first_name}{user.last_name}/n"
            f"your blog is created but not Published"
        )
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def patch(self, request, id=None):
        blog = Blog.objects.get(id=id)
        user = request.user
        previous_is_published = blog.is_published
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            update_blog = serializer.save()
            current_is_published = update_blog.is_published()

            if previous_is_published != current_is_published:
                if current_is_published:
                    self.change_published(user)
                    return Response({
                        "message": "blog updated and published",
                        "data": serializer.data,
                        "status": status.HTTP_200_OK
                    })
                else:
                    self.change_unpublished(user)
                    return Response({
                        "message": "blog updated and not published",
                        "data": serializer.data,
                        "status": status.HTTP_200_OK
                    })
            else:
                self.content_updated(user)
                return Response({
                    "message": "blog content updated",
                    "status": status.HTTP_200_OK
                })
        else:
            return Response({
                "message": "some thing went wrong",
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

    def change_published(user):
        subject = "Blog updated and  Published"
        message = (
            f"hi {user.first_name}{user.last_name}/n"
            f"your blog is updated and  Published"
        )
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def content_updated(user):
        subject = "Blog updated"
        message = (
            f"hi {user.first_name}{user.last_name}/n"
            f"your blog is updated "
        )
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def change_unpublished(user):
        subject = "Blog updated but not  Published"
        message = (
            f"hi {user.first_name}{user.last_name}/n"
            f"your blog is updated but not Published"
        )
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def delete(self, request, id=None):
        user = request.user
        blog = Blog.objects.get(id=id)

        if blog.author == user:
            blog.delete()
            return Response({
                "message": "blog deleted",
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "you are not the author of this blog",
                "status": status.HTTP_400_BAD_REQUEST
            })


@decorators.permission_classes([rest_permission.AllowAny])
class GetblogsView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request, id=None):
        if id:
            blog = Blog.objects.get(id=id, is_published=True)
            serializer = BlogSerializer(blog, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            blog = Blog.objects.filter(is_published=True)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(blog, request)
            serializer = BlogSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)


@decorators.permission_classes([rest_permission.AllowAny])
class LikeGeneralView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        like = Like.objects.all()
        paginate = self.pagination_class()
        result = paginate.paginate_queryset(like, request)
        serializer = LikeSerializer(result, many=True)
        return Response({
            "message": "like list",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })


@decorators.permission_classes([rest_permission.IsAuthenticated])
class LikeView(APIView):

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "like created",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            })
        else:
            return Response({
                "message": "like not created",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

    def delete(self, request, id=None):
        user_name = request.user
        like = Like.objects.filter(id=id, user=user_name)
        like.delete()
        return Response({
            "message": "blog unliked",
            "status": status.HTTP_200_OK
        })


@decorators.permission_classes([rest_permission.AllowAny])
class CommentGeneralView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        comment = Comment.objects.all()
        pagination = self.pagination_class()
        result = pagination.paginate_queryset(comment, request)
        serializer = CommentSerializer(result, many=True)
        return Response({
            "message": "comment list",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })


@decorators.permission_classes([rest_permission.IsAuthenticated])
class CommentView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "comment created",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            })
        else:
            return Response({
                "message": "comment not created",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

    def delete(self, request, id=None):
        user_name = request.user
        comment = Comment.objects.filter(id=id, user=user_name)
        comment.delete()
        return Response({
            "message": "comment deleted",
            "status": status.HTTP_200_OK
        })

    def patch(self, request, id=None):
        user = request.user
        comment = Comment.objects.get(id=id, user=user)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "comment updated",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            })
        else:
            return Response({
                "message": "comment not updated",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })
