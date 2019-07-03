# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
from random import random, uniform

from django.template import RequestContext
from django.core import serializers
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Coalesce
from django.db.models import F, FloatField
from django.core import serializers

from .models import ConfigFail, User, Category, Product, TimeRate, Basket, Currency, Language, ShippingAddress

n_el = 12


def get_logged_user(request, user_name="notLogged"):
    if user_name in "notLogged":
        user = User(isLogged=False, Username="notLogged")
        user_name = request.COOKIES.get("username", user_name)
    if "notLogged" not in user_name:
        user = User.objects.filter(Username=user_name)
        if user.count() != 0:
            user = user[0]
    return user


def get_referer_op(_request):
    ret = QueryDict("op=index")
    try:
        referer = _request.META.get('HTTP_REFERER', "?op=index&")
        ret = QueryDict(referer.split("?")[1])
    except Exception as e:
        print(e)
    return ret


def get_param(request, param_refer, param, default='index'):
    ret = default
    try:
        if len(request.GET) > 0:
            ret = request.GET.get(param, default)
        else:
            ret = param_refer.get(param, default)
    except Exception as e:
        print("Not found param: ", param, e)
    return ret


def get_rate_time(_id):
    r = random()
    times = TimeRate.objects.filter(ID_ConfigFail=_id).filter(TimeRate__gte=r).order_by('TimeRate')
    if len(times) == 0:
        sleep = 0
    else:
        sleep = uniform(times[0].TimeMin, times[0].TimeMax)
    return sleep


def set_login(user, _id_user):
    count_basket = 0
    sum_basket: int = 0
    currency = Currency.objects.all()
    language = Language.objects.all()
    basket = {}
    tax_basket = 0
    shipping_basket = 0
    total_basket = 0
    subtotal_basket = 0
    json_basket = {}
    if user.isLogged:
        cls = "is-logged"
        name = user.Name
        cur = {'name': user.ID_Currency.Name, 'symbol': user.ID_Currency.Symbol}
        lng = {'name': user.ID_Language.Name, 'symbol': user.ID_Language.Symbol}
        basket = Basket.objects.select_related().filter(ID_User=_id_user)
        sum_basket = (basket.aggregate(sum=Coalesce(Sum((F('ID_Product__Price')*(100-F('ID_Product__Sale')))),0, output_field=FloatField()))['sum'])/100
        count_basket = basket.aggregate(sum_qty=Coalesce(Sum('Quantity'), 0))['sum_qty']
        tax_basket = sum_basket * 0.1
        shipping_basket = count_basket * 1.5
        subtotal_basket = sum_basket - tax_basket
        total_basket = sum_basket + shipping_basket
    else:
        cls = "no-logged"
        name = ""
        _currency = Currency.objects.filter(In_Use=True)[0]
        _language = Language.objects.filter(In_Use=True)[0]
        cur = {'name': _currency.Name, 'symbol': _currency.Symbol}
        lng = {'name': _language.Name, 'symbol': _language.Symbol}
    json_currency = json.loads(serializers.serialize("json", currency))
    json_language = json.loads(serializers.serialize("json", language))
    json_basket = json.loads(serializers.serialize("json", basket, use_natural_foreign_keys=True, use_natural_primary_keys=True))
    return json.dumps({"is_logged": user.isLogged, "class": cls, "name": name, 'currency': cur, 'language': lng, 'subtotal_basket': subtotal_basket, 'tax_basket': tax_basket, 'shipping_basket': shipping_basket, 'total_basket': total_basket, 'sum_basket': str(sum_basket), 'count_basket': str(count_basket), 'curs': json_currency, 'lngs': json_language, 'basket': json_basket})


