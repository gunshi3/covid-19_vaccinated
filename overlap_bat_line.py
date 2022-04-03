
from pyecharts import options as opts
from pyecharts.charts import Bar, Line

from datas import covid_19_data_, country_name_map,covid_19_data

percent_min_data = min([_['value'][0] for _ in covid_19_data])
percent_max_data = max([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])

xaxis_data = [country_name_map[_['name']] for _ in covid_19_data_]
yaxis_one_data = [_['value'][0] for _ in covid_19_data_]
yaxis_two_data = [round(_['value'][1] / 10000, 2) for _ in covid_19_data_]


def _overlap():
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data_]
    yaxis_one_data = [_['value'][0] for _ in covid_19_data_]
    yaxis_two_data = [round(_['value'][1] / 10000, 2) for _ in covid_19_data_]
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
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示柱状图上面的字
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value} 万"),  # 显示的y轴
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),  # 倾斜x轴
        )
    )
    #
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
                    opts.MarkPointItem(name="自定义", coord=[xaxis_data[0], yaxis_one_data[0]], value=yaxis_one_data[0])
                ]
            )
        )
    )
    chart_overlap.overlap(line)
    return chart_overlap


chartOverlap = _overlap()
chartOverlap.render("overlap_bar_line.html")
