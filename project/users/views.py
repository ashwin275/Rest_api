from rest_framework.views import APIView
from .serializers import UserSeriliazer,UserLIstSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
import jwt , datetime
from rest_framework.exceptions import NotFound
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
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
           
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            user = CustomUser.objects.get(id=payload['id'])
            if user.is_superuser:
                raise AuthenticationFailed('you are an admin !')
            else:
                serializer = UserSeriliazer(user)
                return Response(serializer.data)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        except (jwt.DecodeError, CustomUser.DoesNotExist):
            raise AuthenticationFailed('Unauthenticated!')

    


class Logoutview(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')

        response.data = {
            'message':'sucess'
        }

        return response
    

class UserListview(APIView):
    def get(self,request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
           
            token = token.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            user = CustomUser.objects.get(id=payload['id'])
            print(user.is_superuser,'admin')
            
            serializer = None
            if user.is_superuser:
                UserList = CustomUser.objects.exclude(id = user.id)
                serializer = UserLIstSerializer(UserList,many=True)
            else:
                raise AuthenticationFailed('your are not a superuser')

            if serializer:
                return Response(serializer.data)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        except (jwt.DecodeError, CustomUser.DoesNotExist):
            raise AuthenticationFailed('Unauthenticated!')


class UserEditView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise NotFound('User not found')
        

    def delete(self,pk):
       
        user = self.get_object(pk)
        user.delete()
        return Response({'message':'user deleted Succesfully'})

