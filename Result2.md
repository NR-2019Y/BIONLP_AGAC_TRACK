### 准备
```{bash}
for F in data/AGAC_training/*.json; do FJ=${F##*/}; FJ=OUT_TAB_DIR2/${FJ%.*}.tab; python3 json2tab_2.py $F $FJ; done
# training
for f in $(ls OUT_TAB_DIR2); do 
	if [ -f data/AGAC_training/${f%.*}.json ] && [ ! -f data/AGAC_sample/${f%.*}.json ]; 
    then echo ${f%.*}.tab;
  fi; 
done > training_list2.txt
# sample
for f in $(ls OUT_TAB_DIR2); do
	if [ -f data/AGAC_sample/${f%.*}.json ]; then
    echo ${f%.*}.tab; 
  fi; 
done > sample_list2.txt

for f in $(cat training_list2.txt); do ln -s ../OUT_TAB_DIR2/$f TRAIN_TAB2/$f; done
for f in $(cat sample_list2.txt); do ln -s ../OUT_TAB_DIR2/$f SAMPLE_TAB2/$f; done

cat $(head -146 training_list2.txt | sed 's#^#TRAIN_TAB2/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > tab2/Data1.tab
cat $(tail -50 training_list2.txt  | sed 's#^#TRAIN_TAB2/#') | 
gawk -F$"\t" '{if(/^$/) {print $0;} else {printf "%s\t%s\t%s\t%s\n", $1, $2, "O", $3} }' > tab2/Data2.tab


```
