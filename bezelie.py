#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bezelie Python Module
# べゼリー専用モジュール

# モジュールのインポート
from random import randint         # 乱数の発生
from time import sleep             # ウェイト処理
import RPi.GPIO as GPIO            # GPIO
import smbus                       # I2C
import math                        # 計算用
import threading                   # マルチスレッド処理
import json                        # jsonファイルを扱うモジュール
import subprocess                  # 外部プロセスを実行するモジュール
from PIL import Image, ImageDraw, ImageFont, ImageFilter #
import numpy
import sys

# CONST
bus = smbus.SMBus(1)
trimJson = "data_trim.json"   # 設定ファイル
tts = "exec_talkJpn.sh"       # 発話シェルスクリプトのファイル名

def main():
  print ("centering...")
  bez = Control()               # べゼリー操作インスタンスの生成
  bez.setCenter()
  sleep (0.5)
  print("done")

class Control(object): # クラスの定義

    # 初期化メソッド。インスタンス生成時に自動実行される。
  def __init__(self, address_pca9685=0x40, dutyMax=490, dutyMin=110, dutyCenter=300, steps=2):
      f = open (trimJson,'r')
      readData = json.load(f)
      self.trimPitch = int(readData['data1'][0]['pitch'])
      self.trimRoll = int(readData['data1'][0]['roll'])
      self.trimYaw = int(readData['data1'][0]['yaw'])

      # インスタンス変数に値を代入。selfは自分自身のインスタンス名。
      self.address_pca9685 = address_pca9685
      self.dutyMax = dutyMax
      self.dutyMin = dutyMin
      self.dutyCenter = dutyCenter
      self.steps = steps
      self.pitchNow = dutyCenter
      self.rollNow = dutyCenter
      self.yawNow = dutyCenter
      self.initPCA9685()
      # 第１引数はselfにするのが義務。

# Servo ----------------------------

  def initPCA9685(self):
      try:
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)
        freq = 0.9 * 50
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = bus.read_byte_data(self.address_pca9685, 0x00)
        newmode = (oldmode & 0x7F) | 0x10
        bus.write_byte_data(self.address_pca9685, 0x00, newmode)
        bus.write_byte_data(self.address_pca9685, 0xFE, prescale)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode)
        sleep(0.005)
        bus.write_byte_data(self.address_pca9685, 0x00, oldmode | 0xa1)
      except:
        print ("サーボドライバーボードを接続してください")
        # pass

  def resetPCA9685(self):
        bus.write_byte_data(self.address_pca9685, 0x00, 0x00)

  def setPCA9685Duty(self, channel, on, off):
        channelpos = 0x6 + 4*channel
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

  def moveServo(self, id, degree, trim, max, min, speed, now):
        dst = int((self.dutyMin - self.dutyMax) * (degree + trim + 90) / 180 + self.dutyMax)
        if speed == 0:
            self.setPCA9685Duty_(id, 0, dst)
            sleep(0.001 * math.fabs(dst - now))
            now = dst
        if dst > max:
            dst = max
        if dst < min:
            dst = min
        while (now != dst):
            if now < dst:
                now += self.steps
                if now > dst:
                    now = dst
            else:
                now -= self.steps
                if now < dst:
                    now = dst
            self.setPCA9685Duty(id, 0, now)
            sleep(0.004 * self.steps *(speed))
        return (now)

  def movePitch(self, id, degree, speed=1):
        max = 320     # 下方向の限界
        min = 230     # 上方向の限界
        self.pitchNow = self.moveServo((id-1)*3+2, degree, self.trimPitch, max, min, speed, self.pitchNow)

  def moveRoll(self, id, degree, speed=1):
        max = 380     # 反時計回りの限界
        min = 220     # 時計回りの限界
        self.rollNow = self.moveServo((id-1)*3+1, degree, self.trimRoll, max, min, speed, self.rollNow)

  def moveYaw(self, id, degree, speed=1):
        max = 390     # 反時計回りの限界
        min = 210     # 時計回りの限界
        self.yawNow = self.moveServo((id-1)*3, degree, self.trimYaw, max, min, speed, self.yawNow)

