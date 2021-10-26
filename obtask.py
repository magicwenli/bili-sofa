import yaml
from callback import *
from bilibili_api import user
from config import settings

settings_path = "./settings.yaml"


class ObTask:
    def __init__(self, mid, type, callback, reply, last_update=0, interval=60) -> None:
        self.mid = mid
        self.type = type
        self.callback = eval(callback)
        self.callback_str = callback
        self.reply = reply
        self.last_update = last_update
        self.interval = interval
        self.user = user.User(mid,settings.credit)

    def getObj(self):
        return {
            "mid": self.mid,
            "type": self.type,
            "callback": self.callback_str,
            "reply": self.reply,
            "last_update": self.last_update,
            "interval": self.interval,
        }


class ObTasks:
    tasks: list[ObTask] = []

    def __init__(self) -> None:
        tasks = loadTasks()
        for task in tasks:
            self.tasks.append(ObTask(**task))

    def saveTask(self):
        tasks = []
        for task in self.tasks:
            tasks.append(task.getObj())
        with open(settings_path, "w") as f:
            f.write(yaml.safe_dump(tasks))


def loadTasks():
    with open(settings_path, "r") as f:
        tasks = yaml.load(f, Loader=yaml.FullLoader)
    return tasks


if __name__ == "__main__":
    tasks = ObTasks()
    print(tasks.tasks[0])
    tasks.tasks[0].callback_str = "123"
    tasks.saveTask()
