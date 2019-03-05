import csv
import random
import matplotlib.pyplot as plt

def plot_cluster(clusters,centroids):
	for key,value in clusters.items():
		if value == 0:
			c = 'red'
			plt.scatter(*list(key), s = 20, c = c)
		elif value == 1:
			c = 'blue'
			plt.scatter(*list(key), s = 20, c = c)
		else:
			c = random.randint(0,255)
			plt.scatter(*list(key), s = 20, c = c)
	plt.scatter(*zip(*centroids), s = 50, c = 'black')
	plt.show()


def formClusters(Centroids,dataset):
	cluster = {}
	for point in dataset:
		cdist = []
		for c in Centroids:
			dist = (sum([(x-y)**2 for x,y in zip(point,c)]))**0.5
			cdist.append(dist)
		print("Distance vector is: ",cdist)
		cluster[point] = cdist.index(min(cdist))
	return cluster

def compCentroid(points,n):
	if points != []:
		centroid = []
		for i in range(n):
			val = sum([axis[i] for axis in points]) / len(points)
			centroid.append(val)
		return(tuple(centroid))

filename = input("Enter Filename to which you want to apply k-mean: ")
attributes = []
data = []
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file)
    attributes = next(csv_reader)
    for row in csv_reader:
        data.append(tuple(map(float,row[1:])))

print("datapoints extracted are: ",data)

k = int(input("Enter number of clusters required: "))
centroids=[]
i = 0
while i != k:
	point = tuple(data[random.randint(0,(len(data)-1))])
	if point not in centroids:
		centroids.append(point)
		i = i + 1
print("Randomly assigned centroids are: ",centroids)
old_clusters = formClusters(centroids,data)
print("First cluster: ",old_clusters)
counter = 0
new_clusters = old_clusters
while True:
	new_k_cent = []
	for i in range(k):
		k_th_clus = [x for x,y in new_clusters.items() if y == i]
		new_k_cent.append(compCentroid(k_th_clus,(len(attributes)-1)))
	print("new centroids: ",new_k_cent)
	old_clusters = new_clusters
	new_clusters = formClusters(new_k_cent,data)
	if len(new_k_cent[0]) == 2:
		plot_cluster(new_clusters,new_k_cent)
	print("new cluster: ",new_clusters)
	if new_clusters == old_clusters:
		counter = counter + 1
		if counter == 2:
			break
print("Final cluster obtained is : ",new_clusters)
print("Centroids are: ",new_k_cent)