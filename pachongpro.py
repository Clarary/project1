#测验版本

#过程：
#1.建立会话
#2.用会话模拟登陆（以后所有的get和post都是用这个登陆过的会话进行）
#3.找到选题的div标签,由此得到题目的类型id
#4.根据id返回各个难度题目的数量
#5.根据题目类型id，难度level,数量num得到题目索引index并下载

import requests
import re
import os
import random
from bs4 import BeautifulSoup
import time
import sys
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
username='0918160124'
passwd='0918160124'


#根据题目类型id，难度level,数量num得到题目索引index
def get_index(key,level,num):
    data = {
            'DoType': 'SavePaper4',
            'KnowledgeID': key,
            'LevelID': level,
            'SelectTitleNum': num,
            'TitleScroe': '1',
            'TitleTypeID': '1',
            'sql': '',
            'TID': ''
        }
    count=0
    index=set()
    print("正在获取类型id为{id}难度level为{level}的试题索引，请稍等\n.......................".format(id=key,level=level))
    while len(index)<int(num):
        count+=1
        response=s.post('http://202.197.71.136/xlxt/stk/folder.asp',data=data)
        for ind in response.text.split('|'):
            if not ind=='':
                index.add(ind)
        print('第{count}次获取，共得到{n}道题'.format(count=count,n=len(index)))
        print("索引为：",index)
    
    print("成功!")
    print("共用了{c}次".format(c=count))
    print('题目类型id为：',key)
    print('题目的索引为：',index)
    print('获取题目数量：' , len(index))
    return index

#根据题目索引index下载并写入文件
def download(key,level,index):
    paperContent=''
    for element in index:
        paperContent+=element
        paperContent+='|'
    data = {
            'SaveKindName': '',
            'PaperContent': paperContent
        }
    response=s.post('http://202.197.71.136/xlxt/stk/paper.asp?SaveKindName=',data=data)
    with open('id{id}level{level}.html'.format(id=key,level=level), 'wb') as f:
        f.write(response.content)
        f.close()
    print("下载成功，已保存为\'id{id}level{level}.html\'\n".format(id=key,level=level))

print("欢迎使用网上测试自动筛题系统：\n作者@梁汉文，李仕浩\n版权所有，侵权必究")
for i in range(18):
    sys.stdout.write('.')
time.sleep(1)
print("\n")
#1.建立会话
s = requests.Session()
s.headers.update(headers)
#1.end
#username = input("请输入用户名：")
#passwd = input("请输入密码：")

#2.模拟登陆
while True:
	try:
		post={
					'userName': username,
					'userPw': passwd,
					'userKind': 'student',
					'submit.x': random.randint(0, 20),  # 0-20随机数
					'submit.y': random.randint(0, 20)  # 0-20随机数
				}
		response=s.get('http://202.197.71.136/jpkc/userlogin.asp',params=post)
		break
	except:
		print("登录失败！")
#2.end


#3.找到选题的div标签,由此得到题目的类型id
time.sleep(1)
print("使用说明：使用该系统将题库的题筛选出来并会自动下载至当前目录，用数苑浏览器打开即可")
while True:
    input_id = input("请选择1.高数，2.概率论，3.现代：\n")
    if int(input_id) in [1,2,3]:
        break
print("题目类型及id如下:")
tr_text,img_text=[],[]
with open('id'+input_id+'.html','r',encoding='utf-8')as f:
    bs=BeautifulSoup(f.read(),"lxml")   #to avoid warning, I added this"lxml"
attrs_1={"class":"Ktitle"}
attrs_2={"src":"images/new/fopen.gif"}
tr_ls=bs.find_all('div',attrs_1)
img_ls=bs.find_all('img',attrs_2)

for i in range(len(tr_ls)):
    img_text.append(str(img_ls[i]['id']))
    #img_text=['img_844', 'img_854', 'img_862',...],要将里面的数字提取出来
content="".join(img_text)
totalCount = re.sub("\D", ",", content)
totalCount=totalCount.split(',')
while '' in totalCount:
    totalCount.remove('')
#print(totalCount)#现在totalCount=['844','854','862']

for i in range(len(tr_ls)):
    print("id:"+totalCount[i]+"  "+tr_ls[i].text)

flag=1
while flag:
    key=input('输入要获取的题目的id:(逗号分隔):\n')
    for k in key.split(','):
        if k not in totalCount:
            print('输入题目id错误，请重新输入：\n')
            flag=1
            break
        flag=0
#3.end


#4.根据id返回各个难度题目的数量  
attrs={'style':'color:#FF0000;'}
for k in key.split(','):
    knowledgeID=k
    data = {
            'DoType': 'GetAllTitleNum',
            'KnowledgeID': knowledgeID,
            'TitleTypeID': 1,
            'SQL': ''
         }
    response=s.get('http://202.197.71.136/xlxt/stk/knowledge.asp?',params=data)
    bs=BeautifulSoup(response.text,"lxml")
    span_ls=bs.find_all('span',attrs)
    print('\nid为{k}的题目数量\n易：{s[0].text}\n中下：{s[1].text}\n中：{s[2].text}\n中上：{s[3].text}\n难：{s[4].text}'.format(k=k,s=span_ls))
    #4.end
    
    
    #5.根据题目类型id，难度level,数量num得到题目索引index并下载
    flag=1
    while flag:
        level = input('输入难度(1-5)(逗号分隔):\n')
        for l in level.split(','):
            if int(l) not in [1,2,3,4,5]:
                print('输入难度错误，请重新输入：\n')
                flag=1
                break
            flag=0
    for l in level.split(','):
        index=get_index(key=int(k), level=l, num=span_ls[int(l)-1].text)
        download(key=int(k),level=l,index=index)
    #print(span_ls[int(l)-1])
#5.end