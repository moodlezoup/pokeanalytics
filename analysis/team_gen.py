import util
import argparse
import math
import snap
import re
from pprint import pprint


# parser = argparse.ArgumentParser()
# parser.add_argument('--month', '-t', required=True)
# parser.add_argument('--format', '-f', required=True)
# args = parser.parse_args()

data = None
info = None

# Only look at pokemon with usage percentage above some threshold epsilon
epsilon = 0.02
usage_weight = 0.5
num_threats = 10
adv_threshold = 0.5


def getEdgeWeight(i, j, network):
    edge = network.GetEI(i, j)
    return network.GetFltAttrDatE(edge, 'weight')


def advantage(team, network, name_to_nid, nid_to_name, usage=None, normalize=True):
    advantage = {}

    for pokemon in team:
        if pokemon not in name_to_nid:
            print pokemon + ' not found'
            continue
        nid = name_to_nid[pokemon]

        for nbr in util.getOutNeighbors(network, nid):
            if nbr in advantage:
                advantage[nbr] += getEdgeWeight(nid, nbr, network)
            else:
                advantage[nbr] = getEdgeWeight(nid, nbr, network)

        for nbr in util.getInNeighbors(network, nid):
            if nbr in advantage:
                advantage[nbr] -= getEdgeWeight(nbr, nid, network)
            else:
                advantage[nbr] = -getEdgeWeight(nbr, nid, network)

    if usage:
        advantage = {nid: (usage[nid_to_name[nid]] ** usage_weight) * val for nid, val in advantage.items()}

    if normalize:
        max_val = max([abs(val) for val in advantage.values()])
        advantage = {nid: val / max_val for nid, val in advantage.items()}

    print 'Team'
    pprint(team)
    advantage = {nid_to_name[nid]: val for nid, val in advantage.items()}

    # print '\nStrengths'
    # pprint(list(reversed(sorted(advantage.items(), key=lambda x: x[1])[-num_threats:])))

    print '\nWeaknesses'
    pprint(sorted(advantage.items(), key=lambda x: x[1])[:num_threats])

    return advantage


def getPokemonName(line, names):
    res = {
        'name1': r'^([A-Z][a-z0-9.:\']+(?:[- ][A-Za-z][a-z0-9.:\']*)*)(?=$| \(| @)',
        'name2': r'(?<=\()([A-Z][a-z0-9.:\']+(?:[- ][A-Za-z][a-z0-9.:\']*)*)(?=\))',
    }
    res = {n: re.compile(r) for n, r in res.items()}

    match = res['name2'].split(line, maxsplit=1)
    if len(match) != 3:
        match = res['name1'].split(line, maxsplit=1)
    if len(match) == 3 and match[1] in names:
        return match[1]
    return None


def getAllTeams(tier, names):
    teams = []
    likes = []
    with open('data/importable.txt', 'r') as f:
        pokemon = []
        team_likes = 0
        keep = False
        last_line_empty = False

        for line in f:
            line = line.strip()
            if not line:
                last_line_empty = True
                continue

            if re.search('=== .* ===', line):
                if len(pokemon) == 6 and pokemon[:] not in teams:
                    teams.append(pokemon[:])
                    likes.append(team_likes)
                pokemon = []

                line_tier = line.split(' ')[1][1:-1]
                team_likes = re.search('(\d*) Likes', line).group(0)
                keep = line_tier == tier

            if keep and last_line_empty:
                name = getPokemonName(line, names)
                if name:
                    pokemon.append(name)

    print len(teams)
    return zip(teams, likes)


def getNetwork(data):
    name_to_nid = {}
    nid_to_name = {}
    network = snap.TNEANet.New()
    network.AddFltAttrE('weight')

    for i, pokemon in enumerate(data):
        if util.usageProportion(pokemon[1], info) < epsilon:
            continue
        name_to_nid[pokemon[0]] = i
        nid_to_name[i] = pokemon[0]
        network.AddNode(i)

    for i, pokemon in enumerate(data):
        if util.usageProportion(pokemon[1], info) < epsilon:
            continue
        for check, vals in pokemon[1]['Checks and Counters'].items():
            if check not in name_to_nid:
                continue

            j = name_to_nid[check]
            if not network.IsNode(j):
                continue

            score = vals[1] - 4 * vals[2]
            if score < adv_threshold:
                continue

            network.AddEdge(j, i)
            edge = network.GetEI(j, i)
            network.AddFltAttrDatE(edge, score, 'weight')

    print network.GetNodes(), network.GetEdges()
    return network, name_to_nid, nid_to_name


if __name__ == '__main__':
    month = '2017-10'
    tier = 'gen7ou-1500'
    data, info = util.readFile(month, tier)
    usage_dict = util.usageDict(month, 'gen7ou-1825')

    network, name_to_nid, nid_to_name = getNetwork(data)
    teams = getAllTeams('gen7ou', name_to_nid.keys())
    advantage(teams[2][0], network, name_to_nid, nid_to_name, usage=usage_dict, normalize=False)
