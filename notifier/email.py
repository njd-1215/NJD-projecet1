import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    """邮件通知"""

    def __init__(self, config):
        self.cfg = config

    def send(self, items):
        msg = MIMEMultipart()
        msg["Subject"] = f"招投标监控提醒：发现 {len(items)} 条新项目"
        msg["From"] = self.cfg["sender"]
        msg["To"] = ", ".join(self.cfg["receivers"])

        # 构建 HTML 正文
        html = "<h3>发现以下匹配的招投标项目：</h3><ul>"
        for item in items:
            html += f'<li><a href="{item["url"]}">{item["title"]}</a>（{item["site"]}，{item["date"]}）</li>'
        html += "</ul>"

        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP_SSL(self.cfg["smtp_server"], self.cfg["smtp_port"]) as server:
            server.login(self.cfg["sender"], self.cfg["password"])
            server.sendmail(self.cfg["sender"], self.cfg["receivers"], msg.as_string())

        print(f"邮件已发送给 {self.cfg['receivers']}")
