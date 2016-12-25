import json, sys, os, argparse, math

parser = argparse.ArgumentParser()
parser.add_argument('--month', '-m', required=True)
parser.add_argument('--tier', '-t', required=True)
args = parser.parse_args()

data = None
info = None

def read_file():
    global data
    global info
    file_path = 'data/' + args.month + '/' + args.tier + '.json'
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

# Number of pokemon with usage percentage above some threshold epsilon
def richness(epsilon):
    counter = 0
    for pokemon in data:
        if pokemon[1]['Raw count']/float(info['number of battles']) > epsilon:
            counter += 1
    return counter

def diversity(q, epsilon=0):
    # The limit of the diversity expression is undefined but well-defined as q -> 1, and equals 
    # the exponential of the Shannon entropy
    if q == 1:
        return math.exp(shannon(epsilon))
    wgm = 0 # weighted generalized mean
    for pokemon in data:
        p = pokemon[1]['Raw count']/float(info['number of battles'])
        if p < epsilon:
            continue
        wgm += p**q
    return wgm**(1/(1-q))

def shannon(epsilon=0):
    H = 0
    for pokemon in data:
        p = pokemon[1]['Raw count']/float(info['number of battles'])
        if p < epsilon:
            continue
        H -= p*math.log(p)
    return H

def gini_simpson(epsilon=0):
    return 1-simpson(epsilon)

def simpson(epsilon=0):
    return 1/diversity(2, epsilon)

def renyi(q, epsilon=0):
    return math.log(diversity(q, epsilon))

def berger_parker():
    return data[0]['Raw count']/float(info('number of battles'))

if __name__ == '__main__':
    read_file()
    print gini()
