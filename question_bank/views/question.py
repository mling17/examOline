from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from question_bank import models
from django.urls import reverse
from utils.pagination import Pagination
from django.conf import settings
from question_bank.forms.question import QuestionAddModelForm, QuestionEditModelForm
from django.db import transaction
from utils.urls import memory_reverse


def question_list(request):
    if request.method == 'GET':
        bid = request.GET.get('bid')
        if bid is None:
            return redirect('question_bank:bank_list')
        questions = models.Question.objects.filter(question_bank_id=bid, is_valid=True).all().order_by('type',
                                                                                                       'sort_num')
        all_count = questions.count()
        query_params = request.GET.copy()
        query_params._mutable = True
        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=settings.PER_PAGE_COUNT,
        )
        question_data_list = questions[pager.start:pager.end]
        return render(request, 'question_list.html', {'questions': question_data_list, 'pager': pager, 'bid': bid})


def create_question(request, q_type, bid):
    data = request.POST
    q_obj = models.Question()

    option_list = []
    choice_check = data.get('choice_check')
    mult_choice_check = data.getlist('mult_choice_check')
    try:
        with transaction.atomic():
            for k, v in data.items():
                if k == 'csrfmiddlewaretoken':
                    continue
                if hasattr(q_obj, k):
                    setattr(q_obj, k, v)
                else:
                    if q_type == 1 and k.startswith('choice_'):
                        opt_title = k.split('_')[-1].upper()
                        if opt_title == 'CHECK':
                            continue
                        opt_obj = models.ChoiceOptions()
                        opt_content = v.strip()
                        opt_obj.is_answer = True if opt_title == choice_check else False
                        opt_obj.title = opt_title
                        opt_obj.content = opt_content
                        opt_obj.question = q_obj
                        option_list.append(opt_obj)
                    elif q_type == 2 and k.startswith('mult_choice_'):
                        opt_title = k.split('_')[-1].upper()
                        if opt_title == 'CHECK':
                            continue
                        opt_obj = models.ChoiceOptions()
                        opt_content = v.strip()
                        opt_obj.is_answer = True if opt_title in mult_choice_check else False
                        opt_obj.title = opt_title
                        opt_obj.content = opt_content
                        opt_obj.question = q_obj
                        option_list.append(opt_obj)
                    elif q_type == 3 and k.startswith('judge_'):
                        opt_obj_a = models.ChoiceOptions(title='A', content='正确', question=q_obj, is_answer=False)
                        opt_obj_b = models.ChoiceOptions(title='B', content='错误', question=q_obj, is_answer=False)
                        if v == 'A':
                            opt_obj_a.is_answer = True
                        else:
                            opt_obj_b.is_answer = True
                        option_list.append(opt_obj_a)
                        option_list.append(opt_obj_b)
                    elif q_type == 4:
                        pass
                    else:
                        pass
            q_obj.user_id = request.session.get('user_id', 0)
            q_obj.question_bank_id = bid
            q_obj.save()
            models.ChoiceOptions.objects.bulk_create(option_list)
    except Exception as e:
        print(e)
        return False


def update_question(request, form, q_obj):
    bid = form.cleaned_data.get('question_bank', 0)
    q_type = form.cleaned_data.get('type')
    title = form.cleaned_data.get('title')
    analysis = form.cleaned_data.get('analysis')
    sort_num = form.cleaned_data.get('sort_num')
    # #####
    q_obj.question_bank_id = bid
    q_obj.type = q_type
    q_obj.title = title
    q_obj.analysis = analysis
    q_obj.sort_num = sort_num
    # #####
    opt_objs = models.ChoiceOptions.objects.filter(question=q_obj)
    choice_check = request.POST.get('choice_check')
    mult_choice_check = request.POST.getlist('mult_choice_check')
    try:
        with transaction.atomic():
            for k, v in form.data.items():
                opt_title = k.split('_')[-1].upper()
                if k.startswith('choice_') and q_type == 1:
                    if opt_title == 'CHECK':
                        continue
                    for opt_obj in opt_objs:
                        if opt_title != opt_obj.title:
                            continue
                        opt_obj.is_answer = True if opt_obj.title == choice_check else False
                        opt_obj.content = v.strip()
                        opt_obj.question = q_obj
                        opt_obj.save()
                elif k.startswith('mult_choice_') and q_type == 2:
                    if k.split('_')[-1].upper() == 'CHECK':
                        continue
                    for opt_obj in opt_objs:
                        if opt_title != opt_obj.title:
                            continue
                        opt_obj.is_answer = True if opt_obj.title in mult_choice_check else False
                        opt_obj.content = v.strip()
                        opt_obj.save()
                elif k.startswith('judge_') and q_type == 3:
                    for opt_obj in opt_objs:
                        if opt_obj.title == form.data.get('judge_check'):
                            opt_obj.is_answer = True
                        else:
                            opt_obj.is_answer = False
                        opt_obj.save()
                elif k.startswith('fill_') and q_type == 4:
                    pass
                else:
                    pass
            q_obj.save()
    except Exception as e:
        print(e)
        return False


def question_add(request):
    bid = request.GET.get('bid', 0)
    if not models.QuestionBank.objects.filter(id=bid).exists():
        return HttpResponse('err')
    if request.method == 'GET':
        form = QuestionAddModelForm()
        return render(request, 'question_change.html', {'form': form})
    form = QuestionAddModelForm(request.POST)
    if form.is_valid():
        q_type = form.cleaned_data.get('type')
        result = create_question(request, q_type, bid)
        if result is False:
            return HttpResponse('err')
        url = reverse('question_bank:question_list') + f'?bid={bid}'
        return redirect(url)

    return render(request, 'question_change.html', {'form': form})


def question_change(request, pk):
    q_obj = models.Question.objects.filter(id=pk).first()
    if not q_obj:
        return HttpResponse('err')
    if request.method == 'GET':
        form = QuestionEditModelForm(instance=q_obj)
        return render(request, 'question_change.html', {'form': form, 'q_id': pk})
    form = QuestionEditModelForm(instance=q_obj, data=request.POST)
    if form.is_valid():
        result = update_question(request, form, q_obj)
        if result is False:
            return HttpResponse('err')
        return redirect(memory_reverse(request, 'question_bank:question_list'))
    return render(request, 'change.html', {'form': form})


def question_delete(request, pk):
    origin_list_url = memory_reverse(request, 'question_bank:question_list')
    if request.method == 'GET':
        return render(request, 'bank_delete.html', {'cancel': origin_list_url})
    models.Question.objects.filter(pk=pk).update(is_valid=False)
    return redirect(origin_list_url)


def get_question_options(request):
    response = {'status': 'success'}
    if request.method == 'GET':
        qid = int(request.GET.get('q_id'), 0)
        result = models.ChoiceOptions.objects.filter(question_id=qid).values('title', 'content', 'is_answer')
        data = []
        for obj_dic in result:
            data.append(obj_dic)
        response['data'] = data
        return JsonResponse(response, safe=True)
