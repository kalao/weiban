import requests
import re
import json
#主要思路: 课程的完成只需要完成一个课程的学习,就可以请求一个和答案无关的请求
TIMESTAMP="1603097458"#需要更新
USERPID="7dce5a61-e8d4-4cd7-9241-df6b743bdacd"#需要更新
USERID="7e4d4e07-1928-41ac-a3d2-394ecd389554"#需要更新
TOKEN="62eddd9c-020e-449d-af36-0bb92404fb3d"#需要更新
COOKIE=""#需要更新
Headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
"Connection": "keep-alive",
"Cookie": COOKIE,#需要更新
"Host": "weiban.mycourse.cn",
"Origin": "https://weiban.mycourse.cn",
"Referer": "https://weiban.mycourse.cn/",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}
#获得列别列表
URL="https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp="+TIMESTAMP+"&"+"userProjectId="+USERPID+"&chooseType=3&userId="+USERID+"&tenantCode=43000010&token="+TOKEN
response = requests.get(URL,headers=Headers,timeout=60)
categoryids=re.findall(r"""\{"categoryCode":"(.*?)",""",response.text)
total=""
for categoryid in categoryids:
    #获得课程列表
    URL="https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp="+TIMESTAMP+"&userProjectId="+USERPID+"&chooseType=3&categoryCode="+categoryid+"&name=&userId="+USERID+"&tenantCode=43000010&token="+TOKEN
    response = requests.get(URL,headers=Headers,timeout=60)
    total=total+response.text
userCourseIds=re.findall(r"""\{"userCourseId":"(.*?)",""",total)
resourceIds=re.findall(r""","resourceId":"(.*?)",""",total)
for resourceId,userCourseId in zip(resourceIds,userCourseIds):
    data={
        'courseId':resourceId,
        'userProjectId':USERPID,
        'tenantCode':'43000010',
        'userId':USERID,
        'token':TOKEN
    }
    #首先进行学习请求
    study="https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp="+TIMESTAMP
    requests.post(study,headers=Headers,data=data)
    #结课请求
    success="https://weiban.mycourse.cn/pharos/usercourse/finish.do?userCourseId="+userCourseId+"&tenantCode=43000010"
    requests.get(success,headers=Headers)
