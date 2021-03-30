# 数据来源 [腾讯疫情实时追踪](https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0)

'''
   ！pip install json
   ！pip install requests
   ！pip install pandas
   !pip install pyecharts
   !pip install BeautifulSoup4
'''

import json
import requests
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup

# 抓取数据
reponse = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5').json()
data = json.loads(reponse['data'])

reponse1 = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_other').json()
data1 = json.loads(reponse1['data'])

reponse_global = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign').json()
data_global = json.loads(reponse_global['data'])
data.keys()
data_global.keys()

# 国内
lastUpdateTime = data['lastUpdateTime']
'''
由于后面可视化要用到，但这字典的key都是英文，
为了方便观看，我就将其转化为中文了
'''

chinaTotal = data['chinaTotal']
chinaTotal['确诊'] = chinaTotal['confirm']
chinaTotal['疑似'] = chinaTotal['suspect']
chinaTotal['死亡'] = chinaTotal['dead']
chinaTotal['治愈'] = chinaTotal['heal']
chinaTotal['现有确诊'] = chinaTotal['nowConfirm']
chinaTotal['现有重症'] = chinaTotal['nowSevere']
del chinaTotal['confirm']
del chinaTotal['suspect']
del chinaTotal['dead']
del chinaTotal['heal']
del chinaTotal['nowConfirm']
del chinaTotal['nowSevere']

sum = chinaTotal['确诊'] + chinaTotal['疑似'] + chinaTotal['死亡'] + chinaTotal['治愈']

chinaAdd = data['chinaAdd']
chinaAdd['新增确诊'] = data['chinaAdd']['confirm']
chinaAdd['新增疑似'] = data['chinaAdd']['suspect']
chinaAdd['新增死亡'] = data['chinaAdd']['dead']
chinaAdd['新增治愈'] = data['chinaAdd']['heal']
chinaAdd['新增确诊'] = chinaAdd['nowConfirm']
chinaAdd['新增重症'] = chinaAdd['nowSevere']
del chinaAdd['confirm']
del chinaAdd['suspect']
del chinaAdd['dead']
del chinaAdd['heal']
del chinaAdd['nowConfirm']
del chinaAdd['nowSevere']

areaTree = data['areaTree']

china_data = areaTree[0]['children']
china_list = []
for x in range(len(china_data)):
    province = china_data[x]['name']
    province_list = china_data[x]['children']
    for y in range(len(province_list)):
        city = province_list[y]['name']
        total = province_list[y]['total']
        today = province_list[y]['today']
        china_dict = {'province': province, 'city': city, 'total': total, 'today': today}
        china_list.append(china_dict)

# 定义数据处理函数
def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm

def suspect(x):
    suspect = eval(str(x))['suspect']
    return suspect

def dead(x):
    dead = eval(str(x))['dead']
    return dead

def heal(x):
    heal = eval(str(x))['heal']
    return heal

def confirmCuts(x):
    confirmCuts = eval(str(x))['confirmCuts']
    return confirmCuts

def deadRate(x):
    deadRate=eval(str(x))['deadRate']
    return deadRate

def healRate(x):
    healRate=eval(str(x))['healRate']
    return healRate

china_data = pd.DataFrame(china_list)


china_data.head()

areaTree_global = data_global['foreignList']

global_data = areaTree_global[1]

len(areaTree_global)

# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['suspect'] = china_data['total'].map(suspect)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data['deadRate']=china_data['total'].map(deadRate)
china_data['healRate']=china_data['total'].map(healRate)
china_data['addconfirm'] = china_data['today'].map(confirm)
china_data['addconfirmCuts'] = china_data['today'].map(confirmCuts)
china_data = china_data[
    ["province", "city", "confirm", "suspect", "dead", "heal","deadRate","healRate", "addconfirm", "addconfirmCuts"]]
china_data.head()

#国际数据处理
global_list = []
for x in range(len(areaTree_global)):
    country = areaTree_global[x]['name']
    confirm = areaTree_global[x]['confirm']
    nowConfirm = areaTree_global[x]['nowConfirm']
    dead = areaTree_global[x]['dead']
    heal = areaTree_global[x]['heal']
    deadRate = areaTree_global[x]['dead'] / areaTree_global[x]['confirm']
    healRate = areaTree_global[x]['heal'] / areaTree_global[x]['confirm']
    date = areaTree_global[x]['date']
    global_dict = {'country': country, 'confirm': confirm, 'nowConfirm': nowConfirm, 'dead': dead, 'heal': heal,
                   'deadRate': deadRate, 'healRate': healRate, 'date': date}
    global_list.append(global_dict)

