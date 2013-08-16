
from sklearn import svm
import numpy
import types
import sys
# step 1 .. M

# convert from list to numpy array


def convert_to_array(x):
    if isinstance(x, types.ListType):
        return numpy.array(x)
    else:
        print 'Not a list type'

# read a csv file and convert it to
# numpy array.. Return numpy array


def read_and_clean(fname):
	fp = open(fname)
	data_array=[]
	label=[]
	headerline = fp.readline()
	for line in fp:
		print len(data_array)	
		linesplit = line.split(",")
		data = convert_to_array([float(i) for i in linesplit[1:]])
		data_array.append(data)	
		label.append(linesplit[0])	
	return (data_array,convert_to_array(label))
# simple version of the code above.. Used to read
# trainLabel.csv, which is just a single column of numbers
def read_and_clean_simple(fname):
    try:
        data = numpy.array([int(i) for i in open(fname, "r").readlines()])
        return data
    except:
        pass
# send in data of the form
# 2.8089094884322816,-0.2428941541280098,-0.54642134078742799,
# 0.25516185655651813,...,.. (N items per row)
# N is the parameter space (cardinality) of classifer
# training data has a 1000 rows
training_array,training_label = read_and_clean("handwrite_train.csv")

clf = svm.SVC()
clf.fit(training_array, training_label)

# next we predict
predict = clf.predict(read_and_clean('handwrite_test.csv'))

# save it to file
numpy.savetxt("submit.csv", predict.astype(int), fmt='%d', delimiter=",")
