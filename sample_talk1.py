#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : 音声合成サンプル

# モジュールのインポート
from time import sleep     # ウェイト処理
import subprocess          # 外部プロセスを実行するモジュール
import sys

# 変数
ttsJpn = "exec_talkJpn.sh" # 日本語発話シェルスクリプトのファイル名
ttsEng = "exec_talkEng.sh" # 英語発話シェルスクリプトのファイル名

# メインループ
try:
  while (True):
    cmds = ['sh',ttsJpn, 'こんにちは'] # コマンドリストの作成
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
    proc.communicate() # コマンド実行プロセスが終了するまで待機
    cmds = ['sh',ttsEng, 'Hello'] # コマンドリストの作成
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
    proc.communicate() # コマンド実行プロセスが終了するまで待機
except KeyboardInterrupt:
  print (' 終了しました')
  sys.exit(0)
