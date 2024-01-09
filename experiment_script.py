import networkx as nx
from utils import *
import time

DISCLAIMER = -1
rg = np.random.default_rng()
nvars = 2  # number of choice variants
print("Specifying the community")
# ----------------------------------------------------------
# community specification
# ----------------------------------------------------------
# specify community net
net = nx.complete_graph(200)
setattr(net, 'nvars', nvars)  # associte 'nvars' with 'net'

# set parameters of community actors
for n in net:
    net.nodes[n]['rho'] = 20
    if n == 0:
        net.nodes[n]['choice'] = 0
    else:
        net.nodes[n]['choice'] = DISCLAIMER
print(net)
# set parameters of community channels
for channel in net.edges:
    alice = min(channel)
    if alice == 0:
        net.edges[channel]['a'] = 1.0
        net.edges[channel]['D'] = define_dialogue_matrix(
            1.0,
            rg.uniform(low=0.2, high=0.6)
        )
    else:
        net.edges[channel]['a'] = 1.0
        net.edges[channel]['D'] = define_dialogue_matrix(
            rg.uniform(low=0.2, high=0.6),
            rg.uniform(low=0.2, high=0.6)
        )

# auxiliary parameters initialisation
for n in net.nodes:
    net.nodes[n]['result_list'] = []


# ----------------------------------------------------------


#
def simulate_dialog(alice, bob):
    global net
    # get dialogue matrix of the current dialogue and
    # the preference densities of its participants
    D = net.edges[alice, bob]['D']
    wA = net.nodes[alice]['w']
    wB = net.nodes[bob]['w']
    wA_result = np.zeros(net.nvars)
    wB_result = np.zeros(net.nvars)
    for v in range(net.nvars):
        wA_result[v] = D[0, 0] * wA[v] + D[0, 1] * wB[v]
        wB_result[v] = D[1, 0] * wA[v] + D[1, 1] * wB[v]
    return wA_result, wB_result


def simulate_dialog_alt(D, wA, wB):
    global net
    # get dialogue matrix of the current dialogue and
    # the preference densities of its participants
    wA_result = np.zeros(net.nvars)
    wB_result = np.zeros(net.nvars)
    for v in range(net.nvars):
        wA_result[v] = D[0, 0] * wA[v] + D[0, 1] * wB[v]
        wB_result[v] = D[1, 0] * wA[v] + D[1, 1] * wB[v]
    return wA_result, wB_result


#
def simulate_session():
    global net
    start_time = time.time()
    # clean auxiliary information
    for node in net.nodes:
        net.nodes[node]['result_list'][:] = []
    # for channel in net.edges:
    #     for ic in channel:
    #         net.nodes[ic]['result_list'][:] = []
    clean_time = time.time()
    # simulate session dialogues
    for channel in net.edges:
        channel_obj = net.edges[channel]
        if not bernoulli_trial(channel_obj['a']):
            # channel is not active
            continue
        else:  # channel active
            pass
        # determine actors participating as Alice and Bob in the
        # current dialogue
        alice, bob = min(channel), max(channel)
        # ------------------------------------------------------
        alice_node = net.nodes[alice]
        bob_node = net.nodes[bob]
        # wA, wB = simulate_dialog(alice, bob)
        wA, wB = simulate_dialog_alt(channel_obj['D'], alice_node['w'], bob_node['w'])
        alice_node['result_list'].append(wA)
        bob_node['result_list'].append(wB)
    dialog_time = time.time()
    # compute the previous session result for each community actor
    for n in net:
        if net.nodes[n]['result_list']:
            # actor 'n' participates at least in one dealogue
            ndialogues = len(net.nodes[n]['result_list'])
            w = np.zeros(net.nvars)
            for wc in net.nodes[n]['result_list']:
                np.add(w, wc, w)
            np.multiply(w, 1.0 / ndialogues,
                        net.nodes[n]['w'])
    compute_time = time.time()
    print(
        f"Clean: {clean_time - start_time}ms, Dialog: {dialog_time - clean_time}, Compute: {compute_time - dialog_time}")


#
def observation():
    # polling simulation
    for n in net:
        hn = h(net.nodes[n]['w'])
        if bernoulli_trial(
                np.power(hn, net.nodes[n]['rho'])):
            # actor 'n' disclaims a choice
            net.nodes[n]['choice'] = DISCLAIMER
        else:
            # actor 'n' chooses
            net.nodes[n]['choice'] = np.random.choice(
                net.nvars, p=net.nodes[n]['w'])
    # compute average preference density
    W = np.zeros(net.nvars)
    for n in net:
        np.add(W, net.nodes[n]['w'], W)
    np.multiply(W, 1.0 / net.number_of_nodes(), W)
    # compute polling result
    DP = len([1 for n in net
              if net.nodes[n]['choice'] == DISCLAIMER])
    if DP == net.number_of_nodes():
        # all community actors disclaimed a choice
        return W, 1.0, uncertainty(net.nvars)
    NP = net.number_of_nodes() - DP
    WP = net.nvars * [None]
    for v in range(net.nvars):
        WP[v] = len([1 for n in net
                     if net.nodes[n]['choice'] == v])
        WP[v] /= NP
    DP /= net.number_of_nodes()
    return W, DP, WP


# ----------------------------------------------------------
# experiment specification
# ----------------------------------------------------------
print("Specifying the experiment...")
# specify initial prefernce densities of community actors
for n in net:
    if n == 0:
        net.nodes[n]['w'] = np.array([1.0, 0.0], float)
    elif n == 1:
        net.nodes[n]['w'] = np.array([0.0, 1.0], float)
    else:
        net.nodes[n]['w'] = uncertainty(net.nvars)

niter = 100  # define number of iterations

# set up the experiment

protocol = [observation()]
start_time_total = time.time()
print("Running experiments, iterations count: ", niter)
for istep in range(niter):
    if istep % 100 == 0:
        print("Done iterations: ", istep)
    start_time = time.time()
    simulate_session()
    session_time = time.time()
    protocol.append(observation())
    observation_time = time.time()
    print(f"Session: {session_time - start_time}s, Observation: {observation_time - session_time}s")
running_time = time.time()

# ----------------------------------------------------------
# store the experiment outcomes
# ----------------------------------------------------------
print("Storing the experiment results...")
out_file = open("protocol_reference.dat", "w")
# out_file.write(str(net.nvars) + "\n")
for item in protocol:
    for val in item[0]:
        out_file.write(str(val) + " ")
    out_file.write(str(item[1]))
    for val in item[2]:
        out_file.write(" " + str(val))
    out_file.write("\n")
out_file.close()

print(f"Running time: {running_time - start_time_total}ms")
