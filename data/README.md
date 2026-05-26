# Z-MATRIX Local Data Directory

data/ 是本地运行数据目录。

真实行情、财务、纸面交易流水、outcome 回填结果默认不进入 Git。
Git 只保存 samples/ 样例 CSV 与目录结构。

默认数据来源：
- local CSV
- manual snapshot
- external API disabled by default

禁止：
- 提交真实交易记录
- 提交敏感账户信息
- 提交大规模行情数据
- 默认联网拉取数据
