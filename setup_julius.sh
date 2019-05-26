#! /bin/bash
# setting up the Julius
# 音声認識エンジンJuliusのインストール

echo "Step0= setting snd-pcm-oss"
#sudo modprobe snd-pcm-oss
#sudo sh -c "echo snd-pcm-oss >> /etc/modules"
# for OSS
sudo apt-get -y install osspd-alsa
sudo sed -i -e 's/snd-pcm-oss//' /etc/modules
# for ALSA
sudo aptitude install libasound2-dev
#sudo apt-get -y install libasound2-dev

echo "Step1= installing Julius"
cd
sudo sh -c "rm -r julius-master"
wget https://github.com/julius-speech/julius/archive/master.zip
unzip master.zip
rm master.zip
cd julius-master
#./configure
./configure --with-mictype=alsa
make
sudo make install

echo "Step2= Getting and unzip Kits"
cd
sudo sh -c "rm -r julius-kit"
mkdir julius-kit
cd julius-kit
wget https://github.com/julius-speech/dictation-kit/archive/master.zip
unzip master.zip
rm master.zip
wget https://github.com/julius-speech/grammar-kit/archive/master.zip
unzip master.zip
rm master.zip

echo "finished"

########################
#echo "Step3=install the kits"
#cd ~/julius-kit/grammar*
#cp ~/VoiceCAP/command.tar .
#tar xvf command.tar
#rm command.tar
#cd command
#./setup.sh
