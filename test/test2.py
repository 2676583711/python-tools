# 从包名.文件名 导入类A
from tools.test.test import A

from email_accidence.testEmail import email

# python的main方法：程序入口方法
if __name__ == '__main__':
    a = A()
    a.say("789")
    e=email()
    e.send()
