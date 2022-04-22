from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from question_bank import models
from django.urls import reverse


def question_list(request):
    if request.method == 'GET':
        bid = request.GET.get('bid')
        if bid is None:
            return redirect('question_bank:bank_list')
        questions = models.Question.objects.filter(question_bank_id=bid, is_valid=True).all().order_by('sort_num')
        return render(request, 'question_list.html', {'questions': questions})


def question_add(request):
    pass


def question_change(request, pk):
    pass


def question_delete(request, pk):
    pass
