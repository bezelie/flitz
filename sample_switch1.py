#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : スイッチ入力のサンプル
# マニュアルを見てスイッチを接続しておいてください。

# モジュールのインポート
from time import sleep    # sleep(ウェイト処理)ライブラリの読み込み
import RPi.GPIO as GPIO   # GPIO(汎用入出力端子)ライブラリの読み込み

# 変数と定数
pinSwitch = 4             # スイッチをGPIO 4に接続。

# 初期設定
GPIO.setmode(GPIO.BCM)    # GPIOをGPIO番号で指定できるように設定
GPIO.setup(pinSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
# GPIO4を入力モードに設定し、プルダウン抵抗を有効化。

# 関数
def main():
  try:
    print ("開始します")
    while True:                            # 繰り返し処理
      if GPIO.input(pinSwitch)==GPIO.LOW: # GPIO4に電圧がかかっていなかったら・・・
        print ("スイッチは押されてません")
      else:                                # それ以外の場合は・・・
        print ("押されました")
      sleep (0.5)                          # 0.5秒待つ
  except KeyboardInterrupt:                # コントロール＋Cが押された場合の処理
    print ("終了しました")
    GPIO.cleanup()                         # ポートをクリア

# 直接実行された場合の処理
if __name__ == "__main__":
    main()
