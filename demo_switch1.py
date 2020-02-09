#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 距離認識デモ
# for Bezelie Flitz
# for Raspberry Pi

from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import subprocess                  # 外部プロセスを実行するモジュール
import json                        # jsonファイルを扱うモジュール
import csv                         # CSVファイルを扱うモジュール
import sys                         # python終了sys.exit()のために必要
import bezelie                     # べゼリー専用サーボ制御モジュール
import RPi.GPIO as GPIO
import time

# 定義
pinSwitch = 4
#csvFile   = "data_rangeDialogE.csv"  # セリフリスト
csvFile   = "data_rangeDialogJ.csv"  # セリフリスト
ttsJpn   = "exec_talkJpn.sh"       # 音声合成実行ファイル
ttsEng = "exec_talkEng.sh"         # 英語発話シェルスクリプトのファイル名

# 初期設定
#bezelie.moveCenter()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 関数
def replyMessage(keyWord):        # 対話
  data = []                       # 対話ファイル（csv）を変数dataに読み込む
  with open(csvFile, 'rt') as f:  # csvFileをtextでオープン
    for i in csv.reader(f):       # ファイルから１行ずつiに読み込む
      data.append(i)              # dataに追加

  data1 = []                      # dataから質問内容がキーワードに一致している行をdata1として抜き出す
  for index,i in enumerate(data): # index=連番
    if i[0]==keyWord:             #
      print ("見つかった")
      j = randint(1,100)          # １から１００までの乱数を発生させる
      data1.append(i+[j]+[index]) # data1=質問内容,返答,乱数,連番のリスト

  if data1 == []:                 # data1が空っぽだったらランダムで返す
    print ("ランダム")
    for index,i in enumerate(data): 
      j = randint(1,100)         
      data1.append(i+[j]+[index])

  maxNum = 0                      # data1の候補から乱数値が最大なものを選ぶ
  for i in data1:                 
    if i[2] > maxNum:              
      maxNum = i[2]                
      ansNum = i[3]               

  bez.moveRnd()
 # subprocess.call("sh "+ttsEng+" "+data[ansNum][1], shell=True)
  subprocess.call("sh "+ttsJpn+" "+data[ansNum][1], shell=True)
  bez.stop()

# サーボの初期化
bez = bezelie.Control()                 # べゼリー操作インスタンスの生成
bez.moveCenter()                        # サーボの回転位置をトリム値に合わせる

# 初回処理
#subprocess.call("sh "+ttsEng+" "+u"preparation-has-been-completed", shell=True)
subprocess.call("sh "+ttsJpn+" 準備完了", shell=True)

# メインループ
def main():
  try:
    while True:                                               # infinity loop
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(pinSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      if GPIO.input(pinSwitch)==GPIO.LOW:
        print ("近いです")
      else:
        replyMessage(u"顔発見")
      sleep (0.5)

  except KeyboardInterrupt: # CTRL+Cで終了
    bez.moveCenter()
    sleep (0.2)
    bez.stop()
    sleep (0.1)
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
  main()
  GPIO.cleanup()
  sys.exit(0)
