from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user=User.objects.get(username=serializer.data['username'])
                token_obj= Token.objects.create(user=user)
                return Response({
                    'status':'Success',
                    'message':'data',
                    'token':str(token_obj),
                    'data':serializer.data
                })
            return Response({
                'status':'Failure',
                'message':'error',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'error',
                'data':serializer.errors
            })

class VerifyOtp(APIView):
    def post(self,request):
        try:
            data=request.data
            profile_obj=Profile.objects.get(user__username=data.get('username'))
            if profile_obj.token==data.get('otp'):
                profile_obj.is_active=True
                profile_obj.save()
                return Response({
                    'status':True,
                    'message':'Correct Otp',
                    'data':{}
                })
            return Response({
                'status':False,
                'message':'Wrong Otp',
                'data':{}
            })
        except Exception as e:
            print(e)

class GetAllData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        all=Profile.objects.all()
        serializer=ProfileSerialiser(all,many=True)
        return Response({
            'status':200,
            'message':'Success',
            "data":serializer.data
        })


from django.http import HttpResponse


def verify_email(request , token):
    obj = Profile.objects.filter(token = token)

    if obj.exists():
        obj = obj[0]
        obj.is_active = True
        obj.save()
        return HttpResponse('Your account activated')
    
    return HttpResponse('Invalid token')