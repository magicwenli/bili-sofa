from obtask import ObTasks, ObTask
from info import Info
from config import settings
from bilibili_api import comment, user
from datetime import datetime
import time
import asyncio


async def loadDynamic(task: ObTask):
    if task.type == "video":
        type_ = comment.ResourceType.VIDEO
        info = await loadVideos(task.user)
        succss, message = await checkSendReply(info, task, type_)
        if succss:
            settings.wxpusher.push(message)


async def checkSendReply(info: Info, task: ObTask, type_: comment.ResourceType):
    old_timestamp = task.last_update
    now_timestamp = datetime.now()
    if int(old_timestamp) < int(info.timestamp):
        resp = ""
        if task.callback_str == "":
            reply = task.reply
        else:
            reply = task.callback(info)
        try:
            resp = await comment.send_comment(reply, oid=info.vid, type_=type_, credential=settings.credit)
            message = "Time: {}\nInfo: {}\nLast Post: {}\nMy Reply: {}".format(
                now_timestamp, resp["success_toast"], info.content.replace("\n", " "), reply.replace("\n", " "))
        except Exception as e:
            print(e)
        task.last_update = info.timestamp
        # tasks
        return True, message
    else:
        message = now_timestamp, "|", info[2].replace("\n", " ")[
            :10], "| 没有更新的动态"
        return False, message


async def loadVideos(user: user.User):
    page = await user.get_videos(0)
    videos = page["list"]["vlist"]
    if len(videos[0]) == 0:
        return Info(0, 0, 0)  # timestamp=0 永远不会回复
    vid = videos[0]["aid"]
    timestamp = videos[0]["created"]
    content = videos[0]["title"]  # use title
    return Info(vid, timestamp, content)


async def startOb(task: ObTask):
    while start_flag:
        await loadDynamic(task)
        time.sleep(task.interval)


async def main():
    # for obt in obts.tasks:
    #     await startOb(obt)
    obt = obts.tasks[0]
    await startOb(obt)


if __name__ == "__main__":
    start_flag = True
    obts = ObTasks()

    asyncio.get_event_loop().run_until_complete(main())
