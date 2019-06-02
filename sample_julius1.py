#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : julius音声認識サンプル

# モジュールのインポート
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import socket                      # ソケット通信モジュール
import select                      # 待機モジュール
import sys                         # python終了sys.exit()のために必要

# 変数
ttsJpn = "exec_talkJpn.sh" # 音声合成
bufferSize = 256    # 受信するデータの最大バイト。２の倍数が望ましい。

# 関数
def socket_buffer_clear():
  while True:
    rlist, _, _ = select.select([client], [], [], 1)
    if len(rlist) > 0: 
      dummy_buffer = client.recv(bufferSize)
    else:
      break

#p = subprocess.Popen(["sh boot_julius.sh"], stdout=subprocess.PIPE, shell=True) # julius起動スクリプトを実行
#pid = p.stdout.read().decode('utf-8') # juliusのプロセスIDを取得
#sleep(3) # 3秒間スリープ

# TCPクライアントを作成しJuliusサーバーに接続する
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
enabled_julius = False
for count in range(3):
  try:
    client.connect(('localhost', 10500))
    # client.connect(('10.0.0.1', 10500))  # Juliusサーバーに接続
    enabled_julius = True
    break
  except socket.error:
    print ('failed socket connect. retry')
    pass
if enabled_julius == False:
  print ('Could not find Julius')
  sys.exit(1)

# メインループ
new = ""
try:
  print ('音声認識開始')
  cmds = ['sh',ttsJpn, 'こんにちは'] # コマンドリストの作成
  proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
  proc.communicate() # コマンド実行プロセスが終了するまで待機
  data = ""
  socket_buffer_clear()
  while True:
    data = client.recv(bufferSize).decode('utf-8')  # Juliusサーバーから受信
    if "<RECOGOUT>" in data:
      new = ""
    new = new + data
    if "</RECOGOUT>" in new:  # RECOGOUTツリーの最終行を見つけたら以下の処理を行う
      print (new)
      if "朝の挨拶" in new:
        cmds = ['sh',ttsJpn, 'どうもです'] #
        proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
        proc.communicate() # コマンド実行プロセスが終了するまで待機
      else:
        print ("not mached")
      socket_buffer_clear()
      new = ""

except KeyboardInterrupt: # CTRL+Cで終了
  client.close()
  sys.exit(0)
