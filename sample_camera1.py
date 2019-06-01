#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# Sample Code : Camera Moving Test
#

# モジュールのインポート
from  time import sleep                # ウェイト処理
import picamera                        # カメラモジュール
import bezelie                         # べゼリー専用モジュール
import sys

# サーボの準備
bez = bezelie.Control()                # べゼリー操作インスタンスの生成
bez.moveCenter()                       # サーボをセンタリング

# メインループ
def main():
  try:
    with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)   # お使いのディスプレイに合わせて調整してください
      camera.rotation = 180            # 画面が上下逆さまだったらこの行は削除してください。
      camera.start_preview()
      sleep(2)
      head = 0
      while (True):
        bez.moveRoll (1, 10)
        bez.moveYaw (1, 25, 2)
        sleep (0.5)
        bez.moveRoll (1, -10)
        bez.moveYaw (1, -25, 2)
        sleep (0.5)
        head += 10
        if head > 20:
          head = -10
        bez.movePitch (1, head)
  except KeyboardInterrupt:
    print (" 終了します")
    sys.exit(0)

if __name__ == "__main__":
    main()
