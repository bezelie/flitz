#!/bin/bash
# csvデータをtsvに変換
sudo sed -E "s/,/    /g" data_julius.csv > data_julius.tsv
# tsvファイルをjuliusのdic形式に変換
sudo iconv -f utf8 -t eucjp data_julius.tsv | ./tool_yomi2voca.pl > data_julius.dic
exit 0
