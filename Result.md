### 训练参数调整（使用json2tab.py提取的tab文件）
（注：wapiti train -a bcd因运行时间过长，未进行测试，此外这部分测试相当于-i参数调到最大时的结果）
```{bash}
#（1）sgd-l1
wapiti train -a sgd-l1 -t 4 -p patFile Data1.tab ModelByData1-sgd-l1.mod
wapiti label -c -m ModelByData1-sgd-l1.mod Data2.tab LabelData2ByData1Mod-sgd-l1.tab
perl conlleval.pl -d $'\t' < LabelData2ByData1Mod-sgd-l1.tab
# processed 14306 tokens with 679 phrases; found: 219 phrases; correct: 75.
# accuracy:  89.77%; precision:  34.25%; recall:  11.05%; FB1:  16.70
#               CPA: precision:  16.67%; recall:   3.57%; FB1:   5.88  6
#           Disease: precision:  25.81%; recall:   9.30%; FB1:  13.68  31
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#              Gene: precision:  34.78%; recall:   7.41%; FB1:  12.21  23
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   7.69%; recall:   2.15%; FB1:   3.36  26
#            NegReg: precision:  51.43%; recall:  25.35%; FB1:  33.96  35
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  44.44%; recall:  17.14%; FB1:  24.74  27
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  3
#               Reg: precision:  14.29%; recall:   4.76%; FB1:   7.14  14
#               Var: precision:  45.28%; recall:  17.02%; FB1:  24.74  53

#（2）l-bfgs
wapiti train -a l-bfgs -t 4 -p patFile Data1.tab ModelByData1-l-bfgs.mod
wapiti label -c -m ModelByData1-l-bfgs.mod Data2.tab LabelData2ByData1Mod-l-bfgs.tab
perl conlleval.pl -d $'\t' < LabelData2ByData1Mod-l-bfgs.tab
# processed 14306 tokens with 679 phrases; found: 110 phrases; correct: 52.
# accuracy:  90.33%; precision:  47.27%; recall:   7.66%; FB1:  13.18
#               CPA: precision:  50.00%; recall:   3.57%; FB1:   6.67  2
#           Disease: precision:  25.00%; recall:   2.33%; FB1:   4.26  8
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  33.33%; recall:   0.93%; FB1:   1.80  3
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:  18.18%; recall:   2.15%; FB1:   3.85  11
#            NegReg: precision:  53.12%; recall:  23.94%; FB1:  33.01  32
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  50.00%; recall:  10.00%; FB1:  16.67  14
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  40.00%; recall:   4.76%; FB1:   8.51  5
#               Var: precision:  57.14%; recall:  14.18%; FB1:  22.73  35

#（3）rprop+
wapiti train -a rprop+ -t 4 -p patFile Data1.tab ModelByData1-rprop+.mod
wapiti label -c -m ModelByData1-rprop+.mod Data2.tab LabelData2ByData1Mod-rprop+.tab
perl conlleval.pl -d $'\t' < LabelData2ByData1Mod-rprop+.tab
# processed 14306 tokens with 679 phrases; found: 66 phrases; correct: 32.
# accuracy:  90.34%; precision:  48.48%; recall:   4.71%; FB1:   8.59
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  62.50%; recall:   5.81%; FB1:  10.64  8
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  66.67%; recall:   1.85%; FB1:   3.60  3
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  2
#            NegReg: precision:  42.11%; recall:  11.27%; FB1:  17.78  19
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  58.33%; recall:  10.00%; FB1:  17.07  12
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  33.33%; recall:   2.38%; FB1:   4.44  3
#               Var: precision:  47.37%; recall:   6.38%; FB1:  11.25  19

#（4）rprop-
wapiti train -a rprop- -t 4 -p patFile Data1.tab ModelByData1-rprop-.mod
wapiti label -c -m ModelByData1-rprop-.mod Data2.tab LabelData2ByData1Mod-rprop-.tab
perl conlleval.pl -d $'\t' < LabelData2ByData1Mod-rprop-.tab
# processed 14306 tokens with 679 phrases; found: 53 phrases; correct: 25.
# accuracy:  90.29%; precision:  47.17%; recall:   3.68%; FB1:   6.83
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  83.33%; recall:   5.81%; FB1:  10.87  6
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  25.00%; recall:   0.93%; FB1:   1.79  4
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#            NegReg: precision:  38.46%; recall:   7.04%; FB1:  11.90  13
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  42.86%; recall:   4.29%; FB1:   7.79  7
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:  66.67%; recall:   4.76%; FB1:   8.89  3
#               Var: precision:  47.37%; recall:   6.38%; FB1:  11.25  19
```

