#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test Code : サーボ動作テスト
# ３つのサーボを順に右と左に回転させる。

# モジュールのインポート
from time import sleep                # ウェイト処理
import bezelie                        # べゼリー専用モジュール
import sys                            # 最後にsys.exit(0)するために必要

# セッティング
bez = bezelie.Control()               # べゼリー操作インスタンスの生成
bez.moveCenter()                      # サーボをセンタリング
sleep(0.5)

# メインループ
try:
  print ("開始します")
  while True:
    # 頭のサーボ（pitch）
    bez.movePitch(1,10)
    sleep(1)
    bez.movePitch(1,-10)
    sleep(1)
    bez.movePitch(1,0)
    sleep(1)
    # 背中のサーボ（roll）
    bez.moveRoll(1,20)
    sleep(1)
    bez.moveRoll(1,-20)
    sleep(1)
    bez.moveRoll(1,0)
    sleep(1)
    # 回転台のサーボ（yaw）
    bez.moveYaw(1,30)
    sleep(1)
    bez.moveYaw(1,-30)
    sleep(1)
    bez.moveYaw(1,0)
    sleep(1)
except KeyboardInterrupt:
  print ("  終了しました")
  sys.exit(0)
