# prometheus_export_pub

# 概要
Prometheusで収集した任意のメトリクス（このスクリプトでは`probe_http_status_code`）をAPI経由で取得し，15秒間隔で値を収集するスクリプト．
取得した結果は，UTC時刻でタイムスタンプ付きのCSVファイルに出力される．
また，このスクリプトはsystemd timerやCronJobで定期実行することで，定期的にメトリクスの値を取得することができる．

# 環境
* Python：3.12.3
  * requests：2.32.5
* Prometheus：2.53.1

# 使い方
仮想環境を使用する際は以下のコマンドを実行

コマンドとその実行結果
```bash
c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ python3 -m venv .venv
c0a22069@c0a22069-log-collector:~/prometheus_export_pub$
```

仮想環境をアクティベートする方法

コマンドとその実行結果
```bash
c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ source .venv/bin/activate
(.venv) c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ 
```

requeatsモジュールのインストール

コマンドとその実行結果
```bash
(.venv) c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ pip3 install requests
Collecting requests
  Using cached requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting charset_normalizer<4,>=2 (from requests)
  Using cached charset_normalizer-3.4.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
Collecting idna<4,>=2.5 (from requests)
  Using cached idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests)
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests)
  Using cached certifi-2025.10.5-py3-none-any.whl.metadata (2.5 kB)
Using cached requests-2.32.5-py3-none-any.whl (64 kB)
Using cached certifi-2025.10.5-py3-none-any.whl (163 kB)
Using cached charset_normalizer-3.4.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (153 kB)
Using cached idna-3.11-py3-none-any.whl (71 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Installing collected packages: urllib3, idna, charset_normalizer, certifi, requests
Successfully installed certifi-2025.10.5 charset_normalizer-3.4.4 idna-3.11 requests-2.32.5 urllib3-2.5.0
(.venv) c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ pip3 install requests
```

## get-metrics.py
PrometheusのHTTP API `/api/v1/query_range`をもちいて，`probe_http_status_code`メトリクスを取得し、CSV形式で保存するスクリプト．
現在時刻を基準に直近1分間のデータを15秒間隔で取得し，対象の各IPアドレス（TARGET_IPS）ごとのHTTPステータスコードをstatus_code_metrics.csv に追記して保存する．

コマンドとその実行結果
```bash
(.venv) c0a22069@c0a22069-log-collector:~/prometheus_export_pub$ python3 get-metrics.py 
/home/c0a22069/prometheus_export_pub/test-get-metrics.py:18: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  now = datetime.utcnow()
/home/c0a22069/prometheus_export_pub/test-get-metrics.py:43: DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.fromtimestamp(timestamp, datetime.UTC).
  ts = datetime.utcfromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
Metrics exported to ./status_code_metrics.csv
Time range: 07:50:00 ～ 07:50:59 (UTC)
(.venv) c0a22069@c0a22069-log-collector:~/prometheus_export_pub$
```
出力されたCSVファイル（IPアドレスは隠しています）
```csv
timestamp,192.168.X.X,192.168.X.X,192.168.X.X,192.168.X.X
2025-11-02 07:50:00,200,200,200,200
2025-11-02 07:50:15,200,200,200,200
2025-11-02 07:50:30,200,200,200,200
2025-11-02 07:50:45,200,200,200,200
```

## run-get-metrics.sh
`get-metrics.py`を実行するスクリプト．
仮想環境を使いつつ，systemd timerやCronJobで定期実行させるときに使用する．
定期実行させない場合は必要ない．





