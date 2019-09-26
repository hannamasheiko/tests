from django.shortcuts import get_object_or_404
from .forms import TestForm, CommentForm
from django.utils import timezone
from .models import Test, Question, Answer, Score
from django.db.models import Q
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import inlineformset_factory
import json


def add_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()

            return redirect('test_list')
    else:
        form = TestForm()
    return render(request, 'tests/add_test.html', {'form': form})


def tests_list(request):
    tests = Test.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    query = request.GET.get("q")
    if query:
        tests = tests.filter(
            Q(title__icontains=query)
        ).distinct()
    paginator = Paginator(tests, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'tests': tests,
        "object_list": queryset,
        "title": " List",
        "page_request_var": page_request_var,
    }

    return render(request, 'tests/tests_list.html', context)


def test_filter(request):
    tests = Test.objects.all()
    y = []
    for t in tests:
        maintenances = t.scores.filter(user=request.user).all()
        if maintenances.exists():
            all_scores = maintenances.all()
            for a in all_scores:
                y.append(a.test.id)

        result = list(set(y))
    test_l = []
    for r in result:
        test = Test.objects.get(pk=r)
        test_l.append(test)

    return render(request, 'tests/test_filter.html', {"tests": test_l})


def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.test = test
            comment.author = request.user
            comment.save()
            return redirect('test_detail', pk=pk)
    else:
        form = CommentForm()
    test_count = test.scores.count()

    context = {'test': test, 'form': form, 'test_count': test_count}

    return render(request, 'tests/test_detail.html', context)


def add_questions(request, test_id):
    test = Test.objects.get(pk=test_id)
    QuestionFormSet = inlineformset_factory(Test, Question, fields=('question_text',), extra=5)

    if request.method == "POST":
        formset = QuestionFormSet(request.POST, instance=test)
        if formset.is_valid():
            formset.created_date = timezone.now()
            formset.save()

            return redirect('add_questions', test_id=test.pk)

    formset = QuestionFormSet(instance=test)
    return render(request, 'tests/add_questions.html', {'formset': formset})


def questions_list(request, test_id):
    questions = Question.objects.filter(test=test_id)

    return render(request, 'tests/questions_list.html', {'questions': questions})


def add_answers(request, question_id, test_id):
    question = Question.objects.get(pk=question_id)
    AnswerFormSet = inlineformset_factory(Question, Answer, fields=('answer', 'accepted'), extra=4, max_num=4)

    if request.method == "POST":
        aformset = AnswerFormSet(request.POST, instance=question)
        if aformset.is_valid():
            aformset.created_date = timezone.now()
            aformset.save()

            return redirect('questions_list', test_id=question.test.pk)

    aformset = AnswerFormSet(instance=question)
    return render(request, 'tests/add_answers.html', {'aformset': aformset})


def test_pass(request, test_id):
    questions = Question.objects.filter(test=test_id)
    count_questions = Question.objects.filter(test=test_id).count()
    response_data = {}
    if request.method == "POST":
        lists = request.POST.get('list')
        answ = json.loads(lists)
        print(answ)
        print(type(answ))
        right = 0
        wrong = 0
        for a in answ:
            print(a)
            question_id_s = a.get('question_id')
            print(question_id_s)
            print(question_id_s.split('_'))
            question_id = question_id_s.split('_')[1]
            print(question_id)
            answer_id = a.get('choice_id')
            answer = Answer.objects.filter(pk=answer_id).values('accepted')
            print(answer)
            for ans in answer:
                if ans['accepted']:
                    right += 1
                else:
                    wrong += 1
        print('right', right)
        print('wrong', wrong)

        percent = (right * 100) / count_questions
        print(percent)
        test = Test.objects.get(pk=test_id)
        score = Score(user=request.user, test=test, count_right=right, count_wrong=wrong,
                      percentage_correct_answers=percent)
        score.save()
        result_test = {
            'right': right,
            'wrong': wrong,
            'percent': percent
        }

    return render(request, 'tests/test_pass.html', {'questions': questions, 'test_id': test_id})


def test_result(request, test_id):
    score = Score.objects.filter(test=test_id, user=request.user).last()
    result_test = {
        'right': score.count_right,
        'wrong': score.count_wrong,
        'percent': score.percentage_correct_answers
    }
    return render(request, 'tests/test_result.html', {'result_test': result_test})


def add_comment_to_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.test = test
            comment.save()
            return redirect('add_comment_to_test', test_id=test.pk)
    else:
        form = CommentForm()
    return render(request, 'tests/add_comment_to_test.html', {'form': form})
