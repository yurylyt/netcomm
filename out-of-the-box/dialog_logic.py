import numpy as np

def make_joint_preference(alice, bob):
    dialog_matrix = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            dialog_matrix[i, j] = alice[i] * bob[j]

    return dialog_matrix

def communicate(alice, bob, transition, iterations=1):
    alice_results = []
    bob_results = []
    # convert to floats
    alice = np.array(alice).astype(float)
    bob = np.array(bob).astype(float)

    alice_results.append(alice)
    bob_results.append(bob)
    # print("Initial joint preference")
    # print(make_joint_preference(alice, bob))

    for i in range(iterations):
        dialog_matrix = make_joint_preference(alice, bob)

        result = np.dot(dialog_matrix.flatten(), transition).reshape(3,3)
        # print("\nResult")
        # print(result)

        # marginalize result to get Alice's opinion
        alice = np.zeros(3)
        # Sum all rows in the result
        for i in range(3):
            alice[i] = result[i].sum()

        # print("\nAlice's opinion")
        # print(alice, "->", alice_result)

        # marginalize result to get Bob's opinion
        bob = np.zeros(3)
        # Sum all columns in the result
        for i in range(3):
            bob[i] = result[:, i].sum()

        # print("\nBob's opinion")
        # print(bob, "->", bob_result)
        alice_results.append(alice)
        bob_results.append(bob)
        # return alice_result, bob_result
    plot_side_by_side(alice_results, bob_results)
    # print("\nAlice")
    # print('\n'.join(str(x) for x in alice_results))
    # plot_results(alice_results)

    # print("\nBob")
    # print('\n'.join(str(x) for x in bob_results))
    # plot_results(bob_results)


def _plot_results(results, plt):
    from matplotlib.ticker import MaxNLocator
    cumsum = np.cumsum(results, axis=1)


    x = np.arange(cumsum.shape[0])
    # plt.plot(cumsum)
    for i in range(3):
        baseline = 0 if i == 0 else cumsum[:, i-1]
        plt.fill_between(x, baseline, cumsum[:, i], label=f'Option {i+1}', alpha=0.5)

    # plt.xticks(ticks=x, labels=[f'{i}' for i in x])
    plt.set_xticks(ticks=x, labels=[f'{i}' for i in x])

    plt.legend()
    plt.set_ylim(bottom=0)
    # plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.yaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.grid()

def plot_results(results):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    _plot_results(results, plt)

    plt.show()

def plot_side_by_side(results_a, results_b):
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    ax1.set_title("Alice")
    ax2.set_title("Bob")

    _plot_results(results_a, ax1)
    _plot_results(results_b, ax2)
    plt.show()