### 预测（使用json2tab.py提取的tab文件）
```{bash}
#（1）sgd-l1
wapiti train -a sgd-l1 -t 4 -p patFile OriTrain.tab ModelByOriTrain-sgd-l1.mod
wapiti label -c -m ModelByOriTrain-sgd-l1.mod OriSample.tab LabelOriSampleByOriTrainModel-sgd-l1.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-sgd-l1.tab
# processed 13866 tokens with 831 phrases; found: 287 phrases; correct: 109.
# accuracy:  87.38%; precision:  37.98%; recall:  13.12%; FB1:  19.50
#               CPA: precision:  25.00%; recall:   3.41%; FB1:   6.00  12
#           Disease: precision:  40.00%; recall:  12.77%; FB1:  19.35  15
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  41.67%; recall:  13.64%; FB1:  20.55  36
#       Interaction: precision: 100.00%; recall:   9.09%; FB1:  16.67  1
#               MPA: precision:  14.71%; recall:   5.15%; FB1:   7.63  34
#            NegReg: precision:  48.84%; recall:  23.33%; FB1:  31.58  43
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#            PosReg: precision:  44.26%; recall:  22.88%; FB1:  30.17  61
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  6
#               Var: precision:  39.74%; recall:  17.71%; FB1:  24.51  78

#（2）l-bfgs
wapiti train -a l-bfgs -t 4 -p patFile OriTrain.tab ModelByOriTrain-l-bfgs.mod
wapiti label -c -m ModelByOriTrain-l-bfgs.mod OriSample.tab LabelOriSampleByOriTrainModel-l-bfgs.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-l-bfgs.tab
# processed 13866 tokens with 831 phrases; found: 0 phrases; correct: 0.
# accuracy:  87.81%; precision:   0.00%; recall:   0.00%; FB1:   0.00
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            NegReg: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Var: precision:   0.00%; recall:   0.00%; FB1:   0.00  0

#（3）rprop+
wapiti train -a rprop+ -t 4 -p patFile OriTrain.tab ModelByOriTrain-rprop+.mod
wapiti label -c -m ModelByOriTrain-rprop+.mod OriSample.tab LabelOriSampleByOriTrainModel-rprop+.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-rprop+.tab
# processed 13866 tokens with 831 phrases; found: 90 phrases; correct: 47.
# accuracy:  87.95%; precision:  52.22%; recall:   5.66%; FB1:  10.21
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#           Disease: precision:  60.00%; recall:   6.38%; FB1:  11.54  5
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  60.00%; recall:   5.45%; FB1:  10.00  10
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#            NegReg: precision:  56.25%; recall:  10.00%; FB1:  16.98  16
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  46.43%; recall:  11.02%; FB1:  17.81  28
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Var: precision:  55.17%; recall:   9.14%; FB1:  15.69  29

#（4）rprop-
wapiti train -a rprop- -t 4 -p patFile OriTrain.tab ModelByOriTrain-rprop-.mod
wapiti label -c -m ModelByOriTrain-rprop-.mod OriSample.tab LabelOriSampleByOriTrainModel-rprop-.tab
perl conlleval.pl -d $'\t' < LabelOriSampleByOriTrainModel-rprop-.tab
# processed 13866 tokens with 831 phrases; found: 54 phrases; correct: 31.
# accuracy:  87.94%; precision:  57.41%; recall:   3.73%; FB1:   7.01
#               CPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#           Disease: precision:  57.14%; recall:   8.51%; FB1:  14.81  7
#            Enzyme: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#              Gene: precision:  71.43%; recall:   4.55%; FB1:   8.55  7
#       Interaction: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               MPA: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            NegReg: precision:  54.55%; recall:   6.67%; FB1:  11.88  11
#           Pathway: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#            PosReg: precision:  60.00%; recall:   2.54%; FB1:   4.88  5
#           Protein: precision:   0.00%; recall:   0.00%; FB1:   0.00  0
#               Reg: precision:   0.00%; recall:   0.00%; FB1:   0.00  1
#               Var: precision:  56.52%; recall:   7.43%; FB1:  13.13  23
```
```
