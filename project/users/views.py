from rest_framework.views import APIView
from .serializers import UserSeriliazer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
import jwt , datetime
# Create your views here.


class RegisterView(APIView):
    def post(self,request):
        serializer = UserSeriliazer(data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorect password')
        

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        

        token = jwt.encode(payload,'secret',algorithm='HS256')
        
        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'message':'success',
            'jwt':token
        }
        
        
        return response
    


class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')


        return Response(token)
