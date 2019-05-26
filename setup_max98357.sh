#! /bin/bash
# MAX98357が使えるようにラズパイの設定を変えます。

echo "Step1=/etc/modprobe.d/raspi-blacklist.conf"
sudo sed -i -e 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
sudo sed -i -e 's/blacklist snd-soc-pcm512x/#blacklist snd-soc-pcm512x/' /etc/modprobe.d/raspi-blacklist.conf
sudo sed -i -e 's/blacklist snd-soc-wm8804/#blacklist snd-soc-wm8804/' /etc/modprobe.d/raspi-blacklist.conf

echo "Step2=/etc/modules"
# ヘッドホンオーディオの無効化
sudo sed -i -e 's/snd_bcm2835/#snd_bcm2835/' /etc/modules

echo "Step3=/etc/asound.conf"
sudo cp asound-conf.txt /etc/asound.conf

echo "Step4=/boot/config.txt"
# デバイスツリーオーバレイの追加
sudo sed -i -e 's/dtparam=audio=on/#dtparam=audio=on/' /boot/config.txt
sudo sh -c "echo dtoverlay=hifiberry-dac >> /boot/config.txt"
sudo sh -c "echo dtoverlay=i2s-mmap >> /boot/config.txt"

echo "設定完了。再起動（sudo reboot）してください"
