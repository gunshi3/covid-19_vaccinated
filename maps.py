
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from datas import covid_19_data, country_name_map

percent_min_data = min([_['value'][0] for _ in covid_19_data])
percent_max_data = max([_['value'][0] for _ in covid_19_data])
vaccinated_min_data = min([_['value'][1] for _ in covid_19_data])
vaccinated_max_data = max([_['value'][1] for _ in covid_19_data])


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

    return chart_map


chartMap = _map()
chartMap.render()
