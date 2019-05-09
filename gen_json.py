#!/usr/bin/python3
import sys
import json
fin_json_  = sys.argv[1]
fpred_     = sys.argv[2]
fout_json_ = sys.argv[3]

# fpred_ = "tmp/PubMed-16371368.pred"
with open(fpred_) as fpred:
	fred_con = [s.rstrip("\n").split("\t") for s in fpred]

fred_con = [ tuple(int(i) for i in spos.split(':')[1:]) + (obj,) for spos, obj in fred_con ]

class TAB_ERROR(Exception):
	def __init__(self, *data):
		self.expression = data

nfred = [ ]
front = [ ]

def zip_pos(L):
	if not L[0][2].startswith("B-"):
		raise TAB_ERROR("invalid:", L)
	if (len(L) > 1) and (not L[-1][2].startswith("E-")):
		raise TAB_ERROR("invalid:", L)
	if not all(e[2].startswith("I-") for e in L[1:-1]):
		raise TAB_ERROR("invalid:", L)
	if not (len(set(e[2][2:] for e in L)) == 1):
		raise TAB_ERROR("invalid:", L)
	return (L[0][0], L[-1][1], L[0][2][2:])

for s, e, o in fred_con:
	if o.startswith("B-"):
		if front:
			nfred.append(zip_pos(front))
			front.clear()
			front.append((s, e, o))
		else:
			front.append((s, e, o))
	elif o.startswith("I-"):
		if not front:
			raise TAB_ERROR("I- without B- before", o)
		else:
			front.append((s, e, o))
	elif o.startswith("E-"):
		if not front:
			raise TAB_ERROR("E- without B- before", o)
		else:
			front.append((s, e, o))
			nfred.append(zip_pos(front))
			front.clear()
	else:
		raise TAB_ERROR("not begin with B/I/O", o)
if front:
	nfred.append(zip_pos(front))
	front.clear()

# s = json_data['text']
# [s[istart:iend] for istart, iend, o in nfred]
# ['gain-of-function', 'mutation', 'gain-of-function', 'mutations', 'hematopoietic malignancies', 'accelerated', 'increased', 'catalytic activity', 'increased', 'interactions', 'catalytic activity', 'increase', 'elevated', 'catalytic activity']

# fin_json_ = "data/AGAC_sample/PubMed-16371368.json"
with open(fin_json_) as fin_json:
	json_data = json.load(fin_json)

del json_data['relations']
json_data['denotations'] = [{'id':"T" + str(i + 1), 'span': {'begin': pstart, 'end': pend}, 'obj': obj} for i, (pstart, pend, obj) in enumerate(nfred)]

with open(fout_json_, "w") as fout_json:
	json.dump(json_data, fout_json)
