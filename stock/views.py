import datetime
import datetime
import json
import math
import re
from itertools import islice

import matplotlib.pyplot as plt
import tushare as ts
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.

plt.rcParams['font.sans-serif'] = ['SimHei']   # 用来正常显示中文标签
ts.set_token('f281dbc422d80e2350e94b1878bd3b86971de985641877fc42ccd836')
pro = ts.pro_api()
from stock.models import Stock, Mystock, Condition_Sheet

def showinfo(request):
    global df
    stock = Stock.objects.all().order_by('code')
    json_data=serializers.serialize('json',stock)
    json_data=json.loads(json_data)
    data=[]
    for i in json_data:
        data.append(i['fields'])
    return render(request, 'stock/showinfo.html',{'rep': data})


def showdetail(request):
    def check_date(date):
        if date.month < 10:
            month = '0' + str(date.month)
        else:
            month = str(date.month)
        if date.day < 10:
            day = '0' + str(date.day)
        else:
            day = str(now.day)
        return str(date.year)+month+day
    code=request.GET.get("code")
    method=request.GET.get("method")
    now=datetime.datetime.today()

    if method == 'daily':
        start = now - datetime.timedelta(days=150)
        start=check_date(start)
        now=check_date(now)
        df = pro.daily(ts_code=code, start_date=start, end_date=now)
        #得到股票数据
    elif method == 'weekly':
        start = now - datetime.timedelta(days=365 * 2)
        start = check_date(start)
        now = check_date(now)
        df = pro.weekly(ts_code=code, start_date=start, end_date=now)
    elif method == 'monthly':
        start = now - datetime.timedelta(days=365 * 9)
        start = check_date(start)
        now = check_date(now)
        df = pro.monthly(ts_code=code, start_date=start, end_date=now)
    else:
        return HttpResponse('没有找到相关数据！')
    json_data=df.to_json(orient="records", force_ascii=False)
    json_data = json.loads(json_data)
    list=[]
    volume = []
    dates=[]

    for item in json_data:
        open= item['open']
        close = item['close']
        low = item['low']
        high = item['high']
        volume_list=item['vol']
        item_list=[open,close,low,high]
        list.append(item_list)
        volume.append(volume_list)

        date=item['trade_date']
        date=date[:4]+'-'+date[4:6]+'-'+date[6:8]
        dates.append(date)

    list.reverse()
    dates.reverse()
    volume.reverse()

    #股票分析模块
    result = ''
    key = dict()
    analysis=pro.daily_basic(ts_code=code).to_json(orient="records")
    analysis=json.loads(analysis)[0]

    turnover=analysis['turnover_rate']
    volume_ratio=analysis['volume_ratio']
    pe=analysis['pe']



    grade=0
    if turnover is None:
        result = [None, 0]
        key['turnover'] = result
    else:
        turnover = float(turnover)
        if turnover < 1:
            result='流动性很差'
            grade=1
        elif turnover>=1 and turnover<2:
            result = '成交低靡'
            grade = 2
        elif turnover >= 2 and turnover < 3:
            result = '成交温和'
            grade = 3
        elif turnover >= 3 and turnover < 5:
            result = '成交活跃'
            grade = 4
        elif turnover >= 5 and turnover < 8:
            result = '成交大量'
            grade = 5
        elif turnover >= 8 and turnover < 15:
            result = '成交放量'
            grade = 6
        elif turnover >= 15 and turnover < 25:
            result = '成交巨量'
            grade = 7
        elif turnover >= 25:
            result = '成交怪异'
            grade = 8
        result = [result, grade]
        key['turnover'] = result



    grade = 0
    if volume_ratio is None:
        result = [None, 0]
        key['volume_ratio'] = result
    else:
        volume_ratio = float(volume_ratio)
        if volume_ratio < 0.8:
            result = '成交量低于正常水平'
            grade = 1
        elif volume_ratio >= 0.8 and volume_ratio < 1.5:
            result = '成交量处于正常水平'
            grade = 2
        elif volume_ratio >= 1.5 and volume_ratio < 2.5:
            result = '成交量温和放量'
            grade = 3
        elif volume_ratio >= 2.5 and volume_ratio < 5:
            result = '成交量明显放量'
            grade = 4
        elif volume_ratio >= 5 and volume_ratio < 10:
            result = '成交量剧烈放量'
            grade = 5
        elif volume_ratio >= 10 and volume_ratio < 20:
            result = '考虑反向操作'
            grade = 6
        elif volume_ratio >= 20:
            result = '成交量极端放量'
            grade = 7
        result = [result, grade]
        key['volume_ratio'] = result

    grade = 0
    if pe is None:
        result = [None, 0]
        key['pe'] = result
    else:
        pe = float(pe)
        if pe < 0:
            result = '公司盈利为负'
            grade = 1
        elif pe >= 0 and pe < 13:
            result = '价值被低估'
            grade = 2
        elif pe >= 13 and pe < 20:
            result = '价值处于正常水平'
            grade = 3
        elif pe >= 20 and pe < 28:
            result = '价值被高估'
            grade = 4
        elif pe >= 28:
            result = '较高的泡沫性'
            grade = 5
        result = [result, grade]
        key['pe'] = result


    #日期错误
    #申请接口得到的数据是时间倒序的
    return render(request, 'stock/detail.html', {'code': code,'dates':dates,'data':list,'volumes':volume,'key':key})



