import smtplib
import sys
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from imp import reload


class EmailUtils:

    def __init__(self, filepath, sender, receiver, subject):
        self.filepath = filepath
        self.sender = sender
        self.receiver = receiver
        # self.filename = filename
        self.subject = subject

    def sendWithAtachment(self):
        # 发送带附件的邮件使用　MIMEMultipart邮件体
        msg = MIMEMultipart('utf-8')
        # msg.add_header("Content-Type", 'html/text; charset="utf-8"')

        # 设置编码为utf-8
        msg.set_charset("UTF-8")
        print(msg.get_charset())

        # 设置发件人
        msg['from'] = self.sender
        # 设置收件人
        msg['to'] = self.receiver
        # 设置此邮件的主题
        msg['subject'] = self.subject

        # 从文件路径中截取文件名
        name = self.filepath.split("/")[len(self.filepath.split("/")) - 1]
        with open(self.filepath, 'r')as f:
            # 构建附件
            attachment = MIMEBase(name, 'txt/html', filename=name)
            print(name)

            # 加载文件到附件中
            attachment.set_payload(f.read())
            # 设置附件的名称
            attachment["Content-Disposition"] = 'attachment;filename="' + name + '"'

        # 把附件添加到邮件体中
        msg.attach(attachment)

        # 使用smtplib模块发送邮件
        smtp = smtplib.SMTP("smtp.163.com", 25)
        # 登录smtp服务器
        smtp.login(self.sender, "zhou123456")
        # 发送邮件
        try:
            smtp.sendmail(self.sender, self.receiver, msg.as_string().encode("utf-8"))
        except:
            msg.set_charset("GBK")
            smtp.sendmail(self.sender, self.receiver, msg.as_string().encode("utf-8"))

        # 发送完毕退出登录
        smtp.quit()
        print("send email is OK")


if __name__ == '__main__':
    fileName = "/home/zhou/a.txt"
    filepath = "/home/zhou/美漫世界的武者.txt"

    eu = EmailUtils(filepath, "liberalzhou@163.com",
                    "15171683953@163.com", "110")
    eu.sendWithAtachment()
