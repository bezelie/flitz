#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : LED点滅サンプル
# GPIO26ピンとGNDにLEDを接続してから実行してください。

# モジュールのインポート
from time import sleep    # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO   # GPIO(汎用入出力端子)ライブラリの読み込み

# 変数
pinLed = 26       # LEDのアノード（長い方の足）を指す

# 初期設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinLed, GPIO.OUT)

# メインループ
def main():
  try:
    while True:
      print ("点灯")
      GPIO.output (pinLed, True)
      sleep(1)
      print ("消灯")
      GPIO.output (pinLed, False)
      sleep(1)
  except:
    GPIO.cleanup()                     # ポートをクリア

if __name__ == "__main__":
    main()
