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
├── TRAIN_TAB
└── RESULT
```

### 2.1 数据检查和预处理

对原始的 AGAC_training 和 AGAC_sample 中的 json 文件进行检查和预处理
（注：data/AGAC_training 和 data/AGAC_sample 中同名的json文件的内容是基本一致的（例外：PubMed-24632946.json，PubMed-26637668.json，PubMed-28890134.json），区别仅在与project字段，一个是AGAC_training，一个是AGAC_sample。不需要专门整理
data/AGAC_sample目录的数据。）
```{bash}
# json2tab.py 可以换成 json2tab_2.py（详细流程见Result2.md），结果会更好，
for F in data/AGAC_training/*.json; do
  FJ=${F##*/}; FJ=OUT_TAB_DIR/${FJ%.*}.tab; 
  python3 json2tab.py $F $FJ; 
done
```
将在OUT_TAB_DIR目录生成245个\*.tab文件（处理部分\*.json文件会报错，因此不生产对应的\*.tab文件）。
```{sh}
# 报错信息
Traceback (most recent call last):
  File "json2tab.py", line 77, in <module>
    raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
__main__.DataError: ('PubMed-19917135.json', ('significantly', 1136, 1149, False), ('T5', 1126, 1129, 'Gene'), 'p53')
Traceback (most recent call last):
  File "json2tab.py", line 65, in <module>
    raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
__main__.DataError: ('PubMed-28939416.json', ('GNASR201C', 1266, 1275, False), ('T7', 1266, 1270, 'Gene'), 'GNAS')
Traceback (most recent call last):
  File "json2tab.py", line 65, in <module>
    raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
__main__.DataError: ('PubMed-28942122.json', ('Clcn7F318L', 713, 723, False), ('T5', 713, 718, 'Gene'), 'Clcn7')
Traceback (most recent call last):
  File "json2tab.py", line 65, in <module>
    raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
__main__.DataError: ('PubMed-29323748.json', ('Ptpn11E76K', 977, 987, False), ('T23', 977, 983, 'Gene'), 'Ptpn11')
Traceback (most recent call last):
  File "json2tab.py", line 65, in <module>
    raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
__main__.DataError: ('PubMed-29464833.json', ('CgPDR1GOF', 1088, 1097, False), ('T15', 1088, 1094, 'Gene'), 'CgPDR1')
# 报错原因：
PubMed-19917135.json：
denotations中字段反复使用：('T24', 1126, 1135, 'Protein'), ('T5', 1126, 1129, 'Gene'), ('T6', 1130, 1135, 'Var')
其余的json文件均为基因名问题。为处理简便并尽量不修改原始的json文件，后续处理中忽略上述文件。
```

### 2.2 使用wapiti软件进行训练和预测

```{bash}
# training
for f in $(ls OUT_TAB_DIR); do 
  if [ -f data/AGAC_training/${f%.*}.json ] && [ ! -f data/AGAC_sample/${f%.*}.json ]; then 
    echo ${f%.*}.tab; 
  fi; 
done > training_list.txt
# sample
for f in $(ls OUT_TAB_DIR); do
  if [ -f data/AGAC_sample/${f%.*}.json ]; then 
    echo ${f%.*}.tab; 
  fi; 
done > sample_list.txt
for f in $(cat training_list.txt); do ln -s ../OUT_TAB_DIR/$f TRAIN_TAB/$f; done
for f in $(cat sample_list.txt); do ln -s ../OUT_TAB_DIR/$f SAMPLE_TAB/$f; done

# pattern文件（patFile)与 https://github.com/kyzhouhzau/2019SpringTextM.git 中用到的是一致的
# Tok321dis.pat，conlleval.pl文件来源于 https://github.com/kyzhouhzau/2019SpringTextM.git
grep -v -P '^\s+$' Tok321dis.pat  > patFile
# 处理tab文件
# 第三列全部为"O"，该列用途还不太明确
# training_list.txt 列出的196份数据(tab)中，选取146份用于训练模型，用另外的50份来检测模型的优劣，并据此调整训练参数
cat $(head -146 training_list.txt | sed 's#^#TRAIN_TAB/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > Data1.tab
cat $(tail -50 training_list.txt  | sed 's#^#TRAIN_TAB/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > Data2.tab

gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' TRAIN_TAB/*.tab > OriTrain.tab
gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' SAMPLE_TAB/*.tab > OriSample.tab

# 训练（示例: 注意调整-a后面的参数）
wapiti train -a sgd-l1 -t 4 -p patFile OriTrain.tab ModelByOriTrain-sgd-l1.mod
wapiti label -c -m ModelByOriTrain-sgd-l1.mod OriSample.tab LabelOriSampleByOriTrainModel-sgd-l1.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-sgd-l1.tab

# 预测
wapiti train -a sgd-l1 -t 4 -p patFile OriTrain.tab ModelByOriTrain-sgd-l1.mod
wapiti label -c -m ModelByOriTrain-sgd-l1.mod OriSample.tab LabelOriSampleByOriTrainModel-sgd-l1.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-sgd-l1.tab
```
详细的训练，预测结果见Result.md(使用json2tab.py)和Result2.md（使用json2tab_2.py）

### 3 结果整理成新的json文件

使用json2tab_2.py提取的tab文件，"wapiti train -a sgd-l1"的预测结果（tab2/LabelOriSampleByOriTrainModel-sgd-l1.tab，第5列是新预测的结果，将该列的结果写入新的json文件即可）。
```{bash}
for f in $(grep -v '^$' tab2/LabelOriSampleByOriTrainModel-sgd-l1.tab | cut -f2 | cut -d: -f1 | uniq); do
  grep -F $f tab2/LabelOriSampleByOriTrainModel-sgd-l1.tab > tmp/${f%.*}.pred
done


```
