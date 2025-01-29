import numpy as np
np.set_printoptions(linewidth=2000, precision=3, suppress=True, formatter={'float': '{: 0.3f}'.format})

def locate(from_state, to_state):
    # find a cell in the transition matrix that corresponds to the transition from from_state to to_state
    return (from_state[0] - 1) * 3 + from_state[1] - 1, (to_state[0] - 1) * 3 + to_state[1] - 1

def print_transition_matrix(matrix):
    print("\t| (1,1)\t| (1,2)\t| (1,3)\t| (2,1)\t| (2,2)\t| (2,3)\t| (3,1)\t| (3,2)\t| (3,3)")
    for i in range(9):
        print('---------------------------------------------------------------------------------')
        a = i // 3 + 1
        b = i % 3 + 1
        print(f'({a},{b})', '\t|', '\t| '.join(f'{x:.3f}'.rstrip('0').rstrip('.').rjust(4) for x in matrix[i]))
