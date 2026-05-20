#!/bin/bash
# zmatrix_env.sh — Z-MATRIX-OS v2.9.1 共享环境
# 所有路径指向 OpenClaw 工作区，零外部硬编码
# ⛔ cd 禁令: source 此文件后不得 cd 到任何外部目录

export ZMATRIX_HOME="/Users/z1/.openclaw/workspace"
export ZMATRIX_PYTHON="/Users/z1/workspace-dev/.venv_glm5/bin/python3"

# PYTHONPATH: workspace 根 (含 zmatrix/ data/ configs/ symlinks)
export PYTHONPATH="$ZMATRIX_HOME:$PYTHONPATH"

# 技能脚本
export Z8_SCRIPTS="$ZMATRIX_HOME/skills/z8-quant-stack/scripts"

# 宪法
export ZMATRIX_CONSTITUTION="$HOME/Documents/openclaw memory/openclaw memory/👑_王座_半人马宪法.md"
