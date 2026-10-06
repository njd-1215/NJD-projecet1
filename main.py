# 招投标监控主程序
import logging
import yaml
from datetime import datetime

from storage.db import Database
from spider.base import BaseSpider
from notifier.email import EmailNotifier
from notifier.wecom import WeComNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_once():
    """执行一次完整的监控流程"""
    logger.info("=== 开始执行招投标监控 ===")
    config = load_config()
    db = Database(config["database"]["path"])

    new_items = []

    for site_cfg in config["sites"]:
        try:
            spider = BaseSpider(site_cfg)
            items = spider.fetch_list()
            logger.info(f"{site_cfg['name']}：抓取到 {len(items)} 条记录")

            for item in items:
                # 关键词过滤
                if not match_keywords(item["title"], config):
                    continue
                # 去重：已推送过的不再推送
                if db.is_exists(item["url"]):
                    continue
                # 存入数据库并标记为待推送
                db.insert_item(item)
                new_items.append(item)
        except Exception as e:
            logger.error(f"抓取 {site_cfg['name']} 失败：{e}")

    # 推送通知
    if new_items:
        logger.info(f"发现 {len(new_items)} 条新的匹配项目，开始推送通知")
        notifiers = []
        if config["notify"]["email"]["enabled"]:
            notifiers.append(EmailNotifier(config["notify"]["email"]))
        if config["notify"]["wecom"]["enabled"]:
            notifiers.append(WeComNotifier(config["notify"]["wecom"]))

        for notifier in notifiers:
            notifier.send(new_items)
    else:
        logger.info("没有发现新的匹配项目")

    logger.info("=== 本次执行结束 ===")


def match_keywords(title, config):
    """检查标题是否匹配关键词规则"""
    title = title.lower()
    # 排除词优先
    for kw in config.get("exclude_keywords", []):
        if kw.lower() in title:
            return False
    # 匹配任意包含词
    for kw in config["keywords"]:
        if kw.lower() in title:
            return True
    return False


if __name__ == "__main__":
    run_once()
