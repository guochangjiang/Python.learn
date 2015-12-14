#!/usr/bin/env python3
# --*-- utf-8 --*--

import pandas as pd

# Reading data locally
df1 = pd.read_csv('data.csv')

# Reading data from web
#data_url = "https://raw.githubusercontent.com/alstat/Analysis-with-Programming/master/2014/Python/Numerical-Descriptions-of-the-Data/data.csv"
#df2 = pd.read_csv(data_url)

# Head of the data
print("Head of df1:")
print(df1.head())
print("Head (10) of df1:\n", df1.head(n = 10))
#print("\nHead of df2:")
#print(df2.head())

# Tail of the data
print("\nTail of df1:")
print(df1.tail())
print("Tail (10) of df1:\n", df1.tail(n = 10))

# Extracting column names
print(df1.columns)

# Extracting row names or the index
print(df1.index)

##转置
print("Transposition of df1:\n", df1.T)

##提取特定列
print("The first row is\n", df1.ix[:, 0])
print("The first 5 colomuns of the first row is\n", df1.ix[:, 0].head())

##第11到20行的前3列数据
print(df1.ix[10:20, 0:3])

print(df1.ix[10:20, ['Abra', ]])  # 指定Abra列
print(df1.drop(df1.columns[[1, 2]], axis = 1).head())  # 舍弃列1和列2

## 各列的统计描述
print("\n统计描述：\n", df1.describe())

from scipy import stats as ss
# Perform one sample t-test using 1500 as the true mean
print(ss.ttest_1samp(a = df1.ix[:, 'Abra'], popmean = 15000))
print(ss.ttest_1samp(a = df1, popmean = 15000))

# Import the module for plotting
import matplotlib.pyplot as plt
plt.show(df1.plot(kind = 'box'))

#pd.options.display.mpl_style = 'default' # Sets the plotting display theme to ggplot2
#df1.plot(kind = 'box')

# Import the seaborn library
import seaborn as sns
sns.set_style("darkgrid")
# Load the example tips dataset
#tips = sns.load_dataset("tips")

# Draw a nested boxplot to show bills by day and sex
#sns.boxplot(x="day", y="total_bill", hue="sex", data=tips, palette="PRGn")
#sns.despine(offset=10, trim=True)

 # Do the boxplot
plt.show(sns.boxplot(data = df1))
plt.show(sns.violinplot(data = df1))
plt.show(sns.distplot(df1.ix[:,2], rug = True, bins = 15))
with sns.axes_style("white"):
    plt.show(sns.jointplot(df1.ix[:,1], df1.ix[:,2], kind = "kde"))
plt.show(sns.lmplot("Benguet", "Ifugao", data = df1))
