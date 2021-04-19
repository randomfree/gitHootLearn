# 获取上次的打包时的commitid

import os
import sys
import requests
import json

gitPath = "/Users/ly/aigAndroidSpace/gitLearnPro/"
lastIdFilePath = gitPath+"lastCommitId"

docTag = "[doc]"

# 从git记录中提取commit ID


def getCommitIdFromLine(line):
    return line.split(" ")[0]


def createLastCommitFile():
    file = open(lastIdFilePath, "w")
    logs = os.popen(f"cd {gitPath} && git log -1000 --oneline")
    logRes = logs.read()
    last_id = ""
    for line in logRes.splitlines():
        last_id = getCommitIdFromLine(line)

    if len(last_id) == "0":
        print("获取1000次以前的那次提交的id出错")
        sys.exit()
    file.write(last_id)
    file.close
    return last_id


def getLastCommitIdFromFile() -> str:
    is_exists = os.path.exists(lastIdFilePath)
    if is_exists:
        file = open(lastIdFilePath)
        commit_id: str = file.readline()
        file.close()
        return commit_id
    else:
        firstId = createLastCommitFile()
        return firstId


def getFormatCommitText(lastId) -> str:
    print("getFormatCommitText", "lastId:", lastId)
    logsResult = os.popen(f"cd {gitPath} && git log -1000 --oneline")

    res = logsResult.read()
    commitArr = []
    for line in res.splitlines():
        currentCommitId = getCommitIdFromLine(line)
        if currentCommitId in lastId:
            print("currentCommitId 相等")
            break
        if line.find(docTag) != -1:
            commitArr.append(line)

    print("需要组织成文字的提交", commitArr)
    if len(commitArr) == 0:
        print("没有需要展示的提交记录")
        sys.exit()

    packageRecordCommitId = commitArr[len(commitArr)-1].split(" ")[0]

    print("最后一次提交记录ID", packageRecordCommitId)

    commitText = ""
    index = 0
    while index < len(commitArr):
        commitText += '%d' % (index+1)+"."
        commitMessage = commitArr[index].split(" ")[1]
        commitText += commitMessage[commitMessage.find("]")+1:]
        commitText += "\n"
        index += 1

    return commitText


def sendMsgByRoboto(text, lastCommitId):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/df283ce5-bbc5-48f5-8d45-9bc789247787"

    headers = {"Content-Type": "application/json"}

    sendText = "commit_id:"+lastCommitId+"\n"+text

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "更新记录:",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": sendText
                            }
                        ]
                    ]
                }
            }
        }
    }

    # print("sendText", sendText)
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("发送机器人", r.status_code)
    return r.status_code


def getLastGitCommitId():
    logsResult = os.popen(f"cd {gitPath} && git log -1 --oneline")
    return logsResult.read().split(" ")[0]+"\n"


def saveLastCommitId(lastId):
    f = open(lastIdFilePath, "w", encoding='utf8')
    f.write(lastId)
    f.close()
    print("last commit id", lastId)


lastId = getLastCommitIdFromFile()[:9]
if not lastId:
    print("没有拿到上次提交记录id")
    sys.exit()

print("上次打包的提交记录", lastId)
formatCommitText = getFormatCommitText(lastId)
print("上次打包的提交记录", formatCommitText)
currentCommitId = getLastGitCommitId()
print("currentCommitId:", currentCommitId)
# status_code = sendMsgByRoboto(formatCommitText, currentCommitId)

# if status_code == 200:
saveLastCommitId(currentCommitId)
