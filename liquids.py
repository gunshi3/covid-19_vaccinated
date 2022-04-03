
# 最大最小值
# 4个球

from pyecharts import options as opts
from pyecharts.charts import Liquid

from datas import covid_19_data

percent_max_data = max([_['value'][0] for _ in covid_19_data])
percent_min_data = min([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])


def _liquid():
    percent_max = (
        Liquid().add(
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
        Liquid().add(
            series_name="最低比率",
            data=[percent_min_data / 100, 0.3],  # 第一个值为显示的值，第二个值为水的分量
            center=["25%", "25%"],
            is_outline_show=False
        )
    )

    return percent_max, percent_min


percent_max_, percent_min_ = _liquid()
percent_max_.render('liquid_1.html')
percent_min_.render('liquid_2.html')