country = '中国'
confirm = data['chinaTotal']['确诊']
nowConfirm = data['chinaTotal']['现有确诊']
dead = data['chinaTotal']['死亡']
heal = data['chinaTotal']['治愈']
deadRate = data['chinaTotal']['死亡'] / data['chinaTotal']['确诊']
healRate = data['chinaTotal']['治愈'] / data['chinaTotal']['确诊']
date = global_list[0]['date']
global_dict = {'country': country, 'confirm': confirm, 'nowConfirm': nowConfirm, 'dead': dead, 'heal': heal,
               'deadRate': deadRate, 'healRate': healRate, 'date': date}
global_list.append(global_dict)
'''confirm =data['chinaTotal']['confirm']
nowConfirm=chinaTotal['nowConfirm']
dead=chinaTotal['dead']
heal=chinaTotal['heal']
deadRate=chinaTotal['dead']/chinaTotal['confirm']
healRate=chinaTotal['heal']/chinaTotal['confirm']
'''

global_data = pd.DataFrame(global_list)
world_name = pd.read_excel("世界各国中英文对照.xlsx")
global_data = pd.merge(global_data, world_name, left_on="country", right_on="中文", how="inner")
global_data = global_data[
    ["country", "英文", "confirm", "nowConfirm", "dead", "heal","deadRate","healRate"]]

# 日数据处理
chinaDayList = pd.DataFrame(data1['chinaDayList'])
chinaDayList = chinaDayList[['date', 'confirm', 'suspect', 'dead', 'heal']]
chinaDayList.head()

# 日新增数据处理
chinaDayAddList = pd.DataFrame(data1['chinaDayAddList'])
chinaDayAddList = chinaDayAddList[['date', 'confirm', 'suspect', 'dead', 'heal']]
chinaDayAddList.tail()

# 饼图
total_pie = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='450px', height='315px', bg_color="transparent"))
        .add("", [list(z) for z in zip(['确     诊  ', '疑     似  ', '死     亡  ', '治     愈  '], chinaTotal.values())],
             center=["50%", "60%"], radius=[75, 100], )
        .add("", [list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())], center=["50%", "60%"], radius=[0, 50])
        .set_global_opts(title_opts=opts.TitleOpts(title="全国总量", pos_bottom=0,
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF")),
                         legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))

#世界地图绘制
world_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(global_data["英文"]), list(global_data["confirm"]))], "world",
             is_map_symbol_show=False)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts(orient='vertical', pos_right="10%"))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, background_color="transparent",
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 10000000, "label": '>10000000', "color": "#893448"},
                                                               {"min": 1000000, "max": 9999999, "label": '1000000-9999999',
                                                                "color": "#FF3200"},
                                                               {"min": 100000, "max": 999999, "label": '100000-999999',
                                                                "color": "#A7FF48"},
                                                               {"min": 10000, "max": 99999, "label": '10000-99999',
                                                                "color": "#00FF42"},
                                                               {"min": 1000, "max": 9999, "label": '1000-9999',
                                                                "color": "#00FFAA"},
                                                               {"min": 100, "max": 999, "label": '100-999',
                                                                "color": "#FAD634"},
                                                               {"min": 10, "max": 99, "label": '10-99',
                                                                "color": "#fb8146"},
                                                               {"min": 1, "max": 9, "label": '1-9',
                                                                "color": "#fff2d1"},
                                                           ])))

city_data = china_data.groupby('city')['confirm'].sum().reset_index()
city_data.columns = ["city", "confirm"]


# 数据处理
area_data = china_data.groupby("province")["confirm"].sum().reset_index()
area_data.columns = ["province", "confirm"]

# 中国疫情地图绘制
area_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",
             is_map_symbol_show=False, label_opts=opts.LabelOpts(color="#fff"),
             tooltip_opts=opts.TooltipOpts(is_show=True), zoom=1.2, center=[105, 30])#105,30
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="中国疫情分布图", pos_top='5%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#FF0000")),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pos_right=0, pos_bottom=0,
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 1001, "label": '>1000', "color": "#893448"},
                                                               {"min": 500, "max": 1000, "label": '500-1000',
                                                                "color": "#ff585e"},
                                                               {"min": 101, "max": 499, "label": '101-499',
                                                                "color": "#fb8146"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#ffb248"},
                                                               {"min": 0, "max": 9, "label": '0-9',
                                                                "color": "#fff2d1"}])))

ity_data = china_data.groupby('city')['confirm'].sum().reset_index()
city_data.columns = ["city", "confirm"]

