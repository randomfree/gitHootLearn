# 获取上次的打包时的commitid

import os
import sys
import requests
import json

gitPath = "/Users/ly/aigAndroidSpace/gitLearnPro"
lastIdFilePath = gitPath+"/lastCommitId"

git_get_count_cmd = "git rev-list HEAD --count"

docTag = "[doc]"

# 从git记录中提取commit ID


def getCommitIdFromLine(line):
    return line.split(" ")[0]


def createLastCommitFile():
    file = open(lastIdFilePath, "w")
    file.write("0")
    file.close
    return "0"


def getLastCommitCount() -> str:
    is_exists = os.path.exists(lastIdFilePath)
    print("getLastCommitIdFromFile,isExists:", is_exists)
    if is_exists:
        file = open(lastIdFilePath)
        commit_count: str = file.readline()
        file.close()
        return commit_count
    else:
        count = createLastCommitFile()
        return count


def getMidGitLog(lastCount):
    currentCount = os.popen(f"cd {gitPath} && "+git_get_count_cmd).read()
    midCount = int(currentCount)-int(lastCount)
    logsResult = os.popen(
        f"cd {gitPath} && git log "+"-"+str(midCount)+" --oneline")
    res = logsResult.read()
    logsResult.close()
    return res


def getFormatCommitText(last_count) -> str:
    res = getMidGitLog(last_count)
    commitArr = []
    for line in res.splitlines():
        if line.find(docTag) != -1:
            commitArr.append(line)

    print("需要组织成文字的提交", commitArr)
    if len(commitArr) == 0:
        print("没有需要展示的提交记录")
        sys.exit()

    # packageRecordCommitId = commitArr[len(commitArr)-1].split(" ")[0]

    # print("最后一次提交记录ID", packageRecordCommitId)

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


# def getLastGitCommitId():
#     logsResult = os.popen(f"cd {gitPath} && git log -1 --oneline")
#     return logsResult.read().split(" ")[0]+"\n"


def saveLastCommitId(lastId):
    f = open(lastIdFilePath, "w", encoding='utf8')
    f.write(lastId)
    f.close()
    print("last commit id", lastId)


last_count = getLastCommitCount()
if not last_count:
    print("没有拿到上次提交记录id")
    sys.exit()

print("上次打包的提交记录", last_count)
formatCommitText = getFormatCommitText(last_count)
print("上次打包的提交记录", formatCommitText)
currentCount = os.popen(f"cd {gitPath} && "+git_get_count_cmd).read()
print("currentCommitId:", currentCount)
# status_code = sendMsgByRoboto(formatCommitText, currentCommitId)

# if status_code == 200:
saveLastCommitId(currentCount)
