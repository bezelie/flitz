#!/bin/bash
# 音声合成（flite）起動スクリプト
VOICEDATA=/tmp/voice.wav
sudo espeak -v "english"+f3 -p 99 -w $VOICEDATA $1
aplay -D plughw:0,0 $VOICEDATA
#sudo rm -f $VOICEDATA
