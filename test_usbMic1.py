#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test Code : USBマイクテスト
# USBマイクの音をarecordで録音し、aplayで再生する。

# モジュールのインポート
from time import sleep                # ウェイト処理
import subprocess                     # 外部プロセスを実行するモジュール
import sys

# メインループ
print ("カード番号とデバイス番号の確認")
subprocess.call("arecord -l", shell=True)

print ("３秒間の録音を開始します")
cmds = ['sudo','arecord','-d','3','-D','hw:1,0','-r','44100','-f','S16_LE','test.wav'] # コマンドリストの作成
# hw:の後の２つの数字が、カード番号とデバイス番号に合っていることを確認してください。
proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
proc.communicate() # コマンド実行プロセスが終了するまで待機
print ("録音終了")
sleep(1)

print ("録音した音を再生します")
cmds = ['aplay','-D','plughw:0,0','test.wav'] # コマンドリストの作成
proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
proc.communicate() # コマンド実行プロセスが終了するまで待機

sys.exit(0)
