# __all__ = ["A"]


class A():
    # 定义类方法与普通函数不一样，定义类方法必须至少有一个参数
    # 通常是self(可以改成其他，但是在 python 界默认是self，虽然可以改，但不建议改)
    def say(self, name):
        print("heelo,test.py" + name, "\t", name)
