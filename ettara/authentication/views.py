from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import *
import random
from django.shortcuts import get_object_or_404
import datetime
from .security import create_token,decrypt_token,create_html_template
from django.core.mail import send_mail
from rest_framework.response import Response

# Create your views here.

@api_view(['POST'])
@csrf_exempt
def login_user(request):
    username=request.POST['uname']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is None:
        return JsonResponse({'mssg':'Incorrct Credentials','status':0},status=400)
    else:
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return JsonResponse(
            data={
                'access':str(access)
            },
            status=200
        )



@api_view(['POST'])
@csrf_exempt
def register_user(request):
    username=request.POST['uname']
    password1=request.POST['password1']
    password2=request.POST['password2']

    if password1==password2: #both passwords match
        name=request.POST['name']
        country=request.POST['age']
        mobile=request.POST['mobile']
        email=request.POST['email']
        city=request.POST['city']
        state=request.POST['state']
        pin=request.POST['pin']
        address=request.POST['address']
        age=request.POST['age']

        if 'company' in request.POST:
            company=request.POST['company']
        else:
            company=None

        try:
            new_user=User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            new_user.save()
            # creation of access token
            refresh=RefreshToken.for_user(new_user)
            access=refresh.access_token
            # print(f"=========\n{str(access)}\n========")

            profile=Profile()
            profile.user=new_user
            profile.name=name
            profile.age=age
            profile.mobile=mobile
            profile.company=company
            profile.country=country
            profile.city=city
            profile.state=state
            profile.pin=pin
            profile.address=address
            profile.save()
        
            payload={
                'email':email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
                'user_id':new_user.id

            }
            html=create_html_template(payload)
            send_mail(
                'Email Verification  ettara',
                    ' ', 
                settings.EMAIL_HOST_USER,
                [email], 
                html_message=html
                )

            return JsonResponse(
                {
                    'mssg':"Profile created Successfully...",
                    'status':True,
                    'access_token':str(access)
                },
                status=201
            )

        except:
            return JsonResponse(
                {
                    'mssg':f"Try a different username... '{username}' is already taken ",
                    'status':False
                },
                status=400
            )
    else:
        return JsonResponse(
            data={
                'mssg':"Passwords Dont Match ... Try Again",
                'status':False
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
            )
    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method=='POST':
        old=request.POST['old_password']
        new=request.POST['new_password']
        user=request.user
        if user.check_password(old): #if old password is correct
            user.set_password(new)
            user.save()
            access=str(RefreshToken.for_user(user).access)
            print(f"\n\n{access}\n\n")
            return JsonResponse({
                'status':True,
                'message':"Password Changed Successfully....",
                'new_access_token':access

            },
            status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse(
                {
                    'status':False,
                    'message':"Incorrect Previous Password.."
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        

@csrf_exempt
@api_view(["POST"])     
def forgot_password(request):
    email=request.POST['email_of_user']
    user=get_object_or_404(User,email=email)
    otp=str(random.randint(100000,999999))
    print(otp)
    payload = {
        'user_id': user.id,
        'email': user.email,
        'otp': otp,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    token=create_token(payload)

    return JsonResponse({
        'otp':otp,
        'token':token
    },safe=False,status=200)


@csrf_exempt
@api_view(['POST'])
def check_otp(request):
    otp=request.POST['otp']
    enc_token=request.POST['token']
    data=decrypt_token(enc_token)
    if data['status']:
        otp_real=data['payload']['otp']
        if otp==otp_real:
            email=data['payload']['email']
            user=User.objects.get(email=email)
            access_token=str(RefreshToken.for_user(user).access_token)

            return JsonResponse(
                {
                    'access_token':access_token,
                    'status':True,
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse({
                'message':'OTP didnt matched....'
            },status=400)
            
    else:
        return JsonResponse({
            'message':'OTP expired...Try Again!!',
            'status':False
        },
        status=status.HTTP_400_BAD_REQUEST
        )
    

@csrf_exempt
@api_view(['POST'])
def verify_mail(request):
    enc_token=request.POST['token']
    data=decrypt_token(enc_token)
    if data['status']:
        payload=data['payload']
        id=payload['user_id']
        user_profile=Profile.objects.get(user__id=id)
        user_profile.email_verified=True
        user_profile.save()
        return HttpResponseRedirect('https://ettarracoffee.in/')
    else:
        return HttpResponseRedirect('< Url of Page showing Verified Link Has Expired>')


@csrf_exempt
@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def create_new_verification_message(request):
    user=request.user
    payload={
        'email':user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
        'user_id':user.id

    }
    html=create_html_template(payload)
    send_mail(
        'Email Verification  ettara',
            ' ', 
        settings.EMAIL_HOST_USER,
        [user.email], 
        html_message=html
        )
    return JsonResponse({'status':True,'mssg':f'Verification Link Sent to {user.email}'})

