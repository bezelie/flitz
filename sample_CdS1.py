#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : 照度センサーのサンプル
# CdSセンサーをCdS(アナログinput0)と3Vに接続してください。

# ライブラリの読み込み
from time import sleep
import RPi.GPIO as GPIO
import subprocess                     # 外部プロセスを実行するモジュール
import bezelie

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# MCP3204からSPI通信で12ビットのデジタル値を取得。4チャンネル使用可
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
GPIO.setmode(GPIO.BCM)

# 変数
value = 2000               # 入力値がこの値を下回ると反応する

# 定数
ttsJpn = "exec_talkJpn.sh" # 発話シェルスクリプトのファイル名
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
      inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
      print("input = "+str(inputVal0))
      if inputVal0 < value:              # しきい値は条件によって変えてください。
        print ("      dark")
        bez.movePitch(1, 20)            # 上を向く
        subprocess.call("sh "+ttsJpn+" "+"くらいよお", shell=True)
        sleep(0.5)
        bez.movePitch(1, 0)
        sleep(0.5)
      else:
        print ("bright")
      sleep(1)

  except KeyboardInterrupt:
    print ("終了しました")
    GPIO.cleanup()                     # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