def read_data(request):
    with open('E:/PycharmProjects/Personal_stock_investment_system/stock/data/Table.txt', 'r') as f:
        i=0
        for line in islice(f,1,None):
            i+=1
            if i>=50:
                break
            if len(line)!=1:
                data=line.split()[:-3]
                if len(data)==55:
                    Stock.objects.create(code=data[0],
                                         name=data[1],
                                         increase=data[2],
                                         current_price=data[3],
                                         ups_and_downs=data[4],
                                         purchase_price=data[5],
                                         sell_price=data[6],
                                         total_volume=data[7],
                                         total=data[8],
                                         current_volume=data[9],
                                         rate_increase=data[10],
                                         entity_increse=data[11],
                                         current_differences=data[12],
                                         turnover=data[13],
                                         committee=data[14],
                                         total_value=data[15],
                                         circulation_value=data[16],
                                         circulation_rate=data[17],
                                         s=data[18],
                                         b=data[19],
                                         s_b=data[20],
                                         remarks=data[21],
                                         bad_news=data[22],
                                         good_news=data[23],
                                         DDE=data[24],
                                         QRR=data[25],
                                         TTM=data[26],
                                         NP=data[27],
                                         MNR=data[28],
                                         PP=data[29],
                                         de_industry=data[30],
                                         industry=data[31],
                                         yincome=data[32],
                                         opening_quotation=data[33],
                                         oir=data[34],
                                         hightest=data[35],
                                         lowest=data[36],
                                         fivedays=data[37],
                                         tendays=data[38],
                                         twentydays=data[39],
                                         form_now=data[40],
                                         amplitude=data[41],
                                         BQ=data[42],
                                         SQ=data[43],
                                         count=data[44],
                                         contribution=data[45],
                                         institutional_trends=data[46],
                                         type=data[47],
                                         general_capital=data[48],
                                         circulation_capital=data[49],
                                         total_profit=data[50],
                                         profit_rate=data[51],
                                         PPS=data[52],
                                         goleden_cross=data[53],
                                         number_of_retail_investors=data[54]).save()
                else:
                    print(data[0])
    return HttpResponse(content='200')

def delete_data(request):
    Stock.objects.all().delete()
    return HttpResponse('200')



def search(request):
    keywords=request.GET.get("keywords")
    results=Stock.objects.filter(code=keywords)
    if len(results)==0:
        return HttpResponse('Noting!')
    else:
        json_data = serializers.serialize('json', results)
        json_data = json.loads(json_data)
        data = []
        for i in json_data:
            data.append(i['fields'])
        return render(request,'stock/searchresult.html',{'rep':data})




def add_favorite(request):
    user=request.user
    stock=request.POST['code']
    capital=re.findall(r"[a-zA-Z]+",stock)
    digital=re.findall(r"\d+",stock)
    stock=capital[0]+digital[0]
    stock=Stock.objects.get(code=stock)
    created_on=datetime.datetime.now()
    if request.user.is_authenticated:
        if len(Mystock.objects.filter(user=user, stock=stock)) == 0:
            Mystock.objects.update_or_create(user=user, stock=stock, created_on=created_on)
            return redirect('/stock/collections/')
        else:
            return HttpResponse(content='已经收藏过了！')
    else:
        return HttpResponse(content='请先登录！')

