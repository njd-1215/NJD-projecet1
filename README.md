# NJD-projecet1 — 招投标项目监控工具

定时爬取招投标网站，按关键词筛选匹配项目，通过邮件 / 企业微信推送通知，SQLite 存储历史记录。

## 功能

- **多网站监控**：配置化添加要监控的招投标网站列表
- **关键词筛选**：按包含词 / 排除词过滤项目标题
- **去重存储**：SQLite 数据库记录历史，已推送的不重复通知
- **多渠道通知**：支持邮件（SMTP）、企业微信机器人
- **定时执行**：基于 APScheduler，可配置每天多个时间点自动运行

## 项目结构

```
NJD-projecet1/
├── main.py              # 主程序入口，执行一次完整流程
├── scheduler.py         # 定时任务启动脚本
├── config.example.yaml  # 配置文件模板
├── requirements.txt     # Python 依赖
├── spider/             # 爬虫模块
│   └── base.py         # 基础爬虫类
├── storage/            # 数据存储模块
│   └── db.py           # SQLite 数据库操作
└── notifier/           # 通知模块
    ├── email.py        # 邮件通知
    └── wecom.py        # 企业微信通知
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

复制配置模板并修改：

```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`，填入：
- 要监控的网站列表和 CSS 选择器
- 关键词 / 排除词
- 邮件 SMTP 配置（163 邮箱需要用授权码，不是登录密码）
- 企业微信机器人 webhook（可选）

### 3. 测试运行一次

```bash
python main.py
```

### 4. 启动定时任务（常驻运行）

```bash
python scheduler.py
```

## 后续扩展方向

- [ ] 支持更多招投标网站（各省政府采购网、公共资源交易中心）
- [ ] 项目详情页抓取（预算金额、截止时间）
- [ ] Web 面板查看历史记录
- [ ] Docker 部署