def dev_post(request, user):
    r = random()
    ret = {'res': 0, 'mess': "", 'username': user.Username}
    id_user = user.ID
    print(id_user)
    if len(request.POST) > 0:
        op = request.POST['op']
        print(op)
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        elif op == "login":
                _user = request.POST['username']
                user = User.objects.filter(Username=_user)
                if user.count() == 0:
                    ret = {'res': 2, 'mess': "USER NOT FOUND"}
                    return json.dumps(ret)
                else:
                    user = user[0]
                user.isLogged = 1
                user.save()
                ret['username'] = user.Username
        elif op == "logout":
                user.isLogged = 0
                user.save()
                ret['username'] = "notLogged"
        elif op == "addBasket":
            id_prod = request.POST['id']
            qty = int(request.POST['qty'])
            basket = Basket(ID_Product_id=id_prod, ID_User_id=id_user, Quantity=qty)
            basket.save()
        elif op == "removePrd":
            id_prd = request.POST['id']
            Basket.objects.filter(ID=id_prd).delete()
        elif op == "setCurrency":
            id_cur = request.POST['id_cur']
            if user.isLogged:
                user.ID_Currency = Currency.objects.filter(ID=id_cur)[0]
                user.save()
            else:
                Currency.objects.all().update(In_Use=False)
                Currency.objects.filter(ID=id_cur).update(In_Use=True)
        elif op == "setLanguage":
            id_lng = request.POST['id_lng']
            if user.isLogged:
                user.ID_Language = Language.objects.filter(ID=id_lng)[0]
                user.save()
            else:
                Language.objects.all().update(In_Use=False)
                Language.objects.filter(ID=id_lng).update(In_Use=True)
        elif op == "createAccount":
            username = request.POST['username']
            lastname = request.POST['lastname']
            name = request.POST['name']
            address = request.POST['address']
            email = request.POST['email']
            password = request.POST['password']
            rpassword = request.POST['rpassword']
            if password != rpassword:
                ret = {'res': 2, 'mess': "PASSWORD DO NOT MATCH"}
                return json.dumps(ret)
            user = User(Username=username, Lastname=lastname, Name=name, Address=address, Mail=email, Password=password, isLogged=True)
            user.save()
        elif op == "saveAddress":
            try:
                id_address = request.POST['id']
                if not id_address:
                    ad = ShippingAddress()
                else:
                    ad = ShippingAddress.objects.filter(ID=int(id_address))[0]
                ad.Firstname = request.POST['firstname']
                ad.Lastname = request.POST['lastname']
                ad.Company = request.POST['company']
                ad.Street = request.POST['street']
                ad.City = request.POST['city']
                ad.Zip = request.POST['zip']
                ad.State = request.POST['state']
                ad.Phone = request.POST['phone']
                ad.Province = request.POST['province']
                ad.Mail = request.POST['email']
                ad.save()
            except Exception as e:
                print(e)
        time.sleep(get_rate_time(fail.ID))
    return json.dumps(ret)


@csrf_exempt
def index(request):
    query_filter = "op=index"
    user = get_logged_user(request)
    id_user = user.ID
    ret = {'res': 0, 'mess': ""}
    r = random()
    prods = Product.objects.all()
    refer = get_referer_op(request)
    op = get_param(request, refer, 'op')
    print(request.method)
    print(request.POST)
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        op = get_param(request, refer, 'op', 'index')
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        elif op == "filter":
            filter_prods = Product.objects.filter(ID_Category__Name="aaaaaa")
            cat = get_param(request, refer, 'cat')
            tags = get_param(request, refer, 'tags')
            if cat == "All":
                _filter_prods = Product.objects.all()
            else:
                _filter_prods = Product.objects.filter(ID_Category__Name=cat)
            if tags == "":
                filter_prods = _filter_prods
            else:
                for tag in tags.split(" "):
                    filter_prods = filter_prods | _filter_prods.filter(Desc__icontains=tag)
            query_filter = "op=filter&cat={}&tags={}".format(cat, tags)
            prods = filter_prods
        time.sleep(get_rate_time(fail.ID))
    page = int(get_param(request, refer, 'page', 1))
    data_user = set_login(user, id_user)
    cats = Category.objects.all()
    data_cats = serializers.serialize("json", cats)
    data_prods = serializers.serialize("json", prods[(page - 1) * n_el:page * n_el])
    
    response = render(
        request,
        'index.html',
        context=(
            {'fail': ret, 'user': json.loads(data_user), 'cats': json.loads(data_cats), 'prods': json.loads(data_prods), 'n_el': int((len(prods) / 12) + 1), 'page': {'n_page' : page, 'query_filter': query_filter}}),
    )
    response.set_cookie('username', user.Username)
    return response


