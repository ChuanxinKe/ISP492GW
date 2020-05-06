import sqlite3
import pandas as pd
import ast
import TerDec as td #个人开发的模块,放在同一文件夹就能正常调用

mission0=td.Mission('初始化变量和输出CSV数据路径是否修改询问')
conn = sqlite3.connect('C:/ISP492GW/copy_only_dont_do_other_things/tweets_sample_data.db')
c = conn.cursor()
one_label = 'created_at'#请在这里更改需要标签,目前不支持嵌套的标签和符号过多数据(e.g.网址)
path='C:/ISP492GW/data_outputs/one_label_'+one_label+'.csv'
outpath=td.setpath(path)
outpath.askupdate('数据输出路径和文件名')
df = pd.read_sql("SELECT * FROM May6",conn)
counter=td.counter(sleep=0,count='已处理tweets: ')
results=[]
mission0.end()

mission1=td.Mission("处理并逐步输出过程sample")
td.printfive(df,"看看读取数据是否成功")

mission2=td.Mission('循环每一行提取label信息')
for index, row in df.iterrows():
    try:
        tweets_label = ast.literal_eval(row['API_return'])
        results.append(str(tweets_label[one_label]))
        counter.flush()
    except:
        pass
td.printfive(results,'label提取结果')
mission2.end()

try:
    mission3=td.Mission('输出csv')
    out=pd.DataFrame(data=results)
    out.to_csv(outpath.path,encoding='gbk')
    mission3.end()
except:
    print('有错误,目前不支持嵌套的标签和符号过多数据(e.g.网址)')

mission1.end()