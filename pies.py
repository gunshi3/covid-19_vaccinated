
from pyecharts.charts import Pie
from pyecharts import options as opts
from datas import covid_19_data, country_name_map


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
    return chart_pie


chartPie = _pie()
chartPie.render()
