from django.conf import settings
from django.db import models

# Create your models here.
class Stock(models.Model):
    code = models.CharField(max_length=20, verbose_name='代码')
    name=models.CharField(max_length=50,verbose_name='名称')
    increase = models.CharField(verbose_name='涨幅',max_length=20)
    current_price=models.CharField(verbose_name='现价',max_length=20)
    ups_and_downs=models.CharField(verbose_name='涨跌',max_length=20)
    purchase_price=models.CharField(verbose_name='买价',max_length=20)
    sell_price=models.CharField(verbose_name='卖价',max_length=20)
    total_volume=models.CharField(verbose_name='总手',max_length=20)
    total=models.CharField(verbose_name='总金额',max_length=20)
    current_volume=models.CharField(max_length=20,verbose_name='现手')
    rate_increase=models.CharField(max_length=20,verbose_name='涨速')
    entity_increse=models.CharField(max_length=20,verbose_name='实体涨幅')
    current_differences=models.CharField(verbose_name='现均差',max_length=20)
    turnover=models.CharField(max_length=20,verbose_name='换手率')
    committee=models.CharField(verbose_name='委比',max_length=20)
    total_value=models.CharField(verbose_name='总市值',max_length=20)
    circulation_value=models.CharField(verbose_name='流通市值',max_length=20)
    circulation_rate=models.CharField(max_length=20,verbose_name='流通比例')
    s=models.CharField(verbose_name='内盘',max_length=20)
    b=models.CharField(verbose_name='外盘',max_length=20)
    s_b=models.CharField(verbose_name='内外比',max_length=20)
    remarks=models.CharField(max_length=20,verbose_name='备注',default='')
    bad_news=models.CharField(verbose_name='利空',max_length=20)
    good_news=models.CharField(verbose_name='利好',max_length=20)
    DDE=models.CharField(verbose_name='主力净量',max_length=20)
    QRR=models.CharField(verbose_name='量比',max_length=20,blank=True,null=True)
    TTM=models.CharField(verbose_name='市盈率',max_length=20)
    NP=models.CharField(verbose_name='净利润',max_length=20)
    MNR=models.CharField(verbose_name='市净率',max_length=20)
    PP=models.CharField(verbose_name='每股盈利',max_length=20)
    de_industry=models.CharField(max_length=20,verbose_name='细分行业')
    industry=models.CharField(max_length=20,verbose_name='行业')
    yincome=models.CharField(verbose_name='昨收',max_length=20)
    opening_quotation=models.CharField(verbose_name='开盘',max_length=20)
    oir=models.CharField(max_length=20,verbose_name='开盘涨幅')
    hightest=models.CharField(verbose_name='最高',max_length=20)
    lowest=models.CharField(verbose_name='最低',max_length=20)
    fivedays=models.CharField(max_length=20,verbose_name='5日涨幅')
    tendays=models.CharField(max_length=20,verbose_name='10日涨幅')
    twentydays=models.CharField(max_length=20,verbose_name='20日涨幅')
    form_now=models.CharField(max_length=20,verbose_name='年初至今')
    amplitude=models.CharField(max_length=20,verbose_name='振幅')
    BQ=models.CharField(verbose_name='买量',max_length=20)
    SQ=models.CharField(verbose_name='卖量',max_length=20)
    count=models.CharField(verbose_name='笔数',max_length=20)
    contribution=models.CharField(verbose_name='贡献度',max_length=20,blank=True,null=True)
    institutional_trends=models.CharField(verbose_name='机构动向',max_length=20)
    type=models.CharField(max_length=20,verbose_name='异动类型')
    general_capital=models.CharField(verbose_name='总股本',max_length=20)
    circulation_capital=models.CharField(verbose_name='流通股本',max_length=20)
    total_profit=models.CharField(verbose_name='总利润',max_length=20)
    profit_rate=models.CharField(verbose_name='利润率',max_length=20)
    PPS=models.CharField(verbose_name='每股净资产',max_length=20)
    goleden_cross=models.CharField(verbose_name='金叉个数',max_length=20)
    number_of_retail_investors=models.CharField(verbose_name='散户数量',max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='股票'
        verbose_name_plural='股票'

class Condition_Sheet(models.Model):
    ref_price=models.CharField(verbose_name='参考基准价',max_length=20,null=True)
    s_w = models.CharField(verbose_name='止赢条件', max_length=20,null=True)
    s_l = models.CharField(verbose_name='止损条件', max_length=20,null=True)
    deadline = models.CharField(verbose_name='截至时间',max_length=20,null=True)
    def __str__(self):
        return "条件表信息"
    class Meta:
        verbose_name="止赢止损表"
        verbose_name_plural="止赢止损表"
class Mystock(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='用户')
    stock=models.ForeignKey(Stock,on_delete=models.CASCADE,verbose_name='我的股票')

    buy_count=models.CharField(verbose_name='买入数量',null=True,max_length=20)
    buy_price=models.CharField(verbose_name='买入单价',null=True,max_length=20)

    created_on=models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')
    conditions_sheet=models.ForeignKey(Condition_Sheet,on_delete=models.CASCADE,verbose_name='止盈止损条件单',null=True)
    def __str__(self):
        return self.stock.name
    class Meta:
        verbose_name='我收藏的股票'
        verbose_name_plural='我收藏的股票'




