#!/bin/bash
# 仮想環境を有効化
source /home/c0a22069/prometheus_export_pub/.venv/bin/activate

# Pythonスクリプトを実行
python3 /home/c0a22069/prometheus_export_pub/get-metrics.py

# 仮想環境を終了
deactivate
