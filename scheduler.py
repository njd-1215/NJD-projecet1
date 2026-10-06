from apscheduler.schedulers.blocking import BlockingScheduler
import yaml
import logging

from main import run_once

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    scheduler = BlockingScheduler()

    # 按配置的小时数添加定时任务
    for hour in config["schedule"]["hour"]:
        scheduler.add_job(
            run_once,
            "cron",
            hour=hour,
            minute=0,
            id=f"job_{hour}h",
        )

    logger.info(f"定时任务已启动，每天执行时间：{config['schedule']['hour']}点")
    # 启动时先跑一次
    run_once()
    scheduler.start()


if __name__ == "__main__":
    main()
