#-*- coding:utf-8 -*-
# sam1
# datetime:2024-6-02

import datetime
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from sqlalchemy import extract, func
from app.apps import db
from app.models import Purchase, sales, warehouse, goods


def get_verify_code():
    def rnd_color():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
    def gene_text():
        return ''.join(random.sample(string.ascii_letters + string.digits, 4))

    def draw_lines(draw, num, width, height):
        for _ in range(num):
            x1 = random.randint(0, width // 2)
            y1 = random.randint(0, height // 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height // 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype('app/static/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=rnd_color(), font=font)
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    return im, code


# 进货表格
# 进货量
def bar_chart():
    d = db.session.query(func.count(extract('Day', Purchase.purchase_addtime)),
                         extract('Day', Purchase.purchase_addtime)).group_by(
        extract('Day', Purchase.purchase_addtime)
    ).all()
    attr = ["{}号".format(j) for _, j in d]
    v1 = [i for i, _ in d]
    bar = (Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
           .add_xaxis(attr)
           .add_yaxis("采购量", v1)
           .set_global_opts(title_opts=opts.TitleOpts(title="日采购量"),
                            datazoom_opts=[opts.DataZoomOpts()])
           )
    return bar


def line_chart():
    try:
        # 查询数据
        sale = db.session.query(func.count(extract('day', sales.sales_addtime)),
                                extract('day', sales.sales_addtime)).group_by(
            extract('day', sales.sales_addtime)
        ).all()

        # 打印调试信息
        print("Sale Query Results:", sale)

        # 提取数据
        if not sale:
            print("No sales data found.")
            return None

        attr = [str(day) for _, day in sale]
        v1 = [count for count, _ in sale]

        print("Attributes:", attr)
        print("Values:", v1)

        # 创建图表
        line = (Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                .add_xaxis(attr)
                .add_yaxis("销售量", v1, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title="日销售量"))
                )

        return line
    except Exception as e:
        print("Error occurred:", e)
        return None


def pie_chart():
    warehouses = db.session.query(
        func.count(warehouse.warehouse_goods_num).label('count'),
        goods.goods_name
    ).filter(
        warehouse.warehouse_goods_name == goods.goods_name
    ).group_by(
        goods.goods_name  # 改为按商品名称分组
    ).all()

    attr = [i for _, i in warehouses]
    v1 = [j for j, _ in warehouses]

    pie = (Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
           .add("", [list(z) for z in zip(attr, v1)], rosetype="area")
           .set_global_opts(title_opts=opts.TitleOpts(title="仓库库存"))
           .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
           )
    return pie


# 生成编号
def on_created():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum
