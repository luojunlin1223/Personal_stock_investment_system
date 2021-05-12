import datetime
import json

import tushare as ts
from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render
from notifications.signals import notify

from stock.models import Mystock
from users.models import UserProfile
# 开启定时工作


def timedTask():
    mystock = Mystock.objects.all()
    for item in mystock:
        conditions_sheet = item.conditions_sheet
        if conditions_sheet:
            now = datetime.datetime.today().date()
            records = datetime.datetime.strptime(conditions_sheet.deadline, "%Y-%m-%d").date()
            if records < now:
                print('已经超过了日期')
            else:
                s_w = float(conditions_sheet.s_w[:-1][1:])
                w = ((s_w + 100) / 100) * float(conditions_sheet.ref_price)
                l = (100 - float(conditions_sheet.s_l[:-1][1:])) / 100 * float(conditions_sheet.ref_price)
                code = item.stock.code
                code=code[2:len(code)]+'.'+code[:2]
                ts.set_token('f281dbc422d80e2350e94b1878bd3b86971de985641877fc42ccd836')
                pro = ts.pro_api()
                df = pro.daily(ts_code=code, trade_date=now.strftime("%Y%m%d")).to_json()
                #df = pro.daily(ts_code=code, trade_date='20210507').to_json()
                df=json.loads(df)
                if len(df.get('open'))!=0:
                    open=df.get('open')['0']
                    if open:
                        verb=''
                        if float(open)<=l:
                            verb='股票价格低于最低止损'
                        elif float(open)>=w:
                            verb='股票价格高于最高止盈'
                        root = UserProfile.objects.filter(is_superuser=True)[0]
                        notify.send(root, recipient=item.user, verb=verb,
                                    target=Mystock.objects.filter(conditions_sheet=conditions_sheet)[0]
                                    , action_object=conditions_sheet)

                    else:
                        print('不满足条件')
                        pass
                else:
                    print('股票今日休市')

scheduler = BackgroundScheduler()
scheduler.add_job(timedTask, 'interval', seconds=2)
#scheduler.add_job(timedTask, 'interval', days=1)

#scheduler.start()


# Create your views here.
def showhomepage(request):
    return render(request, 'homepage/homepage.html')
