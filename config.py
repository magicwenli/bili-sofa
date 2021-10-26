import yaml
from wxpusher import WxPusher
from bilibili_api import Credential
# from ob import ObsClass


class Pusher:
    def __init__(self, uids=None, topic_ids=None, token=None):
        self.config = {
            "uids": uids,
            "topic_ids": topic_ids,
            "token":  token
        }

    def push(self, content):
        WxPusher.send_message(content, **self.config)


class Setting:
    def __init__(self, credit, wxpusher) -> None:
        self.credit = Credential(**credit)
        self.wxpusher = Pusher(**wxpusher)


def loadConfig():
    secret_path = "./.secrets.yaml"

    credit = ''
    wxpusher = ''

    with open(secret_path, "r") as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        credit = config["credential"]
        wxpusher = config["wxpusher"]

    return Setting(credit, wxpusher)



settings = loadConfig()



if __name__ == "__main__":
    print(settings.wxpusher.config)
