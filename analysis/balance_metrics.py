import json, sys, os, argparse, math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--month', '-t', required=False)
parser.add_argument('--format', '-f', nargs='+', required=True)
parser.add_argument('--metric', '-m', required=False)
args = parser.parse_args()

all_months = ['2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', \
              '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02', \
              '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11']
data = None
info = None

# Only look at pokemon with usage percentage above some threshold epsilon
epsilon = 0

# Degree used in diversity metric; for Simpson Index and Renyi Entropy, must equal 2. 
q = 2

def read_file(month, format):
    global data
    global info
    file_path = 'data/' + month + '/' + format + '.json'
    with open(file_path, 'rb') as data_file:
        data = json.load(data_file)
        info = data['info']
        data = [(k,v) for k,v in data['data'].items()]
    data.sort(key=lambda x: x[1]['Raw count'])

def gini():
    numerator = 0
    denominator = 0
    for i in data:
        for j in data:
            numerator += abs(i[1]['Raw count'] - j[1]['Raw count'])
        denominator += i[1]['Raw count']
    denominator = 2*len(data)*denominator
    return numerator/float(denominator)

def richness():
    counter = 0
    for pokemon in data:
        if pokemon[1]['Raw count']/float(info['number of battles']) > epsilon:
            counter += 1
    return counter

def diversity():
    # The limit of the diversity expression is undefined but well-defined as q -> 1, and equals 
    # the exponential of the Shannon entropy
    if q == 1:
        return math.exp(shannon())
    wgm = 0 # weighted generalized mean
    for pokemon in data:
        p = pokemon[1]['Raw count']/float(info['number of battles'])
        if p < epsilon:
            continue
        wgm += p**q
    return wgm**(1/(1-q))

def shannon():
    H = 0
    for pokemon in data:
        p = pokemon[1]['Raw count']/float(info['number of battles'])
        if p < epsilon:
            continue
        H -= p*math.log(p)
    return H

def gini_simpson():
    return 1-simpson()

def simpson():
    global q
    q = 2
    return 1/diversity()

def renyi():
    global q
    q = 2
    return math.log(diversity())

def berger_parker():
    return data[0][1]['Raw count']/float(info['number of battles'])

all_metrics = {'gini': gini, 'richness': richness, 'diversity': diversity, 'shannon': shannon, \
               'gini_simpson': gini_simpson, 'simpson': simpson, 'renyi': renyi, 'berger_parker': berger_parker}

if __name__ == '__main__':
    month = None
    if args.month:
        month = args.month
        for tier in args.format:
            read_file(month, tier)
            print all_metrics[args.metric]()
    else: 
        plt.figure(figsize=(12,8))
        for tier in args.format:
            vals = []
            for month in all_months:
                read_file(month, tier)
                vals.append(all_metrics[args.metric]())
            plt.plot(range(len(all_months)), vals, label=tier)
        if len(args.format) > 1:
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.ylabel(args.metric)
        plt.xlabel('month')
        plt.xticks(range(len(all_months)), all_months, rotation='vertical')
        plt.subplots_adjust(bottom=0.2, right=0.75)
        plt.show()

