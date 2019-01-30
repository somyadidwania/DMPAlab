import csv
from itertools import combinations

def support_count(data,C_old):
	cnt = 0
	#print('  C_old  ',C_old)
	#print('  data  ',data)
	C_new = {}
	for i in data:
		for itemset in C_old:
			#print(itemset,' is in ',C_old,' i is : ',i)
			if set(itemset).issubset(i):
				C_new[itemset] = C_new.get(itemset,0)+1
				#print('C_new is ',C_new)
	C_new = dict(sorted(C_new.items()))
	return C_new

def sup_cnt_comparison(C,min_sup):
	L_new = {}
	for itemset,support in C.items():
		if support >= min_sup:
			L_new[itemset] = support
	return L_new

def generate_C(items,i):
	if i < 3:
		items = list(items)
		items.sort()
		return list(combinations(items,i))
	else:
		C_gen = [] 
		for x in range(0,len(items)):
			#print('X is  ',items[x])
			for y in range(x+1,len(items)):
				#print('Y is  ',items[y])
				if(items[x][0:(i-2)] == items[y][0:(i-2)]):
					t = list(items[x][0:(i-2)])
					t.append(items[x][(i-2)])
					t.append(items[y][(i-2)])
					C_gen.append(tuple(t))
		return C_gen

def prune(C,i,tran_1,min_sup):
		subsets_of_C = []
		pruned_C = []
		for key in C:
			for j in range(1,i):
				subsets_of_C = subsets_of_C + generate_C(key,j) 
			subsets_of_C = support_count(tran_1,subsets_of_C)
			if(all(x >= min_sup for x in subsets_of_C.values())):
				pruned_C.append(key)
			print('Subset of C is :', subsets_of_C)
			subsets_of_C = []

		print('pruned C is :',pruned_C)
		return pruned_C

#Reading of csv file
csv.register_dialect('myDialect',delimiter = ',',skipinitialspace=True) #Setting the delimiter
file_name = input("Enter file name: ")
tran = list()
C1 = {}
with open(file_name) as csv_file:
	data = csv.reader(csv_file, dialect = 'myDialect')
	for row in data:
		for i in range(1,len(row)):
			if row[i] is not '':
				C1[row[i]] = C1.get(row[i],0) + 1
		tran.append(row)
print(tran)
C1 = dict(sorted(C1.items()))
print("C1 item set is ", C1)
L_final = []
min_sup = int(input("Enter the minimum support : "))
#L1 generation
L1 = sup_cnt_comparison(C1,min_sup)
print("L1 item set is ", L1)
L_final = L_final + list(L1.keys())
C2 = generate_C(list(L1.keys()),2)
print("C2 item set is ", C2)
C2 = support_count(tran,C2)
print("New C2 is = ",C2)
L2 = sup_cnt_comparison(C2,min_sup)
L_final = L_final + list(L2.keys())
print('L2 is :',L2)

#Apriori Starts

i=3
C = generate_C(list(L2.keys()),i)
print('C',i,' is : ',C)
while len(C) > 0:
	pruned_C = prune(C,i,tran,min_sup)
	print('Puned C',i,' is : ',pruned_C)
	if len(pruned_C)>0:
		C = support_count(tran,C)
		print('C',i,' is : ',C)
		L = sup_cnt_comparison(C,min_sup)
		L_final = L_final + list(L.keys())
		print('Now L',i,' is : ',L)
		i = i + 1
		C = generate_C(list(C.keys()),i)
		print('Now C',i,' generate is : ',C)
		if len(C) == 0:
			break
	else:
		break
print('\n\n')
print('Final L generated after successfully running Apriori Algorithm : ',L_final)
