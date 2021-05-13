from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User
from . import custompermissions


class CreateUserView(generics.CreateAPIView):  # ユーザーを作成することに特化したViewを作成genericsを利用
    serializer_class = UserSerializer
    # Createなので誰でもアクセスできるように変更
    permission_classes = (permissions.AllowAny,)


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUserView(generics.RetrieveUpdateAPIView):  # 特定のオブジェクトを検索と更新ができるView
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # djangoの中でログインしているユーザーオブジェクトを返す

    def update(self, request, *args, **kwargs):  # updateができないようにしておく
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):  # ModelViewSetを継承したもの
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):  # user_profileにdjangoのUserオブジェクトを格納して作成している
        serializer.save(user_profile=self.request.user)

    def destroy(self, request, *args, **kwargs):  # 削除を無効化する、deleteはdestroyメソッドで行う
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):  # 更新を無効化する
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):  # ModelViewSetを継承したもの
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):  # 削除を無効化、deleteはdestroyメソッドで行う
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):  # 更新を無効化
        response = {'message': 'PUT method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):  # 　部分更新を無効化
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):  # ModelViewSetを継承したもの
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,
                          custompermissions.OwnerPermission,)  # 許可の設定、認証されているか

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):  # 更新を無効化
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
