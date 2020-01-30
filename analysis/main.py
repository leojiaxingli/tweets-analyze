import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    # 构建数据
    x_data = ['2011', '2012', '2013', '2014', '2015', '2016', '2017']
    y_data = [58, 60, 63, 71, 84, 90, 100]
    y_data2 = [52, 54, 51, 58, 56, 59, 62]
    bar_width = 0.3
    # 将X轴数据改为使用range(len(x_data), 就是0、1、2...
    plt.bar(x=range(len(x_data)), height=y_data, label='C语言基础',
            color='steelblue', alpha=0.8, width=bar_width)
    # 将X轴数据改为使用np.arange(len(x_data))+bar_width,
    # 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了
    plt.bar(x=np.arange(len(x_data)) + bar_width, height=y_data2,
            label='Java基础', color='indianred', alpha=0.8, width=bar_width)
    # 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
    for x, y in enumerate(y_data):
        plt.text(x, y + 100, '%s' % y, ha='center', va='bottom')
    for x, y in enumerate(y_data2):
        plt.text(x + bar_width, y + 100, '%s' % y, ha='center', va='top')
    # 设置标题
    plt.title("C与Java对比")
    # 为两条坐标轴设置名称
    plt.xlabel("年份")
    plt.ylabel("销量")
    # 显示图例
    plt.legend()
    plt.show()