def is_city(item):
    '''
    判断一个城市能否在Geo地图上被找到
    :param item: 城市名
    :return: T/F
    '''

    lists_1 = []
    lists_1.append(item)
    lists_2 = [10]
    geo = Geo()
    geo.add_schema(maptype="china")
    try:
        geo.add("确诊城市", [list(z) for z in zip(lists_1, lists_2)])
        return True
    except Exception:
        return False


city_index = []
i = 0
for item in city_data['city']:
    if is_city(item) == False:
        city_index.append(i)
    i += 1

for x in city_index:
    del (city_data['city'][x])
    del (city_data['confirm'][x])

city_index_ = []
i = 0
for item in city_data['confirm']:
    if item > 1000:
        city_index_.append(i)
    i += 1

serious_city = []  # 严重城市
serious_submit = []  # 严重人数
for y in city_index_:
    serious_city.append(list(city_data['city'])[y])
    serious_submit.append(list(city_data['confirm'])[y])

list_1 = ["拉萨"]
list_2 = [1]

area_heat_geo = (
    Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, bg_color='transparent'))
        .add_schema(maptype="china", zoom=1.2, center=[105, 30])
        .add("确诊城市", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))], symbol_size=10)
        .add("确诊城市", [list(z) for z in zip(list_1, list_2)], symbol_size=10)
        .add("确诊城市", [list(z) for z in zip(list(serious_city), list(serious_submit))],  # 感染者超1000的城市
             type_=ChartType.EFFECT_SCATTER, effect_opts=opts.EffectOpts(is_show=True, color="black",
                                                                         symbol_size=30, scale=4, period=1))
        .add("", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))],
             type_=ChartType.HEATMAP)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_size=[0, 25, 50, 75, 100], max_=1000, orient='horizontal',
                                          pos_bottom=0),
        title_opts=opts.TitleOpts(title="中国疫情分布热图", pos_top='5%'),
        legend_opts=opts.LegendOpts(pos_bottom='10%', pos_left=0)))

date = []  # 日期
confirmTotal = []  # 累计确诊
confirmAdd = []  # 新增确诊
suspectTotal = []  # 累计疑似
suspectAdd = []  # 新增疑似
deadTotal = []  # 累计死亡
deadAdd = []  # 新增死亡
healTotal = []  # 累计治愈
healAdd = []  # 新增治愈
deadRate = []  # 死亡率
healRate = []  # 治愈率

for j in data1['chinaDayAddList']:
    confirmAdd.append(j['confirm'])
    suspectAdd.append(j['suspect'])
    deadAdd.append(j['dead'])
    healAdd.append(j['heal'])

for k in data1['chinaDayList']:
    date.append(k['date'])
    confirmTotal.append(k['confirm'])
    suspectTotal.append(k['suspect'])
    deadTotal.append(k['dead'])
    healTotal.append(k['heal'])
    deadRate.append(k['deadRate'])
    healRate.append(k['healRate'])


line_1 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计确诊", confirmTotal, yaxis_index=1, is_smooth=True,
                   tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))
bar_1 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date[7:])
        .add_yaxis("单日确诊", confirmAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("确诊", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_1)

line_2 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计疑似", suspectTotal, yaxis_index=1, is_smooth=True,
                   tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

bar_2 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date[7:])
        .add_yaxis("单日疑似", suspectAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("疑似", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_2)

line_3 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计死亡", deadTotal, yaxis_index=1, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

bar_3 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date[7:])
        .add_yaxis("单日死亡", deadAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_3)

line_4 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.ROMA, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计治愈", healTotal, yaxis_index=1, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))
bar_4 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA, bg_color="#333333"))
        .add_xaxis(date[7:])
        .add_yaxis("单日治愈", healAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("治愈",pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_4)

line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("死亡率", deadRate, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}%"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡/治愈率",pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

lines = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("治愈率", healRate, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}%"))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡/治愈率", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(line)

tl = (
    Timeline(init_opts=opts.InitOpts(theme=ThemeType.WALDEN, bg_color="transparent"))
        .add_schema(play_interval=5000, is_auto_play=True,width='70%',height='10%',pos_left='center',
                    linestyle_opts=opts.LineStyleOpts(),label_opts=opts.LabelOpts(position='bottom',color="white"))
        .add(bar_1, "确诊")
        .add(bar_2, "疑似")
        .add(bar_3, "死亡")
        .add(bar_4, "治愈")
        .add(lines, "死亡/治愈率"))
#中间大标题
big_title = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="COVID-19",
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#FFFFFF',
                                                                          border_radius=True, border_color="white"),
                                  pos_top=0)))
