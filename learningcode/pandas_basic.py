import numpy as np
import pandas as pd
import TerDec as td

mission0=td.Mission('开始pandas基础操作')

mission1=td.Mission('制作并展示series数据结构')
dataset1=pd.Series([1,2,3,np.nan,5,6,7,8,np.nan])
td.printfive(dataset1)
mission1.end()

mission2=td.Mission('制作并展示DataFrame数据结构,随机方式生成,时间为主键')
dates=pd.date_range('20200410',periods=10)
dataset2 = pd.DataFrame(np.random.rand(10,4), index=dates, columns=['A','B','C','D'])
td.printfive(dataset2,'All columns')
td.printfive(dataset2['B'],'only column B')
mission2.end()

mission3=td.Mission('用字典创建标准dataframe')
standard_data = {"name":['google','baidu','yahoo'],"marks":[100,200,300],"price":[1,2,3]}
dataset3=pd.DataFrame(standard_data)
td.printfive(dataset3,'Only 3 rows, so show 3')
mission3.end()