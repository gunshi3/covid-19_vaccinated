
from pyecharts.charts import Bar
from pyecharts import options as opts
from datas import covid_19_data, country_name_map

percent_min_data = min([_['value'][0] for _ in covid_19_data])
percent_max_data = max([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])


def _bar():
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data][::-1]
    yaxis_data = [round(_['value'][1] / 10000, 2) for _ in covid_19_data][::-1]
    chart_bar = (
        Bar()
            .add_xaxis(xaxis_data)  # 传入x轴的数据, 格式为[1,2,3,4,5]
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
                range_text=['最大值', '最小值'],  # 组件两端的文本
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
    return chart_bar


chart_bar = _bar()
chart_bar.render("bar.html")
