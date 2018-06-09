from __future__ import division
import numpy as np
import os

N_NODES = 10
N_QUEUE = 5
 
def compute_states():
    # Generates the Markov Chain
    states = [] # [nodes trasmitting, nodes holding, collision status]

    for i in range(0, N_NODES+1):
        if i == 0:
            # first line of MC transition states
            states.append([0, 0, True])
        else:
            status = True if i == 1 else False
            # all states where one node is transmitting, either colliding or successfully
            for j in range(0, N_NODES*N_QUEUE+1):
                states.append([i, j, status])

    return states

def find_state(state, states):
    # Return the position of a state
    if state in states:
        return states.index(state)
    else:
        return -1

def compute_send(item, rate):
    # average inter arrival time of the network
    return rate * N_NODES

def compute_end_transmission(item, rate):
    # No. of transmitting nodes multiplied by mu
    # 6.026 byte with speed 1MB/s
    return 166.667

def compute_matrix(states, rate):
    # infinitesimal generator
    matrix = np.zeros((len(states), len(states)))

    for index, item in enumerate(states):
        if item == [0, 0, True]:
            # first state
            matrix[0][1] = compute_send(item, rate)
        else:
            # other states

            # START OF TRANSMISSION
            next_state = [item[0], item[1] + 1, item[2]]
            position = find_state(next_state, states)
            if position != -1:
                matrix[index][position] = compute_send(item, rate)

            # END OF TRANSMISSION
            status = True if item[1] <= 1 else False
            if(item[1] <= N_NODES):
                next_state = [item[1], 0, status]
            else:
                status = True if N_NODES == 1 else False
                next_state = [N_NODES, item[1]-N_NODES, status]
            position = find_state(next_state, states)
            if position != -1:
                matrix[index][position] = compute_end_transmission(item, rate)

    # fill the diagonal
    for x in range(0, len(matrix)):
        matrix[x][x] = -sum(matrix[x])
    return matrix

def append_results(l, steady_state):
    # save results in csv
    output = 'model.csv'
    with open(output, 'a') as f:
        for index, p in enumerate(steady_state):
            if(index != 0):
                state = states[index]
                status = 't' if state[2] else 'c'
                if p < 0:
                    p = 0
                transmitting = state[0]
                holding = state[1]
                f.write('{},{},{},{},{}\n'.format(transmitting, holding, status, p, l)) 

if __name__ == "__main__":

    output = 'model.csv'
    f = open(output, 'w+')
    f.write('transmitting,holding,state,prob,rate\n')
    f.close()

    states = compute_states()
    N = len(states)

    rates = [333.33, 250, 200, 175, 150, 125, 100, 75, 50, 45, 40, 38, 35, 32.5, 30, 27.5, 25, 23.5, 22, 19, 17, 15, 13, 12, 11, 10, 9, 8, 7, 6, 5, 2, 1, 0.5, 0.01]
    #rates = [166.66]
    for i, rate in enumerate(rates):
        
        transition_matrix = compute_matrix(states, rate)
        Q = np.ones((N, N + 1))
        Q[:,:-1] = transition_matrix

        b = [0] * N
        b.append(1)
        # compute the steady state
        # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.lstsq.html
        steady_state_matrix = np.linalg.lstsq(Q.transpose(), b, rcond=-1)
        append_results(rate, steady_state_matrix[0])

        perc_done = int((i+1)/len(rates)*100)
        print("> ", perc_done , "% \t >", rate)

print('Finish. Use \'make analysis\' to analyze the model')