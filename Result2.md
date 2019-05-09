（注：wapiti train -a bcd因运行时间过长，未进行测试，此外这部分测试相当于-i参数调到最大时的结果）
### 准备
```{bash}
# json2tab_2.py运行报错信息与json2tab.py的是一致的
for F in data/AGAC_training/*.json; do FJ=${F##*/}; FJ=OUT_TAB_DIR2/${FJ%.*}.tab; python3 json2tab_2.py $F $FJ; done
# training 用于训练
for f in $(ls OUT_TAB_DIR2); do 
	if [ -f data/AGAC_training/${f%.*}.json ] && [ ! -f data/AGAC_sample/${f%.*}.json ]; 
    then echo ${f%.*}.tab;
  fi; 
done > training_list2.txt
# sample 用于预测
for f in $(ls OUT_TAB_DIR2); do
	if [ -f data/AGAC_sample/${f%.*}.json ]; then
    echo ${f%.*}.tab; 
  fi; 
done > sample_list2.txt

for f in $(cat training_list2.txt); do ln -s ../OUT_TAB_DIR2/$f TRAIN_TAB2/$f; done
for f in $(cat sample_list2.txt); do ln -s ../OUT_TAB_DIR2/$f SAMPLE_TAB2/$f; done

cat $(head -146 training_list2.txt | sed 's#^#TRAIN_TAB2/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > tab2/Data1.tab
cat $(tail -50 training_list2.txt  | sed 's#^#TRAIN_TAB2/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > tab2/Data2.tab

gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' TRAIN_TAB2/*.tab > tab2/OriTrain.tab
gawk -F$"\t" '{if(/^$/) {print $0;} 
else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' SAMPLE_TAB2/*.tab > tab2/OriSample.tab
```