def read_favorite(request):
    mystock=Mystock.objects.filter(user=request.user)
    return render(request,"stock/collections.html",{'mystock':mystock})

def delete_favorite(request):
    deleteValues = request.POST.get("deleteValues").split(',')
    for item in deleteValues:
        if item == '':
            pass
        else:
            Mystock.objects.filter(id=item)[0].delete()
    return HttpResponseRedirect('/stock/collections')

def alter_favorite_price(request):
    id=request.POST.get("id")
    price_input=request.POST.get("price_input")
    mystock = Mystock.objects.filter(id=id)[0]
    mystock.buy_price = price_input
    mystock.save()
    return HttpResponse(price_input)

def alter_favorite_count(request):
    id=request.POST.get("id")
    count_input=request.POST.get("count_input")
    mystock = Mystock.objects.filter(id=id)[0]
    mystock.buy_count=count_input
    mystock.save()
    return HttpResponse(count_input)


def create_condisitons(request):
    stock_code=request.POST.get("stock_code")
    stock=Stock.objects.all().filter(code=stock_code)

    json_data = serializers.serialize('json', stock)
    json_data = json.loads(json_data)

    # Json格式转化
    data = {}
    data['status'] = 0
    data['data'] = json_data

# {'status': 0, 'data': [{'model': 'stock.stock', 'pk': 13059, 'fields': {'code': 'SH600052', 'name': '浙江广厦', 'increase': '+10.11', 'current_price': '3.05', 'ups_and_downs': '+0.28', ......

    return render(request,"stock/createconditions.html",{'rep':json.dumps(data)})

def add_conditions(request):
    stock = request.POST.get("stock")
    ref_price=request.POST.get("ref_price")
    s_w=request.POST.get("s_w")
    s_l=request.POST.get("s_l")
    date=request.POST.get("date")
    stock=json.loads(stock)
    code=stock["data"]["code"]
    user=request.user
    mystock=Mystock.objects.filter(stock__code=code,user=user)

    var = Condition_Sheet.objects.update_or_create(ref_price=ref_price, s_l=s_l, s_w=s_w,deadline=date)[0]

    mystock.update(conditions_sheet=var)

    return HttpResponseRedirect('/stock/collections/')

def conditions(request):
    id=request.POST.get("id")
    conditions=Condition_Sheet.objects.get(pk=id)
    return render(request,'stock/conditions.html',{'conditions':conditions})

def change_conditions(request):
    id = request.POST.get("id")
    ref_price=request.POST.get("ref_price")
    s_w=request.POST.get("s_w")
    s_l=request.POST.get("s_l")
    date=request.POST.get("date")
    conditions = Condition_Sheet.objects.get(pk=id)
    conditions.ref_price=ref_price
    conditions.s_w=s_w
    conditions.s_l=s_l
    conditions.deadline=date
    conditions.save()
    return HttpResponseRedirect('/stock/collections/')

def delete_condisitons(request):
    id = request.POST.get("id")
    mystock=Mystock.objects.filter(conditions_sheet_id=id)[0]
    mystock.conditions_sheet=None
    mystock.save()
    conditions = Condition_Sheet.objects.get(pk=id)
    conditions.delete()

    return HttpResponseRedirect('/stock/collections/')







def read_company(request):
    code=request.POST.get("code")
    pro = ts.pro_api()
    df = pro.stock_company(ts_code=code)
    json_data=df.to_json(orient="records",force_ascii=False)
    json_data=json.loads(json_data)
    return render(request,"stock/company.html",{'rep':json_data[0]})


def interest(request):
    id=request.POST.get('id')
    mystock=Mystock.objects.filter(id=id)[0]
    price = mystock.buy_price
    if price is None:
        return HttpResponse('未填写价格')
    code=mystock.stock.code
    code=code[2:len(code)]+'.'+code[:2]
    df = pro.daily(ts_code=code).to_json()
    df = json.loads(df)
    open=df.get('open')['0']
    recent=float(price)
    now=float(open)
    if recent<now:
        return HttpResponse('盈利')
    else:
        return HttpResponse('未盈利')
