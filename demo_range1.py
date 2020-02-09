#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 距離認識デモ
# for Bezelie Flitz
# for Raspberry Pi
# 超音波距離センサーHC-SR04を接続してください。

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
trigger_pin = 17      # GPIO 17
echo_pin = 27         # GPIO 27
actionDistance = 30.0 # しきい値（単位：センチ$）
actionDistanceC = 10.0 # しきい値（単位：センチ$）
waitMonologue = 500                # 顔が見つからなかったとき独り言を言う間隔
#csvFile   = "data_rangeDialogE.csv"  # セリフリスト
csvFile   = "data_rangeDialogJ.csv"  # セリフリスト
ttsJpn   = "exec_talkJpn.sh"       # 音声合成実行ファイル
ttsEng = "exec_talkEng.sh"         # 英語発話シェルスクリプトのファイル名
debugFile = "debug.txt"            # debug用ファイル

# 初期設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# 関数
def send_trigger_pulse():
  GPIO.output(trigger_pin, True)
  time.sleep(0.0001)
  GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
  count = timeout
  while GPIO.input(echo_pin) != value and count > 0:
    count -= 1

def get_distance():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(trigger_pin, GPIO.OUT)
  GPIO.setup(echo_pin, GPIO.IN)
  send_trigger_pulse()
  wait_for_echo(True, 10000)
  start = time.time()
  wait_for_echo(False, 10000)
  finish = time.time()
  pulse_len = finish - start
  distance  = int(pulse_len / 0.000058)
  return (distance) 

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
#  subprocess.call("sh "+ttsEng+" "+data[ansNum][1], shell=True)
  subprocess.call("sh "+ttsJpn+" "+data[ansNum][1], shell=True)
  bez.stop()

def debug_message(message):
  print (message)
#  writeFile(message)
#　pass
#  sys.stdout.write(message)

def writeFile(text):                    # デバッグファイル出力機能
  f = open (debugFile,'r')
  textBefore = ""
  for row in f:
    textBefore = textBefore + row
  f.close()
  f = open (debugFile,'w')
  f.write(textBefore + text + "\n")
  f.close()

# サーボの初期化
bez = bezelie.Control()                 # べゼリー操作インスタンスの生成
bez.moveCenter()                        # サーボの回転位置をトリム値に合わせる

# 初回処理
#subprocess.call("sh "+ttsEng+" "+u"preparation-has-been-completed", shell=True)
subprocess.call("sh "+ttsJpn+" 準備完了", shell=True)

# メインループ
def main():
  try:
    detected = "false"       # 前回顔が認識されたかどうか
    interval = 0                # 
    meet = 0
    prev_input_x = 0         # 
    prev_input_y = 0         # 
    while True:                                               # infinity loop
      distance = get_distance()
      print(distance, end="\t")
      if distance < actionDistance:
        interval = 0
        print ("近いです")
        if detected == "false":
          meet = 1
          replyMessage(u"未発見")
        else:
          meet = meet +1
          if meet > 3:
            if distance < actionDistanceC:
              replyMessage(u"顔認識")
            else:
              replyMessage(u"顔発見")
            meet = 1
        detected = "true"
      else:                   # If no faces were detected.
        print ("遠いです")
        detected = "false"       # 前回顔が認識されたかどうか
        meet = 0
        interval += 1
        if interval > waitMonologue:
          replyMessage(u"未発見")
          interval = 0
          if randint(1,3)==1:
            sign = -1
          else:
            sign = 1
          prev_input_y = sign*randint(0,6)          # 乱数を発生させる
          if prev_input_x > 0:
            sign = -1
          else:
            sign = 1
          prev_input_x = sign*randint(1,10)
          sleep (0.1)
      sleep(0.5)

  except KeyboardInterrupt: # CTRL+Cで終了
    debug_message('終了します')
    bez.moveCenter()
    sleep (0.2)
    bez.stop()
    sleep (0.1)
    sys.exit(0)

if __name__ == "__main__":
  debug_message('---------- started ----------')
  main()
  GPIO.cleanup()
  sys.exit(0)
