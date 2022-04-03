# 新冠疫苗接种数据可视化



## 0. 写在前面

数据可视化，是指将相对晦涩的数据通过可视的、交互的方式进行展示，从而形象、直观地表达数据蕴含的信息和规律。[Echarts](https://github.com/ecomfe/echarts) 是一个由百度开源的数据可视化工具，凭借着良好的交互性，精巧的图表设计，得到了众多开发者的认可。而 Python 是一门富有表达力的语言，很适合用于数据处理。当数据分析遇上数据可视化时，[pyecharts](https://github.com/pyecharts/pyecharts) 诞生了。本项目通过pyecharts对各国新冠疫苗接种数据进行可视化，让用户对各国抗疫情况有一个大概的了解。同时愿世界各国以团结取代分歧、以理性消除偏见，不断推动构建人类命运共同体，凝聚起抗击疫情的强大合力，共克时艰，维护人类共同家园。



## 1. 体验示例网页

点击网址https://1541453904.rth1.me/result.html 即可查看。

*推荐使用[Google Chrome](https://www.google.com/intl/zh-CN/chrome/)浏览。*

![image-20211224170612536](figs/image-20211224170612536.png)



## 2. 开发环境

* OS: Windows

* Language: Python
* Third-party libraries: Pyecharts

`Pyecharts`官网：https://pyecharts.org/#/zh-cn/intro

| Tools     | Version | Install                                | Link                              |
| --------- | ------- | -------------------------------------- | --------------------------------- |
| python    | 3.8     | https://zhuanlan.zhihu.com/p/344887837 | https://www.python.org/downloads/ |
| pyecharts | 1.9     | pip install pyecharts                  | https://pyecharts.org/#/          |

更多优秀美观的图表的制作，请移步官网。



## 3. 数据获取

谷歌新闻：https://news.google.com/covid19/map?hl=en-US&gl=US&ceid=US%3Aen&state=7

国家卫生健康委员会：http://www.nhc.gov.cn/xcs/xxgzbd/gzbd_index.shtml



## 4. 代码

本项目开源：https://github.com/gunshi3/covid-19_vaccinated



### 4.1 数据处理

```python
import pandas as pd

# read excel data
df = pd.read_excel("covid-19_vaccinated.xlsx", engine="openpyxl")

# get min and max value
percent_min = df.describe()['Percent'].min()
percent_max = df.describe()['Percent'].max()

fully_vaccinated_min = df.describe()['Fully vaccinated'].min()
fully_vaccinated_max = df.describe()['Fully vaccinated'].max()

# standard data
covid_19_data = list()
country_name_map = dict()
for index, data in df.iterrows():
    country = data['country']
    en_country = data['en_country']
    percent = data['Percent']
    fully_vaccinated = data['Fully vaccinated']
    # print(country, en_country, percent, fully_vaccinated)
    covid_19_data.append({'name': en_country, 'value': [percent, fully_vaccinated, en_country]})
    country_name_map[en_country] = country
# print(covid_19_data)
# print(country_name_map)
```



### 4.2 模块、变量

```python
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Pie, Bar, Map, Line, Liquid, Page

from standard_data import covid_19_data, country_name_map

percent_min_data = min([_['value'][0] for _ in covid_19_data])
percent_max_data = max([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])
```



### 4.3 折线图

```python
def _line():
    yaxis_data = [_['value'][0] for _ in covid_19_data]
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data]
    chart_line = (
        Line()
            .add_xaxis(xaxis_data=xaxis_data)  # x轴数据，[str,str,str]
            .add_yaxis(
            series_name="接种率", y_axis=yaxis_data,  # y轴数据[num,num,num]
            markpoint_opts=opts.MarkPointOpts(
                data=[  # 标记
                    opts.MarkPointItem(type_="min"), opts.MarkPointItem(type_="max"),
                    opts.MarkPointItem(name="自义标记点定", coord=[xaxis_data[8], yaxis_data[8]])
                ]
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-MarkPoint"),  # 标题
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),  # 倾斜x轴
        )
    )
    return chart_line
```



### 4.4 柱状图

```python
def _bar():
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data][::-1]
    yaxis_data = [round(_['value'][1] / 10000, 2) for _ in covid_19_data][::-1]
    chart_bar = (
        Bar().add_xaxis(xaxis_data)  # 传入x轴的数据, 格式为[1,2,3,4,5]
            .add_yaxis(
            series_name="",  # 系列名称
            y_axis=yaxis_data,  # y轴的数据,[num,num,num]
            label_opts=opts.LabelOpts(  # 标签配置
                position='right',  # 标签显示的位置，inside，left，top，bottom
                formatter="{b}: {c}万"  # 标签显示的格式
            )
        )
            .reversal_axis()  # x轴y轴倒置
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),  # 不显示坐标轴的标签
            tooltip_opts=opts.TooltipOpts(is_show=False),  # 关闭提示，鼠标移动过去不显示
            visualmap_opts=opts.VisualMapOpts(
                dimension=0,
                range_text=['max', 'min'],  # 组件两端的文本
                # is_calculable=True,  # 显示组件拖拽手柄
                # range_color=["lightskyblue", "red", "pink"],  # 组件过渡颜色
                # textstyle_opts=opts.TextStyleOpts(
                #     color="rgba(0,0,0,0.5)"  # 文字颜色
                # ),
                min_=round(vaccinated_min_data / 10000, 2),  # 组件最小值
                max_=round(vaccinated_max_data / 10000, 2),  # 组件最大值
            )
        )
    )
    chart_bar.chart_id = "1"
    return chart_bar
```



### 4.5 地图

```python
def _map():
    data = [[_['name'], [_['value'][0], round(_['value'][1] / 10000, 2), country_name_map[_['name']]]] for _ in
            covid_19_data]
    chart_map = (
        Map()
            .add(
            series_name='',  # 系列名称，用于tooltip的显示
            data_pair=data,  # 格式为 [['country', value],['country', value]]
            maptype='world',
            is_map_symbol_show=False,  # 显示图形标记，默认True
            label_opts=opts.LabelOpts(is_show=False),  # 不显示地名
            itemstyle_opts={  # 图元样式配置项
                "normal": {
                    # 显示的样式
                    "areaColor": "#CED8F6",
                    "borderColor": "#404a59"
                },
                "emphasis": {
                    # 鼠标选中后显示的样式
                    "lable": {"show": Map},
                    "areaColor": "rgba(255,255,255, 0.5)"

                },
            }
        )
            .set_global_opts(
            # 设置标题
            title_opts=opts.TitleOpts(
                title="Covid-19 World vaccinated 2021-12-21",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=35,
                    color="rgba(155,155,155,0.9)"
                )
            ),
            # 设置 提示框配置项
            tooltip_opts=opts.TooltipOpts(
                # formatter="{b}:{c}{d}",  # 格式化 显示在选中时候的样式
                # is_show=False
                formatter=JsCode(
                    """
                    function (params){
                      if('value' in params.data){
                          return params.data.value[2] + ' : ' + params.data.value[0] + '% : ' + params.data.value[1]+'万'
                      }
                    }
                    """
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                # orient='vertical',  # 垂直，可设置 水平 horizontal
                # is_calculable=True,  # 可拖拽
                dimension=0,  # 维度，多层图形时候有用
                pos_right='right',  # 组件位置
                pos_bottom='bottom',  # 组件位置
                range_text=['max', 'min'],  # 组件两端的文本
                # range_color=["lightskyblue", "yellow", "orangered"],  # 组件过渡颜色
                min_=percent_min_data,  # 组件最小值
                max_=percent_max_data,  # 组件最大值
            )
        )
    )
    chart_map.chart_id = "2"
    return chart_map
```



### 4.6 水球图

```python
def _liquid():
    percent_max = (
        Liquid()
            .add(
            series_name="最高比率",
            data=[round(percent_max_data / 100, 2), 0.3],  # 第一个值为显示的值，第二个值为水的分量
            center=["25%", "25%"],
            color='white',
            background_color='lightskyblue',
            is_outline_show=False,  # 显示外边框，默认True
            label_opts=opts.LabelOpts(color='pink', position="inside")
        )
    )
    percent_min = (
        Liquid()
            .add(
            series_name="最低比率",
            data=[percent_min_data / 100, 0.3],  # 第一个值为显示的值，第二个值为水的分量
            center=["25%", "25%"],
            is_outline_show=False
        )
    )
    percent_max.chart_id = "3"
    percent_min.chart_id = "4"
    return percent_max, percent_min
```



### 4.7 饼图

```python
def _pie():
    data = [(country_name_map[_['name']], _['value'][0]) for _ in covid_19_data]
    chart_pie = (
        Pie()
            .add(
            series_name="",
            data_pair=data,  # 格式为 [(key1, value1), (key2, value2)]
            radius=["30%", "75%"],  # 饼图的半径，第一项内半径，第二项外半径
            center=["25%", "50%"],  # 饼图的坐标，第一项内横坐标，第二项纵坐标
            rosetype="radius",  # 扇区圆心角展现数据的百分比，半径展现数据的大小
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="Vaccinated Rose"),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    chart_pie.chart_id = "5"
    return chart_pie
```



### 4.8 重叠图

```python
def _overlap():
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data]
    yaxis_one_data = [_['value'][0] for _ in covid_19_data]
    yaxis_two_data = [round(_['value'][1] / 10000, 2) for _ in covid_19_data]
    chart_overlap = (
        Bar()
            .add_xaxis(xaxis_data)  # x轴数据格式，同柱状图
            .add_yaxis(
            series_name="单位/万",
            y_axis=yaxis_two_data,  # y轴数据格式，同柱状图
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} %"), interval=5,  # 显示的y轴，间隔为5
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示柱状图上面的图
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} 万"),  # 显示的y轴
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),  # 倾斜x轴
        )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=xaxis_data)  # x轴数据格式，同柱状图
            .add_yaxis(
            series_name="单位 %",
            y_axis=yaxis_one_data,  # y轴数据格式，同柱状图
            yaxis_index=1,
            markpoint_opts=opts.MarkPointOpts(
                data=[  # 标记
                    opts.MarkPointItem(type_="min"), opts.MarkPointItem(type_="max"),
                    # opts.MarkPointItem(name="自定义", coord=[xaxis_data[0], yaxis_one_data[0]], value=yaxis_one_data[0])
                ]
            )
        )
    )
    chart_overlap.overlap(line)
    chart_overlap.chart_id = "6"
    return chart_overlap
```



### 4.9 组合图

```python
def first_run():
    chartBar = _bar()
    chartMap = _map()
    chartLiquid_1, chartLiquid_2 = _liquid()
    chartPie = _pie()
    chartOverlap = _overlap()

    page = Page(page_title="Covid-19 World vaccinated", layout=Page.DraggablePageLayout)
    page.add(chartBar, chartMap, chartLiquid_1, chartLiquid_2, chartPie, chartOverlap)
    page.render('render.html')


def second_run():
    Page.save_resize_html(source='render.html', cfg_file="chart_config.json", dest="result.html")


if __name__ == '__main__':
    first_run()
    second_run()
```