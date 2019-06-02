#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Learning Code : print文の使いかた
# 文字を表示する

import sys
from time import sleep

while True:
  print ("Hello world %s" % (sys.argv[0]))
  # sys.argv = コマンドライ引数（リスト型）
  sys.stdout.flush()
  sleep(1)
