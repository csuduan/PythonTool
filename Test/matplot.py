import matplotlib.pyplot as plt
import numpy as np

#plot说明  https://matplotlib.org/2.2.2/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot

#图1
x = np.linspace(0, 2, 100)
plt.subplot(231)
plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')
plt.title("Simple Plot")
plt.legend()


#图2
plt.subplot(232)
t = np.arange(0., 5., 0.2)
# red dashes, blue squares and green triangles
# 参数具体见https://matplotlib.org/2.2.2/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.xlabel('x label',fontsize=14, color='red')
plt.ylabel('y label')
plt.axis([0, 1, 0, 1])  #坐标轴范围
plt.yscale('linear')
plt.title('linear')


#图3
plt.subplot(233)
x=[1,2,3,4,5]
y=[0,1,2,3,4]
plt.scatter(x, x)   # 点图
plt.bar(x, y)       #直方图
plt.text(2,4,r'hahah')  #文本
plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.grid(True)          #网格


#图4
plt.subplot(234)
t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2*np.pi*t)
upper = 0.77
lower = -0.77
supper = np.ma.masked_where(s < upper, s)
slower = np.ma.masked_where(s > lower, s)
smiddle = np.ma.masked_where(np.logical_or(s < lower, s > upper), s)
plt.plot(t, smiddle, t, slower, t, supper)



plt.suptitle('Plot Demo')
plt.show()