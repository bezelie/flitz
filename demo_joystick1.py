#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : アナログ入力のサンプル
# ジョイスティックを接続しておいてください。

# ライブラリの読み込み
import RPi.GPIO as GPIO
from time import sleep
import bezelie
import subprocess          # 外部プロセスを実行するモジュール
import sys

# MCP3204からSPI通信で12ビットのデジタル値を取得。
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(cspin, GPIO.HIGH)
    GPIO.output(clockpin, GPIO.LOW)
    GPIO.output(cspin, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(mosipin, GPIO.HIGH)
        else:
            GPIO.output(mosipin, GPIO.LOW)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(clockpin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(misopin)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(cspin, GPIO.HIGH)
    return adcout

# 初期設定
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
#GPIO.cleanup()                     # ポートをクリア
GPIO.setmode(GPIO.BCM)
pinSwitch = 26
GPIO.setup(pinSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
sleep(0.5)

# 変数
ttsJpn = "exec_talkJpn.sh" # 日本語発話シェルスクリプトのファイル名
ttsEng = "exec_talkEng.sh" # 英語発話シェルスクリプトのファイル名
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

# SPI通信用の入出力を定義
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

# 関数
def main():
  try:
    print ("開始します")
    while True:
      axisX = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
      axisX = int((axisX-2200)*30/2000)
      print("X= "+str(axisX), end="\t")
      bez.moveYaw(1,axisX,0.1)
      axisY = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
      axisY = int((axisY-2100)*15/2000*(-1))+5
      print("Y= "+str(axisY), end="\t")
      bez.movePitch(1,axisY,0.1)
      if GPIO.input(pinSwitch)==GPIO.LOW:
        print ("switch = on")
        bez.moveRoll(1,10,0.1)
        cmds = ['sh',ttsJpn, 'それはなんですか？'] # コマンドリストの作成
        proc = subprocess.Popen(cmds, stdout=subprocess.PIPE) # コマンドの呼び出し
        proc.communicate() # コマンド実行プロセスが終了するまで待機
        bez.moveRoll(1,0,0.1)
      else:
        print ("switch = off")
      sleep(0.5)

  except KeyboardInterrupt:
    print ("終了しました")
    GPIO.cleanup()                     # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
