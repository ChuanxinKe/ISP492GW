# BSP417 WEEK 2 PART 3 OF CODA APP: 
# use case: iterate through f500 tickers and obtain closing prices over a period of time, 

# LIBRARIES: -------------------
import pandas as pd 
import pandas_datareader.data as web 
import datetime as dt
import TerDec as td #个人开发的模块,放在同一文件夹就能正常调用
# VARIABLES: -------------------
mission0=td.Mission('初始化变量和输出CSV数据路径是否修改询问')
f500_url = "https://query.data.world/s/vjghzuarkh6dap3dblkxanppyh5jtl" 
source = "yahoo" 
start_date = dt.datetime(2020, 4, 1) #set what you like here
end_date = dt.datetime.now()    
results = [] #potential issue here is that multiple datatypes come from datareader. so you need to ensure read data is parsed to string in order to buffer to this list. also, remember that lists are one-dimensional, so can only take one variable. Need a Dict for multi col. Here we create a csv line/record, i.e. fields concatenated with commas.
outpath=td.setpath('/Users/yuhaihong/Desktop/Jemma/IMBT/Data Science.csv')
outpath.askupdate('数据输出路径和文件名')
mission0.end()
# MAIN : --------------------
mission1=td.Mission('获取并输出股票数据(主程序)')

mission2=td.Mission('从某神秘网址获取,不知道哪年的财富500强CSV数据')
df500 = pd.read_csv(f500_url)
mission2.end()
#loop through the tail (see pandas lab) of returned dataframe (for expedience, feel free to delete the tail method if you want the whole lot)

mission3=td.Mission('就排名尾部[tail()]的5个财富500强企业,逐个去Yahoo.com抓取历史收盘数据')
counter1=td.counter()
for index, row in df500.tail().iterrows(): 
    try: #always 'try' connections, in case they fail, so the loop doesnt fail altogether.
        dfdr = web.DataReader(row['SYMBOL'], source, start_date, end_date).reset_index() #reset index here so that date is included in the output.         
        for index2, row2 in dfdr.iterrows():
                results.append(str(row['SYMBOL'])+","+str(row2['Date'])+","+str(row2['Close']))
                counter1.flush()
    except Exception as e: #catch any exceptions i.e. if the 'try' failed
        pass
mission3.end()

mission4=td.Mission('输出数据示例')
td.printfive (results,'瞅瞅前五个收盘数据长啥样')
mission4.end()

mission5=td.Mission('简单格式化并导出CSV')
out=pd.DataFrame(data=results)
out.to_csv(outpath.path,encoding='gbk')
mission5.end()

mission1.end()

# this last command outputs what may look a mess to you, but its the humble beginnings of something rather useful, i.e. its a way of producing csv data that you could pipe to a file/source for future analytics.
# Next week we will look at storing this all into an SQL database. 
# For now, if you want to stretch yourself, try storing the results list into a file.
#/P