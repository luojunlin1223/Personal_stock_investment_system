import base64
import datetime
import json
import re
from io import BytesIO
from itertools import islice

import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from matplotlib import ticker
from mplfinance.original_flavor import candlestick_ochl

plt.rcParams['font.sans-serif'] = ['SimHei']   # 用来正常显示中文标签
from stock.models import Stock, Mystock, Condition_Sheet


def showinfo(request, page):
    global df
    page = int(page)
    items_per_page = 10
    last_page = page - 1
    nex_page = page + 1

    stock = Stock.objects.all().order_by('code')[(page - 1) * items_per_page:page * items_per_page]

    json_data=serializers.serialize('json',stock)
    json_data=json.loads(json_data)

    #Json格式转化
    data={}
    data['status']=0
    data['items_per_page']=10
    data['last_page']=last_page
    data['next_page']=nex_page
    data['data'] = json_data


    if len(stock) != 0:
        return render(request, 'stock/showinfo.html',
                      {'stock': data})
    else:
        return HttpResponse(content='超出数据范围！')

def showdetail(request):
    code=request.GET.get("code")
    method=request.GET.get("method")
    ts.set_token('f281dbc422d80e2350e94b1878bd3b86971de985641877fc42ccd836')
    pro = ts.pro_api()
    if method == 'daily':
        df = pro.daily(ts_code=code, start_date='20200901', end_date='20210409')
    elif method == 'weekly':
        df = pro.weekly(ts_code=code, start_date='20200901', end_date='20210409')
    elif method == 'monthly':
        df = pro.monthly(ts_code=code, start_date='20200901', end_date='20210409')
    else:
        return HttpResponse('None')
    # 原始数据按照日期降序排列
    df = df.sort_values(by='trade_date', ascending=True)
    df['dates'] = np.arange(0, len(df))
    fig, ax = plt.subplots(figsize=(10, 7))
    ###candlestick_ochl()函数的参数
    # ax 绘图Axes的实例
    # quotes  序列（时间，开盘价，收盘价，最高价，最低价） 时间是float类型，date必须转换为float
    # width    图像中红绿矩形的宽度,代表天数
    # colorup  收盘价格大于开盘价格时的颜色
    # colordown   低于开盘价格时矩形的颜色
    # alpha      矩形的颜色的透明度
    candlestick_ochl(ax, quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
                     width=0.55, colorup='r', colordown='g', alpha=0.95)
    date_tickers = df['trade_date'].values

    def format_date(x, pos):
        if (x < 0) or (x > len(date_tickers) - 1):
            return ''
        return date_tickers[int(x)]

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  # 按一定规则选取并在水平轴上显示时间刻度
    plt.xticks(rotation=30)  # 设置日期刻度旋转的角度
    ax.set_ylabel('交易价格')
    plt.title(code)
    plt.grid(True)  # 添加网格，可有可无，只是让图像好看一些
    plt.xlabel('交易日期')

    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 前端只需要将 <img\> 标签的 src 属性赋值为后端发送的 Base64 字符串即可
    return render(request, 'stock/detail.html', {'image': src, 'code': code})

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
        return render(request,'stock/searchresult.html',{'results':results})

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
            return HttpResponse(content='收藏成功！')
        else:
            return HttpResponse(content='已经收藏过了！')
    else:
        return HttpResponse(content='请先登录！')

def read_favorite(request):
    mystock=Mystock.objects.all()

    return render(request,"stock/collections.html",{'mystock':mystock})

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

    print(data)
    return render(request,"stock/createconditions.html",{'rep':json.dumps(data)})


def add_conditions(request):
    stock = request.POST.get("stock")
    ref_price=request.POST.get("ref_price")
    s_w=request.POST.get("s_w")
    s_l=request.POST.get("s_l")
    print(stock)
   # Condition_Sheet.objects.update_or_create(ref_price=ref_price,s_l=s_l,s_w=s_w)

    return HttpResponse(stock+ref_price+s_w+s_l)