from initailData import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 销售员列表
salesmanArr = np.array(list(salesmen.keys()))  # dict.keys()返回的是迭代器而不是List
# 每个销售员全年销售总额
totalArr = np.array(quarterSales).sum(axis=0)
# 按团队进行统计全年销售总额
teamTotalFrame = pd.DataFrame({
	'team': teamBelong,
	'sales': totalArr
})
# 分别输出各团队的销售总数
print('各团队的销售总数')
print(teamTotalFrame.groupby(teamTotalFrame['team']).sum())
# 销售总额的前五名
print("\n销售额前五名: ", end='')
for eachSalesman in salesmanArr[totalArr.argsort()[-5:]]:
	print(eachSalesman, end=' ')
# 销售总额的后三名
print("\n销售额后三名: ", end='')
for eachSalesman in salesmanArr[totalArr.argsort()[:3]]:
	print(eachSalesman, end=' ')
# 找出销售总额超过14000的销售员
print("\n销售总额超过14000的销售员: ", end='')
for eachSalesman in salesmanArr[totalArr > 14000]:
	print(eachSalesman, end=' ')
# 各职称在各团队中每个季度的销售
print("\n\n各团队中每个季度的销售")
teamSalesFrame = pd.DataFrame({
	'position': list(salesmen.values()),
	'team': teamBelong,
	'Q1': quarterSales[0],
	'Q2': quarterSales[1],
	'Q3': quarterSales[2],
	'Q4': quarterSales[3],
	'total': totalArr
})
print(teamSalesFrame.groupby(['position', 'team']).sum())
# 直方图显示
data = teamSalesFrame.groupby(['team', 'position']).sum().to_numpy()

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 和负号正常显示

# 绘制条形图
xLabel = ['A:Junior', 'A:Senior', 'B:Junior', 'B:Senior', 'C:Junior', 'C:Senior']
groupItemLabel = ['Q1', 'Q2', 'Q3', 'Q4', 'Total']
xBase = range(0, len(xLabel) * 2, 2)
xWidth = 0.35
colors = ['deeppink', 'orange', 'yellow', 'springgreen', 'deepskyblue']

rectangles = []
for index in range(len(groupItemLabel)):
	rectangles.append(plt.bar(
		x=[i + index * xWidth for i in xBase],
		height=data[:, index:index + 1].reshape(6),
		width=xWidth,
		color=colors[index],
		label=groupItemLabel[index]
	))
# y轴取值范围
plt.ylim(
	min(map(lambda arr: min(arr), data)) - 3000,
	max(map(lambda arr: max(arr), data)) + 5000
)
plt.ylabel("销售额")

# 设置x轴刻度显示值
# 参数一：中点坐标
# 参数二：显示值
plt.xticks([i + (xWidth * len(groupItemLabel) / 2 - xWidth / 2) for i in xBase], xLabel)
plt.xlabel("职称 & 团队")
plt.title("各职称在各团队中每个季度的销售")
# 设置题注
plt.legend()
# 编辑文本
for recArr in rectangles:
	for rec in recArr:
		height = rec.get_height()
		plt.text(
			rec.get_x() + rec.get_width() / 2,
			height + 1000, str(height),
			ha="center", va="bottom"
		)
plt.show()
