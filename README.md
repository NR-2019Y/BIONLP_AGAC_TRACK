# BIONLP_AGAC_TRACK

AGAC track (Course Project)

## 1 准备

http://pubannotation.org/projects/AGAC_training/annotations.tgz \# 解压的250个\*.json文件后放到 data/AGAC_training 目录

http://pubannotation.org/projects/AGAC_sample/annotations.tgz   \# 解压后的50个\*.json文件后放到 data/AGAC_sample 目录

https://github.com/Jekub/Wapiti.git \# wapiti软件

https://github.com/kyzhouhzau/2019SpringTextM.git \# conlleval.pl脚本、pat/Tok321dis.pat文件，放置于当前目录

https://github.com/bionlp-hzau/Tutorial_4_CRF \# 参考文档

其他: numpy包(python3)

## 2 流程
```{sh}
# 项目目录
.
├── data
│   ├── AGAC_sample
│   └── AGAC_training
├── OUT_TAB_DIR
├── SAMPLE_TAB
└── TRAIN_TAB
```

### 2.1 数据检查和预处理

对原始的 AGAC_training 和 AGAC_sample 中的 json 文件进行检查和预处理
```{bash}
# json2tab.py 可以换成 json2tab_2.py
for F in data/AGAC_training/*.json; do
  FJ=${F##*/}; FJ=OUT_TAB_DIR/${FJ%.*}.tab; 
  python3 json2tab.py $F $FJ; 
done
```
将在OUT_TAB_DIR目录生成245个\*.tab文件（处理部分\*.json文件会报错，因此不生产对应的\*.tab文件）。

### 2.2 使用wapiti软件进行训练和预测

```{bash}
# training
for f in $(ls OUT_TAB_DIR); do 
	if [ -f data/AGAC_training/${f%.*}.json ] && [ ! -f data/AGAC_sample/${f%.*}.json ]; then echo ${f%.*}.tab; fi; 
done > training_list.txt
# sample
for f in $(ls OUT_TAB_DIR); do
	if [ -f data/AGAC_sample/${f%.*}.json ]; then echo ${f%.*}.tab; fi; 
done > sample_list.txt