#截至时间
times = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(subtitle=("截至 " + lastUpdateTime),
                                  subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13, color='#FFFFFF'),
                                  pos_top=0))
)

confirms = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="确诊", pos_left='center', pos_top='center',
                                                      subtitle="(累计)",item_gap=1,
                                                      subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
confirms_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['确诊']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         新增: " + str(chinaAdd['新增确诊'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
                                                             )))
suspects = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="疑似", pos_left='center', pos_top='center',
                                                      subtitle="(现有)",item_gap=1,
                                                      subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
suspects_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['疑似']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         新增 :" + str(chinaAdd['新增疑似'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#FF00FF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#EE82EE")
                                                             )))
deads = (Pie().
         set_global_opts(title_opts=opts.TitleOpts(title="死亡", pos_left='center', pos_top='center',
                                                   subtitle="(累计)",item_gap=1,
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
deads_people = (Pie().
                set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['死亡']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         新增 :" + str(chinaAdd['新增死亡'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#FF0000",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#F08080")
                                                          )))
heals = (Pie().
         set_global_opts(title_opts=opts.TitleOpts(title="治愈", pos_left='center', pos_top='center',
                                                   subtitle="(累计)",item_gap=1,
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
heals_people = (Pie().
                set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['治愈']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         新增 :" + str(chinaAdd['新增治愈'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#00FF00",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#98FB98")
                                                          )))

sum=chinaTotal['确诊']+chinaTotal['疑似']+chinaTotal['死亡']+chinaTotal['治愈']
confirm_liquid = (
    Liquid()
        .add("确诊比例", [chinaTotal['确诊'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#00FFFF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

suspect_liquid = (
    Liquid()
        .add("疑似比例", [chinaTotal['疑似'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF00FF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

dead_liquid = (
    Liquid()
        .add("死亡比例", [chinaTotal['死亡'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF0000",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

heal_liquid = (
    Liquid()
        .add("治愈比例", [chinaTotal['治愈'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#00FF00",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

wc = (
    WordCloud()
        .add("", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))],
             word_gap=0, word_size_range=[10, 30]))


page = (Page(page_title="COVID-19多维数据一览")
        .add(total_pie)
        .add(world_map)
        .add(area_map)
        .add(area_heat_geo)
        #.add(bar)
        .add(tl)
        .add(big_title)
        .add(times)
        .add(confirms)
        .add(confirms_people)
        .add(suspects)
        .add(suspects_people)
        .add(deads)
        .add(deads_people)
        .add(heals)
        .add(heals_people)
        .add(confirm_liquid)
        .add(suspect_liquid)
        .add(dead_liquid)
        .add(heal_liquid)
        .add(wc)
        ).render('COVID-19 多维数据一览.html')

with open("COVID-19 多维数据一览.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0][
        'style'] = "width:411px;height:303px;position:absolute;top:5px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[1][
        "style"] = "width:605px;height:274px;position:absolute;top:36px;left:333px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[2][
        "style"] = "width:309px;height:405px;position:absolute;top:313px;left:961px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[3][
        "style"] = "width:305px;height:405px;position:absolute;top:310px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[4][
        "style"] = "width:646px;height:304px;position:absolute;top:312px;left:312px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[5][
        "style"] = "width:250px;height:55px;position:absolute;top:2px;left:440px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[6][
        "style"] = "width:200px;height:30px;position:absolute;top:11px;left:675px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[7][
        'style'] = "width:60px;height:75px;position:absolute;top:5px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:25px 0px 0px 0px"
    divs[8][
        "style"] = "width:130px;height:75px;position:absolute;top:5px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[9][
        "style"] = "width:60px;height:75px;position:absolute;top:80px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[10][
        "style"] = "width:130px;height:75px;position:absolute;top:80px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[11][
        "style"] = "width:60px;height:75px;position:absolute;top:155px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[12][
        "style"] = "width:130px;height:75px;position:absolute;top:155px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[13][
        "style"] = "width:60px;height:75px;position:absolute;top:230px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[14][
        "style"] = "width:130px;height:75px;position:absolute;top:230px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:0px 0px 25px 0px"

    divs[15][
        "style"] = "width:160px;height:160px;position:absolute;top:-35px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[16][
        "style"] = "width:160px;height:160px;position:absolute;top:40px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[17][
        "style"] = "width:160px;height:160px;position:absolute;top:115px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[18][
        "style"] = "width:160px;height:160px;position:absolute;top:188px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[19][
        "style"] = "width:1280px;height:120px;position:absolute;top:600px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"

    body = html_bf.find("body")
    body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()