### 训练参数调整（使用json2tab_2.py提取的tab文件）
```{bash}
#（1）sgd-l1
wapiti train -a sgd-l1 -t 4 -p patFile tab2/Data1.tab tab2/ModelByData1-sgd-l1.mod
wapiti label -c -m tab2/ModelByData1-sgd-l1.mod tab2/Data2.tab tab2/LabelData2ByData1Mod-sgd-l1.tab
perl conlleval.pl -d $'\t' < tab2/LabelData2ByData1Mod-sgd-l1.tab
# processed 14306 tokens with 680 phrases; found: 195 phrases; correct: 72.
# accuracy:  89.84%; precision:  36.92%; recall:  10.59%; FB1:  16.46
#               CPA: precision:  33.33%; recall:   7.14%; FB1:  11.76  6
#           Disease: precision:  28.57%; recall:   9.30%; FB1:  14.04  28
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#              Gene: precision:  35.71%; recall:   4.63%; FB1:   8.20  14
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:  10.71%; recall:   3.23%; FB1:   4.96  28
#            NegReg: precision:  48.48%; recall:  22.54%; FB1:  30.77  33
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  50.00%; recall:  20.00%; FB1:  28.57  28
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  23.08%; recall:   7.14%; FB1:  10.91  13
#               Var: precision:  47.73%; recall:  14.79%; FB1:  22.58  44

#（2）l-bfgs
wapiti train -a l-bfgs -t 4 -p patFile tab2/Data1.tab tab2/ModelByData1-l-bfgs.mod
wapiti label -c -m tab2/ModelByData1-l-bfgs.mod tab2/Data2.tab tab2/LabelData2ByData1Mod-l-bfgs.tab
perl conlleval.pl -d $'\t' < tab2/LabelData2ByData1Mod-l-bfgs.tab
# processed 14306 tokens with 679 phrases; found: 94 phrases; correct: 46.
# accuracy:  90.42%; precision:  48.94%; recall:   6.77%; FB1:  11.90
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#           Disease: precision:  16.67%; recall:   1.16%; FB1:   2.17  6
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  66.67%; recall:   1.85%; FB1:   3.60  3
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:  22.22%; recall:   2.15%; FB1:   3.92  9
#            NegReg: precision:  50.00%; recall:  18.31%; FB1:  26.80  26
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  53.85%; recall:  10.00%; FB1:  16.87  13
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  40.00%; recall:   4.76%; FB1:   8.51  5
#               Var: precision:  61.29%; recall:  13.48%; FB1:  22.09  31

#（3）rprop+
wapiti train -a rprop+ -t 4 -p patFile tab2/Data1.tab tab2/ModelByData1-rprop+.mod
wapiti label -c -m tab2/ModelByData1-rprop+.mod tab2/Data2.tab tab2/LabelData2ByData1Mod-rprop+.tab
perl conlleval.pl -d $'\t' < tab2/LabelData2ByData1Mod-rprop+.tab
# processed 14306 tokens with 680 phrases; found: 75 phrases; correct: 38.
# accuracy:  90.39%; precision:  50.67%; recall:   5.59%; FB1:  10.07
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  62.50%; recall:   5.81%; FB1:  10.64  8
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  66.67%; recall:   1.85%; FB1:   3.60  3
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  3
#            NegReg: precision:  47.62%; recall:  14.08%; FB1:  21.74  21
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  53.85%; recall:  10.00%; FB1:  16.87  13
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  33.33%; recall:   2.38%; FB1:   4.44  3
#               Var: precision:  54.17%; recall:   9.15%; FB1:  15.66  24

#（4）rprop-
wapiti train -a rprop- -t 4 -p patFile tab2/Data1.tab tab2/ModelByData1-rprop-.mod
wapiti label -c -m tab2/ModelByData1-rprop-.mod tab2/Data2.tab tab2/LabelData2ByData1Mod-rprop-.tab
perl conlleval.pl -d $'\t' < tab2/LabelData2ByData1Mod-rprop-.tab
# processed 14306 tokens with 680 phrases; found: 53 phrases; correct: 26.
# accuracy:  90.35%; precision:  49.06%; recall:   3.82%; FB1:   7.09
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  83.33%; recall:   5.81%; FB1:  10.87  6
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  25.00%; recall:   0.93%; FB1:   1.79  4
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  2
#            NegReg: precision:  53.85%; recall:   9.86%; FB1:  16.67  13
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  33.33%; recall:   2.86%; FB1:   5.26  6
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  33.33%; recall:   2.38%; FB1:   4.44  3
#               Var: precision:  52.63%; recall:   7.04%; FB1:  12.42  19
```
### 预测（使用json2tab_2.py提取的tab文件）
```{bash}
#（1）sgd-l1
wapiti train -a sgd-l1 -t 4 -p patFile tab2/OriTrain.tab tab2/ModelByOriTrain-sgd-l1.mod
wapiti label -c -m tab2/ModelByOriTrain-sgd-l1.mod tab2/OriSample.tab tab2/LabelOriSampleByOriTrainModel-sgd-l1.tab
perl conlleval.pl -d $'\t' < tab2/LabelOriSampleByOriTrainModel-sgd-l1.tab
# processed 13866 tokens with 834 phrases; found: 241 phrases; correct: 95.
# accuracy:  87.60%; precision:  39.42%; recall:  11.39%; FB1:  17.67
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  7
#           Disease: precision:  26.67%; recall:   8.51%; FB1:  12.90  15
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  47.83%; recall:  10.00%; FB1:  16.54  23
#       Interaction: precision: 100.00%; recall:   9.09%; FB1:  16.67  1
#               MPA: precision:  17.65%; recall:   6.19%; FB1:   9.16  34
#            NegReg: precision:  52.78%; recall:  21.11%; FB1:  30.16  36
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#            PosReg: precision:  46.43%; recall:  22.03%; FB1:  29.89  56
#           Protein: precision: 100.00%; recall:   2.38%; FB1:   4.65  1
#               Reg: precision:  20.00%; recall:   3.12%; FB1:   5.41  5
#               Var: precision:  41.94%; recall:  14.61%; FB1:  21.67  62

#（2）l-bfgs
wapiti train -a l-bfgs -t 4 -p patFile tab2/OriTrain.tab tab2/ModelByOriTrain-l-bfgs.mod
wapiti label -c -m tab2/ModelByOriTrain-l-bfgs.mod tab2/OriSample.tab tab2/LabelOriSampleByOriTrainModel-l-bfgs.tab
perl conlleval.pl -d $'\t' < tab2/LabelOriSampleByOriTrainModel-l-bfgs.tab
# processed 13866 tokens with 834 phrases; found: 134 phrases; correct: 63.
# accuracy:  88.03%; precision:  47.01%; recall:   7.55%; FB1:  13.02
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  4
#           Disease: precision:  40.00%; recall:   4.26%; FB1:   7.69  5
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  55.56%; recall:   4.55%; FB1:   8.40  9
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:  25.00%; recall:   2.06%; FB1:   3.81  8
#            NegReg: precision:  58.06%; recall:  20.00%; FB1:  29.75  31
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  40.54%; recall:  12.71%; FB1:  19.35  37
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  50.00%; recall:   3.12%; FB1:   5.88  2
#               Var: precision:  52.63%; recall:  11.24%; FB1:  18.52  38

#（3）rprop+
wapiti train -a rprop+ -t 4 -p patFile tab2/OriTrain.tab tab2/ModelByOriTrain-rprop+.mod
wapiti label -c -m tab2/ModelByOriTrain-rprop+.mod tab2/OriSample.tab tab2/LabelOriSampleByOriTrainModel-rprop+.tab
perl conlleval.pl -d $'\t' < tab2/LabelOriSampleByOriTrainModel-rprop+.tab
# processed 13866 tokens with 834 phrases; found: 95 phrases; correct: 52.
# accuracy:  88.02%; precision:  54.74%; recall:   6.24%; FB1:  11.19
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#           Disease: precision:  66.67%; recall:   4.26%; FB1:   8.00  3
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  66.67%; recall:   7.27%; FB1:  13.11  12
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  2
#            NegReg: precision:  60.00%; recall:  10.00%; FB1:  17.14  15
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  45.16%; recall:  11.86%; FB1:  18.79  31
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Var: precision:  61.29%; recall:  10.67%; FB1:  18.18  31

#（4）rprop-
wapiti train -a rprop- -t 4 -p patFile tab2/OriTrain.tab tab2/ModelByOriTrain-rprop-.mod
wapiti label -c -m tab2/ModelByOriTrain-rprop-.mod tab2/OriSample.tab tab2/LabelOriSampleByOriTrainModel-rprop-.tab
perl conlleval.pl -d $'\t' < tab2/LabelOriSampleByOriTrainModel-rprop-.tab
# processed 13866 tokens with 834 phrases; found: 63 phrases; correct: 39.
# accuracy:  87.99%; precision:  61.90%; recall:   4.68%; FB1:   8.70
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  57.14%; recall:   8.51%; FB1:  14.81  7
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  77.78%; recall:   6.36%; FB1:  11.76  9
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            NegReg: precision:  54.55%; recall:   6.67%; FB1:  11.88  11
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  50.00%; recall:   3.39%; FB1:   6.35  8
#           Protein: precision: 100.00%; recall:   2.38%; FB1:   4.65  1
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#               Var: precision:  65.38%; recall:   9.55%; FB1:  16.67  26
```
