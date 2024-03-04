from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExpenseSerializer
from .models import Expense


class TrackExpense(APIView):

    def post(self, request):
        title = request.data.get('title')
        amount = request.data.get('amount')
        #obj = Expense(user=request.user, title=title, expense=expense)
        obj = Expense(title=title, amount=amount)
        obj.save()

        #expenses = request.objects.filter(user = request.user).order_by('date')
        expenses = Expense.objects.all().order_by('date')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response({
            'status' : '200',
            'data' : serializer.data
        })        
    
    def get(self, request):
        #expenses = request.objects.filter(user = request.user).order_by('date')
        expenses = Expense.objects.all().order_by('date')
        serializer = ExpenseSerializer(expenses)
        return Response({
            'status' : '200',
            'data' : serializer.data
        }) 