@csrf_exempt
def saveAddress(request):
    ret = {'res': 0, 'mess': ""}
    try:
        user = get_logged_user(request)
        id_user = user.ID
        r = random()
        refer = get_referer_op(request)
        op = get_param(request, refer, 'op')
        if request.method == 'POST':
            ret = json.loads(dev_post(request, user))
            if ret['res'] < 2:
                username = ret['username']
                user = get_logged_user(request, username)
                id_user = user.ID
        if request.method == 'GET' or "-1" not in op:
            op = get_param(request, refer, 'op')
            data_user = set_login(user, id_user)
            fail = ConfigFail.objects.filter(Name=op)[0]
            if r < fail.FailureRateService:
                ret = {'res': 2, 'mess': fail.ErrorMessage}
            time.sleep(get_rate_time(fail.ID))
        ret['res'] = 'OKK'
        ret['mess'] = True
    except Exception as e:
        ret['mess'] = str(e)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def product(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    r = random()
    refer = get_referer_op(request)
    op = get_param(request, refer, 'op')
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        op = get_param(request, refer, 'op')
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        elif op == "product":
            id_prod = get_param(request, refer, "id")
            prod = Product.objects.filter(ID=id_prod)
        time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    data_prod = serializers.serialize("json", prod)
    tot = prod[0].Price * (100-prod[0].Sale)/100
    response = render(
        request,
        'product.html',
        context=(
            {'fail': ret, 'user': json.loads(data_user), 'prods': json.loads(data_prod), 'tot': tot}),
    )
    response.set_cookie('username', user.Username)
    return response

@csrf_exempt
def basket(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    r = random()
    refer = get_referer_op(request)
    op = "basket"
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    response = render(
        request,
        'basket.html',
        context=({'fail': ret, 'user': json.loads(data_user)}),
    )
    response.set_cookie('username', user.Username)
    return response


@csrf_exempt
def checkout_review(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    r = random()
    refer = get_referer_op(request)
    op = "checkout-review"
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    response = render(
        request,
        'checkout-review.html',
        context=({'fail': ret, 'user': json.loads(data_user)}),
    )
    response.set_cookie('username', user.Username)
    return response

@csrf_exempt
def checkout_payment(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    r = random()
    refer = get_referer_op(request)
    op = "checkout-payment"
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    ad = ShippingAddress.objects.filter(ID_User=user)
    response = render(
        request,
        'checkout-payment.html',
        context=({'fail': ret, 'user': json.loads(data_user),'ad': json.loads(serializers.serialize('json', list(ad)))}),
    )
    response.set_cookie('username', user.Username)
    return response

@csrf_exempt
def checkout_address(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    r = random()
    refer = get_referer_op(request)
    op = "checkout-address"
    if request.method == 'POST':
        ret = json.loads(dev_post(request, user))
        if ret['res'] < 2:
            username = ret['username']
            user = get_logged_user(request, username)
            id_user = user.ID
    if request.method == 'GET' or "-1" not in op:
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
            time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    ad = ShippingAddress.objects.filter(ID_User=user)
    response = render(
        request,
        'checkout-address.html',
        context=({'fail': ret, 'user': json.loads(data_user),'ad': json.loads(serializers.serialize('json', list(ad)))}),
    )
    response.set_cookie('username', user.Username)
    return response

@csrf_exempt
def place_order(request):
    r = random()
    fail = None
    ret = {'res': 0, 'mess': ""}
    user = get_logged_user(request)
    id_user = user.ID
    
    r = random()
    refer = get_referer_op(request)
    op = "place-order"
    
    if request.method == 'GET' or "-1" not in op:
        fail = ConfigFail.objects.filter(Name=op)[0]
        if r < fail.FailureRateService:
            ret = {'res': 2, 'mess': fail.ErrorMessage}
        else:
            Basket.objects.filter(ID_User=id_user).delete()
        time.sleep(get_rate_time(fail.ID))
    data_user = set_login(user, id_user)
    response = render(
        request,
        'place-order.html',
        context=({'fail': ret, 'user': json.loads(data_user)}),
    )
    response.set_cookie('username', user.Username)
    return response

@csrf_exempt
def get_fail(request):
    json_ret = {"status": "KO", "mess": -1}
    try:
        if request.method == 'GET':
            nf = request.GET['nameFail']
            vf = ConfigFail.objects.filter(Name=nf)[0].Value
            json_ret["status"] = "OK"
            json_ret["mess"] = vf
    except Exception as e:
        pass
    return HttpResponse(json.dumps(json_ret), content_type='application/json')


@csrf_exempt
def is_logged(request):
    json_ret = {"status": "KO", "mess": -1}
    try:
        if request.method == 'GET':
            lg = request.GET['logged']
            user = User.objects.filter(isLogged=True)
            if user.count() == 0:
                user = User(isLogged=False)
            else:
                user = user[0]
            if lg == "2":
                json_ret["status"] = "OK"
                json_ret["mess"] = user.isLogged
            elif lg == "1":
                user.isLogged = False
                json_ret['mess'] = 1
                user.save()
            elif lg == "0":
                user.isLogged = True
                user.save()
                json_ret["status"] = "OK"
                json_ret["mess"] = user.isLogged
    except Exception as e:
        print(e.message)
        pass

    return HttpResponse(json.dumps(json_ret), content_type='application/json')
