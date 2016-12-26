import json

def read_file(month, format, listify=True):
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

def usage_proportion(pokemon, info):
    return pokemon['Raw count']/float(info['number of battles'])