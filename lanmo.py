import requests
import json
import time
import random
import re
import os
Notice_Url = os.environ["Notice_Url"]
login_credits = os.environ["credits"]
course_id=os.environ["course_id"]
print(login_credits)
def send_vote(event_id,topic_id):
    url = "https://www.mosoteach.cn/web/index.php?c=interaction_vote&m=save_answer"

    payload = {'id': event_id,
    'type': 'VOTE',
    'data': '[{"topic_id":"'+topic_id+'","choice":["'+str(random.randint(5,6))+'"],"content":""}]',
    'clazz_course_id': course_id}
    
    headers = {
    'Cookie': 'login_token='+login_token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    print(payload)
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text)
    response = requests.request("GET", Notice_Url+"自动打卡已完成！")
def get_vote(url):
    if(url==""):
        return
    regex = (r"(?<=&id=).*?(?=&)")
    matches = re.finditer(regex, url, re.DOTALL)
    event_id=""
    for matchNum, match in enumerate(matches, start=1):
        event_id=match.group()
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

    headers = {
    'Cookie': 'login_token='+login_token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data = payload, files = files)
    regex = (r"(?<=data-topic-id=\").*?(?=\")")
    matches = re.finditer(regex, response.text, re.DOTALL)
    topic_id=""
    for matchNum, match in enumerate(matches, start=1):
        topic_id=match.group()
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    send_vote(event_id,topic_id)
    #print(response.text)
url = "https://www.mosoteach.cn/web/index.php?c=passport&m=account_login"

payload = login_credits
files = [

]
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

login_response=json.loads(response.text)
print(response.text)
#print(login_response["user"]["app_token"])
login_token=login_response["user"]["app_token"]
has_new_event=-1
while (has_new_event<0):
    url = "https://www.mosoteach.cn/web/index.php?c=interaction&m=index&clazz_course_id="+course_id+"&keyword=&status=IN_PRGRS"

    payload = {}
    headers = {
    'Cookie': 'login_token='+login_token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    has_new_event=response.text.find("color:#EC6941;")
    print(response.text.find("color:#EC6941;"))
    if (has_new_event>-1):
        break
    time.sleep(90)

regex = r"(?<=<span class=\"interaction-status processing\">进行中<\/span>).*?(?=<\/span>)"
test_str=response.text
matches = re.finditer(regex, test_str, re.DOTALL)
detail=""
for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    detail=detail+match.group()
regex = r"(?<=<span class=\"interaction-name grey fontsize-14 color-33\" title=\").*?(?=\">)"


matches = re.finditer(regex, detail, re.DOTALL)
detail=""
for matchNum, match in enumerate(matches, start=1):
    detail=detail+match.group()+" "
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
print(detail)
response = requests.request("GET", Notice_Url+"老师在蓝墨云班课发布了新的活动，请及时完成！活动名称："+detail)

regex = (r"(?<=data-row-status=\"IN_PRGRS\"\n"
	r"                                                data-id=\").*?(?=\">)")
#print(response.text)
matches = re.finditer(regex, response.text, re.DOTALL)
tpurl=""
for matchNum, match in enumerate(matches, start=1):
    tpurl=tpurl+match.group()+"@"
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
regex = (r"(?<=data-url=\")https:.*?(?=@)")
matches = re.finditer(regex, tpurl, re.DOTALL)
for matchNum, match in enumerate(matches, start=1):
    get_vote(match.group())
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
