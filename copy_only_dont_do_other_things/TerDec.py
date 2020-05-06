'''
Needs pandas.
'''

"""
This is a terminal decoration module. It aims at building a fresher-friendly presentation of terminal outputs.
However it can also be used to replace some of the notes, so it won't bring to many burdens to developers and lines to script.
The author also believes that it helps to debug by using from the beginning. Let your terminal talking!!!

By the way, it takes your machine some time to do so.
>>>if you are starter: 
       it won't slow your script too much! Don't worry!
   elif:
       I believe you will use it wisely.

Table of Contents

1. Path Configuration Setting when Transplanted
2. Mission Reply
3. Count in a Flush Manner
4. Print First 5 Items of dict, list, string, tuple (pandas also supported)

Copyright: kcxwdzx@sina.com                    Last Modify Date:05/05/2020

"""
#Import--------------
import timeit
import time
import pandas

# For special support of pandas
a={"name":['google','baidu'],"price":[1,2]}
pddate=pandas.DataFrame(a)

# Path Configuration Setting when Transplanted-------------
class setpath:
    #You have to set path to create one.
    def __init__(self, path):
        self.path=path
    
    #Just put new file name inside new path.
    #reminder is optional, default as:'Current path'
    def askupdate(self,reminder='Current path'):
        while True:
            print(reminder+': '+ self.path)
            change = input("Do you want to change? (y/n): ")
            if change == 'y':
                self.path = input('Please put new path here:')
                print ("\nNew path is set as: " + self.path + "\nThank You!\n")
                break
            elif change == 'n':
                print ("\nThis path is kept.Thank You!\n")
                break
            else:
                print('\nONLY y or n is accepted. Please try again.')

# Mission Reply----------------
class Mission:
    # begintime is used to get how many seconds are used so far.
    begintime = timeit.default_timer()
    # mis is optional for mission name. Default as:""
    def __init__(self, mis=""):
        self.mis = mis
        self.starttime = timeit.default_timer()
        print('\n>>>> MISSION: '+ self.mis +' >>>>\n')
    
    # print the time this mission used and so far since initial.
    def end(self):
        self.endtime = timeit.default_timer()
        interval = format(self.endtime-self.starttime,'.5f')
        sofar = format(self.endtime-self.begintime,'.5f')
        print('\n<<<< End: '+ self.mis + ' , USE: '+interval + ' , SO FAR: ' + sofar + ' S <<<<\n')

# Count in a Flush Manner--------------------
class counter:
    # Default: sleep 0.01s each count, print'Count:' and start from 0. "
    def __init__(self, sleep=0.01, count='Count: ',number=0):
        self.sleep=sleep
        self.count=count
        self.number=number

    # Count the number and print it in a flush way by [end='\r'].
    # So it may be disturbed by other print.  
    def flush(self):
        self.number=self.number+1
        print(self.count+str(self.number),end='\r')
        time.sleep(self.sleep)


def printfive(results, description="the target data"):
# Print first 5 items of dict, list, string, tuple, pandas.series----------------------
# description is optional. Default as: "the target data"   
    print('\nprint 5 samples - : ' + description)
    print(type(results))
    try:
        if type(results)==type({"he":1}):
            a=list(results.items())[:5]
            print(a)
            print('Notes: Although print as list, it did not change actually.')
        
        elif type(results)==type(pddate):
            print(results[0:5])

        elif len(results)<5:
            for i in range(len(results)):
                print(results[i])

        else:           
            for i in range(5):
                print(results[i])
    except:
        print('Please check data. Only dict, list, string, tuple, pandas.series, pandas.dataframe are support!')

###Internal Test-----------------------
if __name__== '__main__':
    mission0 = Mission('Internal Test')

    mission1=Mission('set path when changing files')
    path1 = setpath("C:/user/coda.csv")
    path2 = setpath('/file/output/dashboard.png')
    path1.askupdate('This path is for input data')
    path2.askupdate('This path is for out put figure')
    mission1.end()
    
    mission2 = Mission('loop 500 times')
    c=counter()
    for i in range(500):
        c.flush()
    mission2.end()

    mission3=Mission('present different data sample')
    sample1 = ('North','South','West','East')
    sample2 = 'hello'
    sample3 = [1,2,3,4,5,6,7]
    sample4 = {"David":"UK", "Mike":"US", "James":"Japen","Tim":"US","Robert":"US","Chris":"China"}
    sample5 = set(["London","New York","Manchster","Leeds","Loughborough","Surry"])
    printfive(sample1,'sample1-position(tuple,4 items)')
    printfive(sample2,'sample2-hello(string, 5 items)')
    printfive(sample3, 'sample3-number(list, 7 items)')
    printfive(sample4, 'sample4-homenation(dict, 6 items)')
    printfive(sample5,'sample5-city(set, error here)')
    printfive(sample5)
    mission3.end()

    mission0.end()