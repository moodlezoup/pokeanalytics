import json
import snap


def readFile(month, format, listify=True):
    data = None
    info = None
    file_path = 'data/' + month + '/' + format + '.json'
    with open(file_path, 'rb') as data_file:
        usage = json.load(data_file)
    info = usage['info']
    data = usage['data']
    if listify:
        data = [(k,v) for k,v in data.items()]
        data.sort(key=lambda x: x[1]['Raw count'])
    return data, info


def usageDict(month, format):
    data, info = readFile(month, format, listify=False)
    return {k: usageProportion(v, info) for k, v in data.items()}


def usageProportion(pokemon, info):
    return pokemon['Raw count']/float(info['number of battles'])


def getInNeighbors(network, nid):
    node = network.GetNI(nid)
    return [node.GetInNId(i) for i in range(node.GetInDeg())]


def getOutNeighbors(network, nid):
    node = network.GetNI(nid)
    return [node.GetOutNId(i) for i in range(node.GetOutDeg())]
