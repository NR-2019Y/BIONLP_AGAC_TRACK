# BIONLP_AGAC_TRACK

AGAC track (Course Project)

## 1 数据来源

http://pubannotation.org/projects/AGAC_training/annotations.tgz \# 解压的250个\*.json文件后放到 data/AGAC_training 目录

http://pubannotation.org/projects/AGAC_sample/annotations.tgz   \# 解压后的50个\*.json文件后放到 data/AGAC_sample 目录

## 2 流程

### 2.1 数据检查和预处理

对原始的 AGAC_training 和 AGAC_sample 中的 json 文件进行检查和预处理
```{bash}
# json2tab.py 可以换成 json2tab_2.py
for F in data/AGAC_training/*.json; do
  FJ=${F##*/}; FJ=OUT_TAB_DIR/${FJ%.*}.tab; 
  python3 json2tab.py $F $FJ; 
done
```


