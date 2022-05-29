import datetime

import jwt
from jwt import InvalidSignatureError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import User
from .serializers import UserSerializer, PostSerializer

SECRET = 'sadsadsadDSADAEDsad214323SADQ2@!$@!$%#'

def jwt_authenticate(request):
    token = request.COOKIES.get('jwt') or request.data.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    return payload



class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogInView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(f'User {email} is not found')

        elif not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')

        payload = {
            'id': user.id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

        return response

class UserView(APIView):

    def get(self, request):

        # token = request.COOKIES.get('jwt') or request.data.get('jwt')
        #
        # if not token:
        #     raise AuthenticationFailed('Unauthenticated')
        #
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.exceptions.InvalidSignatureError:
        #     raise AuthenticationFailed('Unauthenticated')
        # except jwt.exceptions.ExpiredSignatureError:
        #     raise AuthenticationFailed('Token has expired')
        payload = jwt_authenticate(request)
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PostView(APIView):

    def post(self, request):
        payload = jwt_authenticate(request)
        # user = User.objects.filter(id=payload['id']).first()
        data = request.data
        request.data['creator'] = payload['id']
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class PostLikeView(APIView):

    def post(self, request):
        payload = jwt_authenticate(request)
        # user = User.objects.filter(id=payload['id']).first()
        data = request.data
        request.data['creator'] = payload['id']
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
