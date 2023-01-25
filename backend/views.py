import random
from re import M
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from rest_framework.generics import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Users_Loan_Approval import Predicting_Loan
from .settings import CSV_ROOT
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .serializer import *

class Get_User_Input(APIView):
    def post(self,request):
            data = request.data
            print(data)
            new_list = [data[i] for i in data.keys()]
            print(new_list)
            user = Predicting_Loan(CSV_ROOT,new_list)
            
            return Response(user.Predict_Result(), status=status.HTTP_200_OK)
