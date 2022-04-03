
from pyecharts.charts import Line
from pyecharts import options as opts
from datas import covid_19_data, country_name_map


def _line():
    yaxis_data = [_['value'][0] for _ in covid_19_data]
    xaxis_data = [country_name_map[_['name']] for _ in covid_19_data]
    chart_line = (
        Line()
            .add_xaxis(xaxis_data=xaxis_data)  # x轴数据，[str,str,str]
            .add_yaxis(
            series_name="接种率",
            y_axis=yaxis_data,  # y轴数据[num,num,num]
            markpoint_opts=opts.MarkPointOpts(
                data=[  # 标记
                    opts.MarkPointItem(type_="min"), opts.MarkPointItem(type_="max"),
                    opts.MarkPointItem(name="自定义标记点", coord=[xaxis_data[8], yaxis_data[8]])
                ]
            ),
        )
            .set_global_opts(
            # title_opts=opts.TitleOpts(title="Line-MarkPoint"),  # 标题
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),  # 倾斜x轴
        )
    )

    return chart_line


chartLine = _line()
chartLine.render("line.html")
