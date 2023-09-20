from django.shortcuts import render
from rest_framework.permissions import  IsAdminUser, AllowAny # IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import  News, Admins
# from rest_framework_simplejwt.token import RefreshToken, AccessToken
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from .serializers import (NewsSerializer,  PlaceNewsSerializer,CategoryNewsSerializer,
                          AdminSerializer, AdminLoginSerializer, OneAdminSerializer,
                          PlaceAdminSerializer, CategoryAdminSerializer)
# ,, , ,
#                           )
from datetime import datetime
import os


# Create your views here.
class GetAllNewsView(APIView):
    queryset = News.objects.all()
    serializer = NewsSerializer
    # permission_classes = [AllowAny,]

    def get(self, request, language):
        news = News.objects.filter(language=language)
        if news:
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        else:
            return Response("Bunday xabar mavjud emas")


class PostNewsView(APIView):
    queryset = News.objects.all()
    serializer = NewsSerializer()
    permission_classes = [AllowAny,]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=NewsSerializer)
    def post(self, request):
        serializer = NewsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            print(True)
            id = request.data.get('creted_by')
            try:
                admin = Admins.objects.get(id=id)
                admin.count_news += 1
                admin.save()
                print(admin.count_news)
            except Admins.DoesNotExist:
                return Response({"error": "Admin not found"}, status=404)
            print("sss")
            return Response({
                "MSG":"Success",
                "data":serializer.data
            })
        else:
            return  Response(serializer.errors)


class PlaceNewsView(APIView):
    queryset = News.objects.all()
    serializer = PlaceNewsSerializer
    # permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=PlaceNewsSerializer)
    def post(self, request):
        place = request.data.get('place')
        news = News.objects.filter(place=place)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class CategoryNewsView(APIView):
    queryset = News.objects.all()
    serializer = CategoryNewsSerializer
    # permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=CategoryNewsSerializer)
    def post(self, request):
        category = request.data.get('category')
        news = News.objects.filter(category=category)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

class GetOneNewsView(APIView):
    queryset = News.objects.all()
    # serializer = OneNewsSerializer
    # permission_classes = [AllowAny, ]

    # @swagger_auto_schema(request_body=OneNewsSerializer)
    def get(self, request, pk):
        # id = request.data.get('id')
        news = News.objects.filter(id=pk)
        if news:
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)
        else:
            return Response("Bunday xabar mavjud emas")

class GetOneAdmin(APIView):
    queryset = Admins.objects.all()
    serializer = OneAdminSerializer()
    permission_classes =[IsAdminUser, ]

    @swagger_auto_schema(request_body=OneAdminSerializer)
    def post(self, request):
        name = request.data.get('name')
        admin = Admins.objects.filter(name = name).first()
        serializer = AdminSerializer(admin)
        return Response({
            "MSG":"Success",
            "data":serializer.data
        })
#
class PostOneAdmin(APIView):
    queryset = Admins.objects.all()
    serializer = AdminSerializer()
    permission_classes = [IsAdminUser, ]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=AdminSerializer)
    def post(self, request):
        serializer = AdminSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({
                "MSG":"Success",
                "data":serializer.data
            })
        else:
            return  Response(serializer.errors)
#
class PalceGetAdmin(APIView):
    queryset = Admins.objects.all()
    serializer = PlaceAdminSerializer()
    permission_classes = [IsAdminUser, ]

    @swagger_auto_schema(request_body=PlaceAdminSerializer)
    def post(self, request):
        place = request.data.get('place')
        admin = Admins.objects.filter(place=place).first()
        serializer = AdminSerializer(admin)
        return Response({
            "MSG": "Success",
            "data": serializer.data
        })
#
class GetAdminCategoryView(APIView):
    queryset = Admins.objects.all()
    serializer = CategoryAdminSerializer()
    permission_classes = [IsAdminUser, ]

    @swagger_auto_schema(request_body=CategoryAdminSerializer)
    def post(self, request):
        job_category = request.data.get('job_category')
        admin = Admins.objects.filter(job_category = job_category).first()
        serializer = AdminSerializer(admin)
        return  Response({
            "MSG":"Success",
            'data':serializer.data
        })
#
class LoginView(APIView):
    queryset = Admins.objects.all()
    serializer = AdminLoginSerializer()
    permission_classes = [AllowAny,]

    @swagger_auto_schema(request_body=AdminLoginSerializer)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = Admins.objects.get(username=username, password=password)
        except Admins.DoesNotExist:
            return Response("Bunday foydalanuvchi topilmadi")
        serializers = AdminLoginSerializer(user)
        return Response({
            "MSG":"Success",
            'data':serializers.data
        })

#
# # for delete old news automatic
# class DeleteNews(APIView):
#     queryset = News.objects.all()
#     serializer = NewsSerializer()
#
#     def delete(self):
#         news = News.objects.first()
#         if news is not None:
#             news_month = news.created_at.strftime("%m")
#             current_month = datetime.now().strftime("%m")
#             if news_month < current_month:
#                 news.delete()
#                 return Response("News deleted successfully.")
#         return Response("No news to delete or it's not the right time to delete.")
#
#