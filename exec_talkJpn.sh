#!/bin/bash
# 音声合成（Open JTalk）起動スクリプト

# メッセージがない場合は終了
CMD=`basename $0`
if [ $# -lt 1 ]; then
  echo "Usage: ${CMD} <message>"
  exit 1  # エラーコード 1で終了
fi

HTSVOICE=/usr/share/hts-voice/mei/mei_normal.htsvoice # 音声データファイル名
DICDIRE=/var/lib/mecab/dic/open-jtalk/naist-jdic/ # 形態素解析ソフトMeCabの辞書ディレクトリ名
VOICEDATA=/tmp/voice.wav # 生成する音声合成データファイル名
sudo echo "$1" | open_jtalk \
-x $DICDIRE \
-m $HTSVOICE \
-ow $VOICEDATA \
-s 55000 \
-b 0.0 \
-r 1.0 \
-fm 0.0 \
-u 0.0 \
-jm 1.0 \
-jf 1.0 \
-z 10000
aplay -q -D plughw:0,0 $VOICEDATA
# sudo rm -f $VOICEDATA
exit 0

# s   サンプリング周波数　1-
#     0000-
#-p 80 \
# p   フレーム周期 1-
#     100ぐらいか。大きな値にすると実行に時間がかかってしまう。
#-a 0.05 \
# a   オールパス値　0.0-1.0
# b   ポストフィルター係数 0.0-1.0
# r   スピーチ速度係数 0.0-(1.0)-
#     1.5ぐらいがよいかな。大きくても2.5ぐらいか。大きいと冒頭が切れる。
# fm  追加ハーフトーン (0.0)
# u   有声・無声境界値 0.0-(0.5)-1.0
# jm  スペクトラム係数内変動の重み 0.0-(1.0)-
# jf  F0系列内変動の重み 0.0-(1.0)-
#     0にすると平坦なロボット声になる。
# z   オーディオバッファサイズ 0-(0)-
