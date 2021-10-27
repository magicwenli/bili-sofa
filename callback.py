from info import Info
import random

def cb1(info:Info):
    return info.content[::-1]+str(random.randint(999,999999))

if __name__=="__main__":
    a=eval("cb1")
    info=(1,112,"ccccc")
    print(a(info))