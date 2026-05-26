# Workspace Layout v1.0

当前工作区标准结构：

zmatrix/ — 系统核心模块
zmatrix/architecture/ — 三层架构注册与审计
zmatrix/investment/ — B/R/D 与 7层投资过滤
zmatrix/data_facts/ — 本地数据事实层
zmatrix/paper_trading/ — 纸面账本与 outcome 回填
zmatrix/backtest/ — 轻量回测

pipelines/ — Z-G01~Z-G18 历史管线与业务管线
hermes/ — Z9/Hermes 旧记忆与校准资产
scripts/ — 验证与调度脚本
docs/contracts/ — 契约
docs/architecture/ — 架构文档
tests/ — 测试
release/ — release package
data/ — 本地数据目录，只提交 samples
