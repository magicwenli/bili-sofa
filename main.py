from obtask import ObTasks, ObTask
from info import Info
from config import Pusher, settings, replyTemplate
from bilibili_api import comment, user
from datetime import datetime
import asyncio
import random
from log import logger
from exceptions import PraseDynamicInfoException

DEBUGMODE = False

async def startTask(task: ObTask):
    while start_flag:
        sleep_seconds = random.randint(10, task.interval)
        if task.type == "video":
            type_ = comment.ResourceType.VIDEO
            info = await loadVideos(task.user)
            await checkSendReply(info, task, type_)
        elif task.type == "dynamic":
            type_ = comment.ResourceType.DYNAMIC
            info = await loadDynamics(task.user)
            await checkSendReply(info, task, type_)
        logger.info("{}: sleep {} seconds.".format(task.tid,sleep_seconds))
        await asyncio.sleep(sleep_seconds)
        # return
        # return "{}: task {} wait {} s.".format(datetime.now(), task.mid, task.interval)


async def checkSendReply(info: Info, task: ObTask, type_: comment.ResourceType):
    old_timestamp = task.last_update
    if int(old_timestamp) < int(info.timestamp):
        logger.info("{}: New dynamic detacted. Create: {}, Content:{:<}".format(
            task.tid, datetime.fromtimestamp(info.timestamp).strftime("%Y--%m--%d %H:%M:%S"), info.content))
        resp = ""
        if task.callback_str == "":
            reply = task.reply
        else:
            reply = task.callback(info)
        try:
            logger.info("{}: Send commnet. Type: {}, Contnet:{}".format(
                task.tid, task.type, reply))
            resp = await comment.send_comment(reply, oid=info.vid, type_=type_, credential=settings.credit)
            logger.info("{}: Response. Toast: {:<}".format(
                task.tid, resp["success_toast"]))
        except Exception as e:
            logger.warning(e)

        if not DEBUGMODE:
            task.last_update = info.timestamp
            obts.saveTask()

        logger.info("{}: Pushing to wx.".format(task.tid))
        settings.wxpusher.push(replyTemplate(info, reply))

        return
    else:
        logger.info("{}: Nothing happend. Last Update: {}".format(task.tid,task.getLastUpdate()))
        return


async def loadVideos(user: user.User):
    page = await user.get_videos(0)
    videos = page["list"]["vlist"]
    if len(videos[0]) == 0:
        logger.info("No newer video.")
        return Info(0, 0, 0)  # timestamp=0 永远不会回复
    vid = videos[0]["aid"]
    timestamp = videos[0]["created"]
    content = videos[0]["title"]  # use title
    description = videos[0]["description"]
    uname = await user.get_user_info()
    return Info(vid, timestamp, content, description, uname=uname["name"])


async def loadDynamics(user: user.User):
    page = await user.get_dynamics(0)
    if "cards" in page:
        try:
            dynamic = page["cards"][0]
            did = dynamic["desc"]["dynamic_id"]
            timestamp = dynamic["desc"]["timestamp"]
            if dynamic["desc"]["type"] == 2:
                content = dynamic["card"]["item"]["description"]
                uname = dynamic["card"]["user"]["name"]
            else:
                content = dynamic["card"]["item"]["content"]
                uname = dynamic["card"]["user"]["uname"]
            return Info(did, timestamp, content, uname=uname)

        except KeyError:
            raise PraseDynamicInfoException()

    else:
        logger.info("No newer dynamic.")
        return Info(0, 0, 0)  # timestamp=0 永远不会回复


if __name__ == "__main__":
    start_flag = True
    obts = ObTasks()
    tasks = [asyncio.ensure_future(startTask(obt)) for obt in obts.tasks]
    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
    # for task in tasks:
    #     print('Task ret: ', task.result())
