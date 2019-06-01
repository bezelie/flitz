#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Test Code : カメラ動作テスト
# カメラの画像をディスプレイに表示する

# モジュールのインポート
import subprocess                     # 外部プロセスを実行 $
import sys

# メインループ
def main():
  try:
    print ("開始します")
    subprocess.call("raspivid -t 0 -rot 180 -f -w 320 -h 240", shell=True)
    # -rot 180 ：１８０度回転
    # -w 320 ：横サイズ
    # -h 240 ：縦サイズ
  except KeyboardInterrupt:
    print ("  終了しました")
    sys.exit(0)

if __name__ == "__main__":
    main()
