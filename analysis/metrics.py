import json, sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--month', '-m', required=True)
parser.add_argument('--tier', '-t', required=True)
args = parser.parse_args()

data = None

def read_file():
    file_path = 'data/' + args.month + '/' + args.tier + '.json'
    with open(file_path, 'rb') as data_file:
        data = [(k,v) for k,v in json.load(data_file)['data'].items()]
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

if __name__ == '__main__':
    read_file()
    print gini()