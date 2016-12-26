import util, sys, os, argparse, math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--months', '-t', nargs=2, required=False)
parser.add_argument('--format', '-f', nargs='+', required=True)
parser.add_argument('--ignore', '-i', nargs='+', required=False)
parser.add_argument('--metric', '-m', nargs='+', required=False)
args = parser.parse_args()

all_months = ['2014-11', '2014-12', '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', \
              '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01', '2016-02', \
              '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11']
data = None
info = None

def euclidean(x, y):
    distance = 0
    for k in set(x.keys() + y.keys()):
        if args.ignore and k in args.ignore:
            continue
        distance += (x.get(k, 0) - y.get(k, 0))**2
    return math.sqrt(distance)

def manhattan(x, y):
    distance = 0
    for k in set(x.keys() + y.keys()):
        if args.ignore and k in args.ignore:
            continue
        distance += abs(x.get(k, 0) - y.get(k, 0))
    return distance

def chebyshev(x, y):
    distance = 0
    for k in set(x.keys() + y.keys()):
        if args.ignore and k in args.ignore:
            continue
        distance = max(distance, abs(x.get(k, 0) - y.get(k, 0)))
    return distance

if __name__ == '__main__':
    metrics = args.metric or ['euclidean', 'manhattan', 'chebyshev']
    if args.months:
        for tier in args.format:
            print '========== ' + tier + ' =========='
            data1, info1 = util.read_file(args.months[0], tier, listify=False)
            data2, info2 = util.read_file(args.months[1], tier, listify=False)
            x = {k: util.usage_proportion(v, info1) for k, v in data1.items()}
            y = {k: util.usage_proportion(v, info2) for k, v in data2.items()}
            if 'euclidean' in metrics: print 'Euclidean: ' + str(euclidean(x, y))
            if 'manhattan' in metrics: print 'Manhattan: ' + str(manhattan(x, y))
            if 'chebyshev' in metrics: print 'Chebyshev: ' + str(chebyshev(x, y))
            print ''
    else:
        plt.figure(figsize=(12,8))
        for tier in args.format:
            euclidean_distances = []
            manhattan_distances = []
            chebyshev_distances = []
            name_to_vals = {'euclidean': euclidean_distances, 'manhattan': manhattan_distances, \
                            'chebyshev': chebyshev_distances}
            for i in range(len(all_months)):
                if i == 0:
                    continue
                data1, info1 = util.read_file(all_months[i-1], tier, listify=False)
                data2, info2 = util.read_file(all_months[i], tier, listify=False)
                x = {k: util.usage_proportion(v, info1) for k, v in data1.items()}
                y = {k: util.usage_proportion(v, info2) for k, v in data2.items()}
                euclidean_distances.append(euclidean(x, y))
                manhattan_distances.append(manhattan(x, y))
                chebyshev_distances.append(chebyshev(x, y))
            for metric in metrics:
                distances = None
                vals = name_to_vals[metric]
                plt.plot(range(len(all_months)-1), vals, label=(tier + '_' + metric))
        if len(args.format) > 1 or len(metrics) > 1:
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.ylabel('distance')
        plt.xlabel('month')
        plt.xticks(range(len(all_months)-1), all_months[1:], rotation='vertical')
        plt.subplots_adjust(bottom=0.2, right=0.75)
        plt.show()







