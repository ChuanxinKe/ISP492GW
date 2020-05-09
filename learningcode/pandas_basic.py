import numpy as np
import pandas as pd
import TerDec as td

mission0=td.Mission('pandas基础操作')

mission1=td.Mission('制作并展示series数据结构')
dataset1=pd.Series([1,2,3,np.nan,5,6,7,8,np.nan])
td.printfive(dataset1)
mission1.end()

mission2=td.Mission('制作并展示DataFrame数据结构,随机方式生成,时间为主键,打印前后五,某列')
dates=pd.date_range('20200410',periods=10)
dataset2 = pd.DataFrame(np.random.rand(10,4), index=dates, columns=['A','B','C','D'])
print('\n输出前五条')
print(dataset2.head())
print('\n输出后五条')
print(dataset2.tail())
td.printfive(dataset2['B'],'Only column B')
mission2.end()

mission3=td.Mission('转化为numpy的array')
td.printfive(dataset2.to_numpy())
mission3.end()

mission4=td.Mission('用python字典创建标准dataframe')
standard_data = {"name":['google','baidu','yahoo'],"marks":[100,200,300],"price":[1,2,3]}
dataset3=pd.DataFrame(standard_data)
print(dataset3.head())
mission4.end()

mission5=td.Mission('同维度不对等数据,随机数生成,并进行运算')
dataset4 = pd.DataFrame({'amount': pd.Series(np.random.randn(3), index=['apple', 'banana', 'coconut']),
                    'price': pd.Series(np.random.randn(4), index=['apple', 'banana', 'coconut', 'durian']),
                    'weight': pd.Series(np.random.randn(3), index=['banana', 'coconut', 'durian'])})
print(dataset4)
print('开始运算')
row = dataset4.iloc[1]
column = dataset4['price']
print('\n行相减1')
print(dataset4.sub(row, axis='columns'))
print('\n行相减2')
print(dataset4.sub(row, axis=1))
print('\n列相减1')
print(dataset4.sub(column, axis='index'))
print('\n列相减2')
print(dataset4.sub(column, axis=0))
mission5.end()

mission6=td.Mission('多层索引展示')
dfmi = dataset4.copy()
dfmi.index = pd.MultiIndex.from_tuples([('UK', 'apple'), ('UK', 'banana'),
                                        ('UK', 'coconut'), ('France', 'apple')],
                                        names=['country', 'fruit'])
print(dfmi)
mission6.end()

mission0.end()
