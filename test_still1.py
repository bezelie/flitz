#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test Code : カメラ静止画撮影テスト
# カメラで静止画を撮影する。

# モジュールのインポート
from time import sleep
import subprocess                     # 外部プロセスを実行 $
import sys

# メインループ
def main():
    subprocess.call("sudo raspistill -rot 180 -o test.jpg", shell=True)
    # -rot 180 ：１８０度回転
    print ("写真を撮りました")
    sleep(1)
    print ("ファイルマネージャーでtest.jpgを開いてみてください")
    sys.exit(0)

if __name__ == "__main__":
    main()
