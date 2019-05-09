#!/usr/bin/env python3
import sys
import re
import json
import numpy

input_json = sys.argv[1]

def get_uniq(ori_data, key):
	s = set( )
	l = list( )
	for e in ori_data:
		k = key(e)
		if k not in s:
			s.add(k)
			l.append(e)
	return l

with open(input_json) as fjson:
	jdata = json.load(fjson)

re_sep   = re.compile(r'(\s+|[\+_,Δ/\.\-"' r"'" r':;\?\(\)!])')
re_blank = re.compile(r'^\s+$')
jtext = jdata['text']
l_jtext = re.split(re_sep,  jtext)
l_jtext = [s for s in l_jtext if len(s) != 0]
is_point = [e in (".", ",", ";", "?", "!") for e in l_jtext]
is_blank = [bool(re.match(re_blank, e)) for e in l_jtext][1:]
is_blank.append(False)
is_full_stop = [i and j for i, j in zip(is_point, is_blank)]

end_index = numpy.cumsum(list(map(len, l_jtext)))
begin_index = (0,) + tuple(end_index[:-1])
word_table = list(zip(l_jtext, begin_index, end_index, is_full_stop))

jcdenotations = jdata['denotations']
jcdenotations = list(map(lambda x : (x['id'], x['span']['begin'], x['span']['end'], x['obj']), jcdenotations))
# 应对重复数据，例如 PubMed-28890134.json 里面 ('T1', 76, 92, 'NegReg'), ('T3', 76, 92, 'NegReg') 
jcdenotations = get_uniq(jcdenotations, key = lambda x : x[1:])
jcdenotations.sort(key = lambda x: x[1])

class DataError(Exception):
	def __init__(self, *data):
		self.expression = data

input_json_name = input_json.split('/')[-1]
tdata = [ ]
for wd in word_table:
	s = wd[0]
	if re.match(re_blank, s):
		continue
	if (not jcdenotations) or (wd[1] < jcdenotations[0][1]):
		tdata.append((s, str.join(":", (input_json_name, str(wd[1]), str(wd[2]))), 'O'))
		if wd[3]:
			tdata.append(())
	else:
		jde = jcdenotations[0]
		if wd[1] == jde[1]:
			tdata.append((s, str.join(":", (input_json_name, str(wd[1]), str(wd[2]))), 'B-' + jde[3]))
			if wd[3]:
				tdata.append(())
			if wd[2] == jde[2]:
				jcdenotations.pop(0)
			elif wd[2] > jde[2]:
				raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])
		else:
			if wd[2] < jde[2]:
				tdata.append((s, str.join(":", (input_json_name, str(wd[1]), str(wd[2]))), 'I-' + jde[3]))
				if wd[3]:
					tdata.append(())
			elif wd[2] == jde[2]:
				tdata.append((s, str.join(":", (input_json_name, str(wd[1]), str(wd[2]))), 'E-' + jde[3]))
				if wd[3]:
					tdata.append(())
				jcdenotations.pop(0)
			else: # wd[2] > jde[2]
				raise DataError(input_json_name, wd, jde, jtext[jde[1]:jde[2]])

output_tab = sys.argv[2]
if len(sys.argv) < 4:
	with open(output_tab, 'w') as ftab:
		for line in tdata:
			print('\t'.join(line), file = ftab)
