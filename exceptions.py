class BaseException(Exception):
    """
    API 基类异常。
    """
    def __init__(self, msg: str = "出现了错误，但是未说明具体原因。"):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class VideoListEmptyException(BaseException):
    def __init__(self):
        super().__init__()
        self.msg = "视频列表为空"


class PraseDynamicInfoException(BaseException):
    def __init__(self):
        super().__init__()
        self.msg = "解析动态信息失败"