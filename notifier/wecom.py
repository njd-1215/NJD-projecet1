import requests


class WeComNotifier:
    """企业微信机器人通知"""

    def __init__(self, config):
        self.cfg = config

    def send(self, items):
        content = f"招投标监控提醒：发现 {len(items)} 条新项目\n\n"
        for i, item in enumerate(items, 1):
            content += f"{i}. {item['title']}\n   {item['url']}\n\n"

        payload = {
            "msgtype": "text",
            "text": {"content": content}
        }

        resp = requests.post(self.cfg["webhook"], json=payload)
        print(f"企业微信推送结果：{resp.json()}")