# Action -----------------------------
  def moveCenter(self): # 3つのサーボの回転位置をトリム値に合わせる
    self.movePitch(1, 1)
    self.moveRoll(1, 1)
    self.moveYaw(1, 1)

  def pitchUpLong(self, id, time=2): # 
        self.movePitch(id, 5)

  def pitchDownLong(self, id, time=2): # 
        self.movePitch(id, -15)

  def pitchUp2(self, id, time=0.1): # 
        self.movePitch(id, 5)
        self.movePitch(id, 0)
        sleep (time)
        self.movePitch(id, 5)
        self.movePitch(id, 0)
        sleep (time)

  def pitchDown2(self, id, time=0.1): # 
        self.movePitch(id, -5)
        self.movePitch(id, 0)
        sleep (time)
        self.movePitch(id, -5)
        self.movePitch(id, 0)
        sleep (time)

  def pitchUpDown(self, id, time=0.5): # 
        self.movePitch(id, 5)
        self.movePitch(id, -10)
        self.movePitch(id, 0)

  def pitchUpMax(self, id, time=0.5): # 
        self.movePitch(id, 5)

  def pitchDownMax(self, id, time=0.1): # 
        self.movePitch(id, -15)
        self.movePitch(id, 0)

  def pitchCenter(self, id, time=0.2): # 
        self.movePitch(id, 0)

  def rollRightLeft(self, id, time=0.5): # 
        self.moveRoll(id, 20)
        self.moveRoll(id, -20)
        self.moveRoll(id, 0)

  def rollRightLong(self, id, time=2): # 
        self.moveRoll(id, 30)

  def rollRightMax(self, id, time=0.1): # 
        self.moveRoll(id, 30)
        sleep (time)
        self.moveRoll(id, 0)

  def rollLeftMax(self, id, time=0.5): # 
        self.moveRoll(id, -30)

  def rollCenter(self, id, time=0.2): # 
        self.moveYaw(id, 0)

  def yawRightLeft(self, id, time=0.1): # 
        self.moveYaw(id, 20)
        self.moveYaw(id, -20)
        self.moveYaw(id, 0)

  def yawRight(self, id, time=2): # 
        self.moveYaw(id, 10)

  def yawRightMax(self, id, time=2): # 
        self.moveYaw(id, 30)

  def yawRightPitchDown(self, id, time=0.5): # 
        self.moveYaw(id, 30)
        sleep (time)
        self.movePitch(id, -10)
        sleep (time)
        self.movePitch(id, 0)

  def yawLeftPitchDown(self, id, time=0.5): # 
        self.moveYaw(id, -30)
        sleep (time)
        self.movePitch(id, -10)
        sleep (time)
        self.movePitch(id, 0)

  def yawLeftMax(self, id, time=2): # 
        self.moveYaw(id, -30)

  def yawCenter(self, id, time=0.2): # 
        self.moveYaw(id, 0)

  def moveRnd(self):
        self.stop_event = threading.Event()
        r = randint(1,4)
        if r == 1:
            self.thread = threading.Thread(target = self.pitchUpDown(1))
        elif r == 2:
            self.thread = threading.Thread(target = self.rollRightLeft(1))
        elif r == 3:
            self.thread = threading.Thread(target = self.yawRightLeft(1))
        else:
            self.thread = threading.Thread(target = self.pitchUpDown(1))
        self.thread.start()

  def stop(self):
        self.stop_event.set()
        self.thread.join()

  def act(self, id, act):
    self.stop_event = threading.Event()
    if act == 'pitchUpLong':
        self.thread = threading.Thread(target = self.pitchUpLong, kwargs={'id':id})
    elif act == 'pitchDownLong':
        self.thread = threading.Thread(target = self.pitchDownLong, kwargs={'id':id})
    elif act == 'pitchUp2':
        self.thread = threading.Thread(target = self.pitchUp2, kwargs={'id':id})
    elif act == 'pitchDown2':
        self.thread = threading.Thread(target = self.pitchDown2, kwargs={'id':id})
    elif act == 'pitchUpDown':
        self.thread = threading.Thread(target = self.pitchUpDown, kwargs={'id':id})
    elif act == 'pitchUpMax':
        self.thread = threading.Thread(target = self.pitchUpMax, kwargs={'id':id})
    elif act == 'pitchDownMax':
        self.thread = threading.Thread(target = self.pitchDownMax, kwargs={'id':id})
    elif act == 'pitchCenter':
        self.thread = threading.Thread(target = self.pitchCenter, kwargs={'id':id})
    elif act == 'rollRightLeft':
        self.thread = threading.Thread(target = self.rollRightLeft, kwargs={'id':id})
    elif act == 'rollRightLong':
        self.thread = threading.Thread(target = self.rollRightLong, kwargs={'id':id})
    elif act == 'rollRightMax':
        self.thread = threading.Thread(target = self.rollRightMax, kwargs={'id':id})
    elif act == 'rollLeftMax':
        self.thread = threading.Thread(target = self.rollLeftMax, kwargs={'id':id})
    elif act == 'rollCenter':
        self.thread = threading.Thread(target = self.rollCenter, kwargs={'id':id})
    elif act == 'yawRightLeft':
        self.thread = threading.Thread(target = self.yawRightLeft, kwargs={'id':id})
    elif act == 'yawRight':
        self.thread = threading.Thread(target = self.yawRight, kwargs={'id':id})
    elif act == 'yawRightMax':
        self.thread = threading.Thread(target = self.yawRightMax, kwargs={'id':id})
    elif act == 'yawRightPitchDown':
        self.thread = threading.Thread(target = self.yawRightPitchDown, kwargs={'id':id})
    elif act == 'yawLeftPitchDown':
        self.thread = threading.Thread(target = self.yawLeftPitchDown, kwargs={'id':id})
    elif act == 'yawLeftMax':
        self.thread = threading.Thread(target = self.yawLeftMax, kwargs={'id':id})
    elif act == 'yawCenter':
        self.thread = threading.Thread(target = self.yawCenter, kwargs={'id':id})
    else:
        print ("No Action")
    self.thread.start()
    
