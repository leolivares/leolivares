import queue
import sys


def get_connected(start, visited, rivals, connected):
    q = queue.Queue()
    q.put_nowait(start)
    connections = []
    visited[start] = True
    while not q.empty():
        current = q.get_nowait()
        connections.append(current)
        for next in rivals[current]:
            if not visited[next]:
                q.put_nowait(next)
                visited[next] = True
    connected.append(connections)
    return connected, visited


def cal_gain(connected, D, price):
    cost = [0 for _ in range(len(connected))]
    gainD = [0 for _ in range(len(connected))]
    gainP = [0 for _ in range(len(connected))]
    for i in range(len(connected)):
        for j in range(len(connected[i])):
            polit = connected[i][j]
            cost[i] += price[polit]
            if polit <= D:
                gainD[i] -= 1
                gainP[i] += 1
            else:
                gainD[i] += 1
                gainP[i] -= 1

    return cost, gainD, gainP


def cal_delta(connected, cost, gainD, gainP, B):
    delta_all_D = [0 for _ in range(B + 1)]
    delta_all_P = [0 for _ in range(B + 1)]
    for i in range(len(connected)):
        for j in range(B, 0, -1):
            if cost[i] <= j:
                delta_all_D[j] = max(delta_all_D[j], delta_all_D[j-cost[i]] + gainD[i])
                delta_all_P[j] = max(delta_all_P[j],
                                     delta_all_P[j - cost[i]] + gainP[i])
    return delta_all_D[B], delta_all_P[B]


if __name__ == '__main__':
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        next_line = list(map(int, line.strip().split(" ")))
        while len(next_line) == 4:
            D, P, R, B = next_line
            priceD = list(map(int, sys.stdin.readline().strip().split(" ")))
            priceP = list(map(int, sys.stdin.readline().strip().split(" ")))
            price = [0] + priceD + priceP
            rivals = [[] for x in range(D+P+1)]
            visited = [False for x in range(D+P+1)]
            connected = []
            for i in range(R):
                u1, u2 = sys.stdin.readline().strip().split(" ")
                u1, u2 = int(u1), int(u2) + D
                rivals[u1].append(u2)
                rivals[u2].append(u1)

            for i in range(1, D+P+1):
                if visited[i] != True:
                    connected, visited = get_connected(i, visited, rivals, connected)

            cost, gainD, gainP = cal_gain(connected, D, price)
            D_t, P_t = cal_delta(connected, cost, gainD, gainP, B)
            break

        print(D_t + D, P_t + P)

