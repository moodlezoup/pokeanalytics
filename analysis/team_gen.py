import util
import argparse
import math
import snap


# parser = argparse.ArgumentParser()
# parser.add_argument('--month', '-t', required=True)
# parser.add_argument('--format', '-f', required=True)
# args = parser.parse_args()

data = None
info = None

# Only look at pokemon with usage percentage above some threshold epsilon
epsilon = 0.05


def getNetwork(data):
    name_to_nid = {}
    nid_to_name = {}
    network = snap.TNEANet.New()
    network.AddFltAttrE('weight')

    for i, pokemon in enumerate(data):
        name_to_nid[pokemon[0]] = i
        nid_to_name[i] = pokemon[0]
        if util.usage_proportion(pokemon[1], info) < epsilon:
            continue
        network.AddNode(i)

    for i, pokemon in enumerate(data):
        if util.usage_proportion(pokemon[1], info) < epsilon:
            continue
        for check, vals in pokemon[1]['Checks and Counters'].items():
            if check not in name_to_nid:
                continue

            j = name_to_nid[check]
            if not network.IsNode(j):
                continue

            score = vals[1] - 4 * vals[2]
            if score < 0.7:
                continue

            network.AddEdge(j, i)
            edge = network.GetEI(j, i)
            network.AddFltAttrDatE(edge, score, 'weight')

    print network.GetNodes(), network.GetEdges()
    return network, name_to_nid, nid_to_name


if __name__ == '__main__':
    month = '2017-10'
    tier = 'gen7ou-0'
    data, info = util.read_file(month, tier)
    getNetwork(data)
