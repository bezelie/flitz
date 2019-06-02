#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : サーボを動かす
# ラズパイにサーボドライバーとサーボを接続してから実行してください。

# ライブラリの読み込み
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール

# 準備
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# メインループ
def main():
  try:
    print ("開始します")
    while True:
      action = 'pitchUpLong'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchDownLong'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchUp2'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchDown2'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchUpDown'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchUpMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchDownMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'pitchCenter'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollRightLeft'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollRightLong'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollRightMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollLeftMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollCenter'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawRightLeft'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawRight'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'rollRightMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawRightPitchDown'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawLeftPitchDown'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawLeftMax'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------
      action = 'yawCenter'
      print ("Action= "+action)
      bez.act(1, action)
      bez.stop()
      bez.moveCenter()
      sleep (1)
      #---------------------------

  except KeyboardInterrupt:
    print ("  終了しました")

if __name__ == "__main__":
    main()
