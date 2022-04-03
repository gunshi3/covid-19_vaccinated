
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Pie, Bar, Map, Line, Liquid, Page

from standard_data import covid_19_data, country_name_map

percent_min_data = min([_['value'][0] for _ in covid_19_data])
percent_max_data = max([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])


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