# Message ----------------------------

  def drawText(self, img, text, size, align):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size, encoding="UTF-8")
    if align == 'center':
      img_size = numpy.array(img.size)
      txt_size = numpy.array(font.getsize(text))
      pos = (img_size - txt_size) / 2
      draw.multiline_text(pos, text, (0, 0, 0), font=font, spacing=1, align='center')
    else:
      draw.multiline_text((10,10), text, (0, 0, 0), font=font, spacing=1, align='left')

# Speech -----------------------------
  def speech(self, id, text):
    self.stop_event = threading.Event()
    if id == 1:
      self.thread = threading.Thread(target = self.speechExe, kwargs={'text':text})
    else:
      print ("Not Matched")
    self.thread.start()

  def speechExe(self, text):
    subprocess.call("sh "+tts+" "+text, shell=True)

# LED ---------------------------

  def onLed(self, channel):
        channelpos = 0x6 + 4*channel
        on = 0
        off = 4095
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

  def offLed(self, channel):
        channelpos = 0x6 + 4*channel
        on = 0
        off = 0
        try:
            bus.write_i2c_block_data(self.address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8])
        except IOError:
            pass

# スクリプトとして実行された場合はセンタリングを行う
if __name__ == "__main__":
  bez = Control()               # べゼリー操作インスタンスの生成
  if len(sys.argv)==1:
    print ("centering...")
    bez.moveCenter()
    sleep (0.5)
    print("done")
  else:
    comm1=str(sys.argv[1])
    print (comm1)
    if comm1=="center":
      bez.act(1, "pitchCenter")
      bez.act(1, "rollCenter")
      bez.act(1, "yawCenter")
    elif comm1=="pitch":
      bez.act(1, "pitchDownMax")
    elif comm1=="roll":
      bez.act(1, "rollRightMax")
    elif comm1=="yaw":
      bez.act(1, "yawRightLeft")
    else:
      bez.act(1, comm1)
