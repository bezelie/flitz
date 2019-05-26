#! /bin/bash
# 音声合成プログラムopenJTalk（日本語)とflite（英語）のインストール

echo "Step1=openJTalk標準パッケージのインストール"
sudo apt-get -y install open-jtalk # プログラム本体
sudo apt-get -y install open-jtalk-mecab-naist-jdic # 辞書
sudo apt-get -y install hts-voice-nitech-jp-atr503-m001 # 音響モデル。標準の男性声。

echo "Step2=MMD Agentから音響モデルMeiを取得"
# MMD Agent(http://www.mmdagent.jp/)
cd /tmp # カレントディレクトリーを /tmp に移動。
wget http://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip
# MMDAgent_Example-1.7.zip の取得
unzip MMDAgent_Example-1.7.zip MMDAgent_Example-1.7/Voice/*
# MMDAgent_Example-1.7.zip の展開
sudo cp -r MMDAgent_Example-1.7/Voice/mei/ /usr/share/hts-voice
# Meiの音響データを/usr/share/hts-voiceへコピー

echo "Step3=/var/openjtalkディレクトリーが存在していなければ作成する"
if [ ! -e /var/openjtalk ]; then
  sudo mkdir /var/openjtalk # /var/openjtalkディレクトリー作成
  sudo chown pi.pi /var/openjtalk # 所有者 pi、所有グループ pi を指定
fi

echo "Step4=espeakのインストール"
sudo apt-get install espeak

echo "設定完了"
