from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ExpenseSerializer
from .models import Expense
from .serializers import User, UserSerializer
from django.contrib.auth import authenticate, login, logout

class TrackExpense(APIView):

    def post(self, request):
        title = request.data['title']
        amount = request.data['amount']
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

        username = User.objects.filter(username = request.data.get('username'))
        if username.exists():
            return Response({'message' : 'Username Already Exists.'})
        
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
            'Error' : serializer.errors
            })


class SignInView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user_obj = User.objects.filter(username = username)
        if not user_obj.exists():
            return Response({'message' : 'Username Does Not Exists.'})
        
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return Response({
                'status' : status.HTTP_200_OK,
                'message' : 'Signed In Successfully.'
            })
        
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