from rest_framework import status
from django.http import Http404
from .models import NewUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer,UserLoginSerializer,UserSerializer,ImageupdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated'})


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            serializer = RegisterUserSerializer(newuser)
            if newuser:
                return Response({"user":serializer.data,"success": True},status=status.HTTP_201_CREATED)
        else:
            email_errors = reg_serializer.errors.get('email', [])
            if any(error.code == 'unique' for error in email_errors):
                print('error emil')
                return Response({"error": "Email is already in use" ,"success": False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(reg_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        token = response.data.get("access")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=request.data['email'], password=request.data['password'])
            if user is not None:
                login(request, user)
                serializer = UserSerializer(user)
                return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
            else:
                print('error not match')
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super(AdminLoginView, self).post(request, *args, **kwargs)
        token = response.data.get('access')
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None and user.is_superuser:
            login(request, user)
            return Response({'token': token, 'user_id': user.pk}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = NewUser.objects.filter(is_superuser=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserEditAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return NewUser.objects.get(pk=pk)
        except NewUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserSearchApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        username = request.query_params.get('username')
        print(username)
        if username:
            user = NewUser.objects.filter(username__startswith = username)
            if user:
                serializer = UserSerializer(user,many=True)
                return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return NewUser.objects.get(pk=pk)
        except NewUser.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        user.profile = request.data.get('profile')
        serializer = ImageupdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
