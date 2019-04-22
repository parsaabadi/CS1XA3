import random
import json
from urllib.parse import parse_qs

from django.shortcuts import render
from CountryCapital.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from CountryCapital.models import CountryCapitalData


def index(request):
    response = render(request, 'CountryCapital/index.html')
    response.set_cookie('id_num', '', 1 * 86400)
    response.set_cookie('curr_scores', 0, 1 * 86400)
    response.set_cookie('total_attempt', 3, 1 * 86400)
    return response


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('id_num')
    response.delete_cookie('curr_scores')
    response.delete_cookie('total_attempt')
    return response


def get_dict(string):
    dicts = {}
    lines = string.split('&')
    for l in lines:
        ls = l.split('=')
        dicts[ls[0]] = ls[1]
    return dicts

@login_required
def spellgame_next(request):
    reqmetalist = list(request.META.keys())
    if 'HTTP_REFERER' not in reqmetalist:
        response = render(request, 'CountryCapital/index.html', {
            'show': True, 'message': 'You can not copy paste url for the game or press back/reload button'
        })
        response.set_cookie('id_num', '', 1 * 86400)
        response.set_cookie('curr_scores', 0, 1 * 86400)
        response.set_cookie('total_attempt', 3, 1 * 86400)
        return response
    if request.method == 'POST':
        postData = parse_qs(request.body.decode('utf-8'))
        answer = postData['answer'][0]
        list_id = [int(i) for i in request.COOKIES['id_num'].split(',')[:-1]]
        answerobj = CountryCapitalData.objects.get(pk=list_id[-1])
        if answer.lower() == answerobj.capitals.lower():
            if int(request.COOKIES['curr_scores'])+1 == 5:
                response = render(request, 'CountryCapital/win.html', {
                    'ques': answerobj,
                    'data': postData,
                    'show': True,
                    'message': 'You won the game!!!'
                })
                response.set_cookie('id_num', '', 1 * 86400)
                response.set_cookie('curr_scores', 0, 1 * 86400)
                response.set_cookie('total_attempt', 3, 1 * 86400)
                return response
            else:
                size = CountryCapitalData.objects.all().count()
                id = random.randint(1, size)
                while id in list_id:
                    id = random.randint(1, size)
                obj = CountryCapitalData.objects.get(pk=id)
                curr_scores = int(request.COOKIES['curr_scores']) + 1
                list_id.append(id)
                list_str = [str(i) for i in list_id]
                postData['roundnumber'] = [curr_scores+1]
                postData['curr_score'] = [curr_scores]
                response = render(request, 'CountryCapital/spellcheckfirst.html', {
                    'ques': obj,
                    'data': postData,
                    'showCorrect': True,
                    'message': 'Correct Spelling, next round!!!'
                })
                response.set_cookie('id_num', ','.join(list_str)+',', 1 * 86400)
                response.set_cookie('curr_scores', curr_scores, 1 * 86400)
                response.set_cookie('total_attempt', request.COOKIES['total_attempt'], 1 * 86400)
                return response

        else:
            totalattempt = int(request.COOKIES['total_attempt']) - 1
            if totalattempt <= 0:
                return render(request, 'CountryCapital/lose.html', {
                    'show': True,
                    'message': 'You lost the game. Please retry!!!'
                })
            else:
                postData['totalattemptleft'] = [totalattempt]
                response = render(request, 'CountryCapital/spellcheckfirst.html', {
                    'ques': answerobj,
                    'data': postData,
                    'show': True,
                    'message': 'Your spelling is wrong!!!'
                })
            response.set_cookie('total_attempt', totalattempt, 1 * 86400)
            return response
    else:
        response = render(request, 'CountryCapital/index.html', {
            'show': True, 'message': 'You can not copy paste url for the game or press back button'
        })
        response.set_cookie('id_num', '', 1 * 86400)
        response.set_cookie('curr_scores', 0, 1 * 86400)
        response.set_cookie('total_attempt', 3, 1 * 86400)
        return response

@login_required
def spell_check(request):
    reqmetalist = list(request.META.keys())
    if 'HTTP_REFERER' not in reqmetalist:
        response = render(request, 'CountryCapital/index.html', {
            'show': True, 'message': 'You can not copy paste url for the game or press back/reload button'
        })
        response.set_cookie('id_num', '', 1 * 86400)
        response.set_cookie('curr_scores', 0, 1 * 86400)
        response.set_cookie('total_attempt', 3, 1 * 86400)
        return response
    if request.method == 'POST':
        print(request.body.decode('utf-8'))
        postData = parse_qs(request.body.decode('utf-8'))

        print(postData)
        size = CountryCapitalData.objects.all().count()
        id = random.randint(1, size)
        list_id = [int(i) for i in request.COOKIES['id_num'].split(',')[:-1]]
        while id in list_id:
            id = random.randint(1, size)
        print(id)
        obj = CountryCapitalData.objects.get(pk=id)
        list_id.append(id)
        list_str = [str(i) for i in list_id]
        response = render(request, 'CountryCapital/spellcheckfirst.html', {
            'ques': obj,
            'data': postData
        })
        response.set_cookie('id_num', ','.join(list_str)+',', 1*86400)
        response.set_cookie('curr_scores', 0, 1 * 86400)
        response.set_cookie('total_attempt', 3, 1 * 86400)
        return response
    else:
        response = render(request, 'CountryCapital/index.html', {
            'show': True, 'message': 'You can not copy paste url for the game or press back/reload button'
        })
        response.set_cookie('id_num', '', 1 * 86400)
        response.set_cookie('curr_scores', 0, 1 * 86400)
        response.set_cookie('total_attempt', 3, 1 * 86400)
        return response


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'CountryCapital/registration.html',
                          {'user_form': user_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            response = render(request, 'CountryCapital/login.html', {'show': True, 'message': 'Wrong username or '
                                                                                           'password'})
            return response
    else:
        return render(request, 'CountryCapital/login.html', {})
