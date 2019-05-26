#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sample Code : 超音波センサーサンプル
# 超音波距離センサーHC-SR04を接続してください。

# モジュールのインポート
from time import sleep                # ウェイト処理
import RPi.GPIO as GPIO
import time
import sys

# 定義
trigger_pin = 17      # GPIO 17
echo_pin = 27         # GPIO 27
actionDistance = 10.0 # しきい値（単位：センチ）

# 初期設定
#bezelie.moveCenter()
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
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = int(pulse_len / 0.000058)
    return (distance)    

# メインループ
def main():
  try:
    while True:
      distance = get_distance()
      print(distance, end="\t")
      if distance < actionDistance:
        print ("近いです")
      else:
        print ("遠い")
      sleep(0.5)

  except KeyboardInterrupt:
    print (' 終了しました')
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    main()
