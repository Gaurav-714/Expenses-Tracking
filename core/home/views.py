from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *
from .models import Expense
from django.contrib.auth import authenticate, login, logout


class TrackExpense(APIView):

    def post(self, request):
        try:
            title = request.data['title']
            amount = request.data['amount']
        except KeyError:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Title and Amount are required fields.'
            })
        
        obj = Expense(user=request.user, title=title, amount=amount)
        #obj = Expense(title=title, amount=amount)
        obj.save()
        expenses = Expense.objects.filter(user = request.user).order_by('date')
        #expenses = Expense.objects.all().order_by('date')
        serializer = ExpenseSerializer(expenses, many=True)

        return Response({
            'status' : status.HTTP_201_CREATED,
            'data' : serializer.data
        })        
    

    def get(self, request):
        try:
            expenses = Expense.objects.filter(user = request.user).order_by('date')
            #expenses = Expense.objects.all().order_by('date')
            serializer = ExpenseSerializer(expenses, many=True)
            return Response({
                'status' : '200',
                'data' : serializer.data
            })
        
        except Exception as ex:
            return Response({
                'status' : status.HTTP_404_NOT_FOUND,
                'message' : 'No data available.'
            })
        

    def delete(self, request):
        srno = request.data.get('srno')
        obj = Expense.objects.get(pk=srno, user=request.user)
        obj.delete()
        return Response({
            'status' : status.HTTP_200_OK,
            'message' : 'Record deleted successfully.'
        })
    

class SignUpView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        if not username:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'error': 'Username Is Required.'
            })

        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            return Response({'message': 'Username Already Exists.'})
        
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if obj:
                return Response({
                    'status' : status.HTTP_201_CREATED,
                    'message' : 'Signed Up Successfully.',
                    'data' : serializer.data
                })

        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'error' : serializer.errors
            })


class SignInView(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'error': 'Username and Password are required fields.'
            })
        
        user_obj = User.objects.filter(username = username)
        if not user_obj.exists():
            return Response({'message' : 'Username Does Not Exists.'})
        
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user = user)
            return Response({
                'status' : status.HTTP_200_OK,
                'token': token.key,
                'message' : 'Signed In Successfully.'
            })
        else:
            return Response({
                'status' : status.HTTP_401_UNAUTHORIZED,
                'error' : 'Invalid Credentials.'
            })
    

class SignOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({
            'status': status.HTTP_200_OK,
            'message' : 'Signed Out Successfully.'
        })