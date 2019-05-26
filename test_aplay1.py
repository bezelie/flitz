#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test Code : スピーカーテスト
# wavファイル「Front Center」をaplayで再生する。

# モジュールのインポート
from time import sleep     # ウェイト処理
import subprocess          # 外部プロセスを実行するモジュール
import sys

# カード番号とデバイス番号の確認
print ("カード番号とデバイス番号の確認")
subprocess.call("aplay -l", shell=True)

# メインループ
try:
  while (True):
    cmds = ['aplay','-D','plughw:0,0','Front_Center.wav'] # コマンドリストの作成
    # plughw:の後の２つの数字が、カード番号とデバイス番号に合っていることを確認してください。
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
    proc.communicate() # コマンド実行プロセスが終了するまで待機
except KeyboardInterrupt:
  print (' 終了しました')
  sys.exit(0)
