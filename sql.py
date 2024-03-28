#!/usr/bin/env python

import requests
import sys
import argparse
import re

Version = "sql-scan Tool V1.0.0"
Title = '''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it for illegal purposes, or you will bear corresponding legal responsibilities
************************************************************************************'''
Logo = f'''
                Github==>https://github.com/interstin/sql-scan 
                {Version}  '''

def get(url,payload):
    result = requests.get(url=url+payload).text
    return result


def post(url,payload,data):
    result = requests.post(url,data=data+payload).text
    return result

def scan(url,method,data):
    with open('payload.txt','r') as file:
        for line in file:
            payload = line
            print("payload为：",payload)
            if data==None:
                data =''
                result = {
                    'post':post(url,payload,data)
                }.get(method,get(url,payload))
                print(result.decode('utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url",required=True, help="URL to scan")
    parser.add_argument("-M","--method",default='get',help="get or post or others method,default is get")
    parser.add_argument("-D","--data",help="the data that you want to post")
    args = parser.parse_args()

    if args.url==None:
        print("请指定你要访问的地址:\n如test.py -u http://xxxxx") 
    elif not re.search(r"(?i)\Ahttp[s]*://", args.url):
        args.url = "http://%s" % args.url 
        print("你访问的url为：",args.url)
    
    scan(args.url,args.method,args.data)



if __name__=='__main__':
    print(Logo,'\n')
    main()