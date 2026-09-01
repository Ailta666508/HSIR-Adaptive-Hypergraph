import numpy as np
import matplotlib.pyplot as plt
import collections
import seaborn as sns
import argparse
import os

np.random.seed(42)

def load_hypergraph(file_path):
    hyperedges = []
    nodes = set()
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                edge = [n.strip() for n in line.split(',')]
                hyperedges.append(edge)
                nodes.update(edge)
    
    node_to_he = collections.defaultdict(list)
    for idx, he in enumerate(hyperedges):
        for node in he:
            node_to_he[node].append(idx)
            
    return list(nodes), hyperedges, node_to_he


def parse_args():
    parser = argparse.ArgumentParser(description="Hypergraph SIR Spreading Simulation")
    
    # 参数一：数据集
    parser.add_argument('--data', type=str, default='contact-high-school', help="模拟过程用到的超边数据集")

    return parser.parse_args()


def main():
    args = parse_args()

    # 加载超图数据
    all_nodes, hyperedges, node_to_he = load_hypergraph(f'data/{args.data}/hyperedges-{args.data}.txt')

    # 速率系数
    beta = 0.03     # 易感者感染速率系数
    mu = 0.1       # 感染者康复速率系数
    delta = 0.1     # 感染者脱离超边速率系数
    eta = 0.3       # 超边熔断速率系数

    # 其他参数
    gamma = 1.5     # 感染协同效应指数
    alpha = 0.5     # 风险权重因子
    phi = 0.4       # 风险逃离阈值

    # 实验参数
    T = 100         # 模拟时间步长
    num_runs = 100   # 模拟运行次数

    N = len(all_nodes) # 节点数量

    # 初始感染节点种子选择：选择度数最大的节点
    degrees = {node: len(node_to_he[node]) for node in all_nodes}
    seed = max(degrees, key=degrees.get)

    total_S = np.zeros(T + 1)
    total_I = np.zeros(T + 1)
    total_R = np.zeros(T + 1)
    for run in range(num_runs):

        # 初始化节点状态和超边连接关系
        current_status = {node: 'S' for node in all_nodes}
        current_status[seed] = 'I'
        current_node_to_he = node_to_he.copy()
        current_h = hyperedges[:]

        current_s = set(all_nodes)
        current_s.remove(seed)
        current_i = {seed}
        current_r = set()

        # 记录每个时间步的各状态节点数量
        S_t = []
        I_t = []
        R_t = []

        for t in range(T):
            # 记录当前时间步的感染节点数量
            S_t.append(len(current_s))
            I_t.append(len(current_i))
            R_t.append(len(current_r))
            if len(current_i) == 0:
                break
            
            # 记录新的节点状态和超边连接关系
            new_status = current_status.copy()
            new_h = [he[:] for he in current_h]

            # 计算当前时刻超边内部感染者数量以及超边风险值信息
            hi = [0] * len(hyperedges)
            for node in current_i:
                for he_idx in current_node_to_he[node]:
                    hi[he_idx] += 1

            Rh_global = len(current_i) / N
            Rh_local = [0] * len(hyperedges)
            for he_idx in range(len(hyperedges)):
                Rh_local[he_idx] = hi[he_idx] / len(current_h[he_idx]) if len(current_h[he_idx]) > 0 else -1
            Rh = [0] * len(hyperedges)
            for he_idx in range(len(hyperedges)):
                Rh[he_idx] = (1 - alpha) * Rh_local[he_idx] + alpha * Rh_global

            # 遍历更新节点状态信息和超边连接关系
            for node in all_nodes:
                if current_status[node] == 'S':
                    for he_idx in current_node_to_he[node]:
                        # 动力学事件 1: 易感者感染
                        if np.random.rand() < beta * hi[he_idx]**gamma:
                            new_status[node] = 'I'
                            
                        # 动力学事件 3: 易感者脱离超边
                        if np.random.rand() < delta * Rh[he_idx] and node in new_h[he_idx]:
                            new_h[he_idx].remove(node)

                # 动力学事件 2: 感染者康复
                if current_status[node] == 'I':
                    if np.random.rand() < mu:
                        new_status[node] = 'R'

            for he_idx in range(len(hyperedges)):
                # 动力学事件 4: 超边熔断
                if Rh[he_idx] > phi and np.random.rand() < eta:
                    new_h[he_idx] = []
                    
            # 更新节点状态和超边连接关系
            current_status = new_status
            current_node_to_he = collections.defaultdict(list)
            for idx, he in enumerate(new_h):
                for node in he:
                    current_node_to_he[node].append(idx)
            current_h = new_h

            current_s = {node for node in all_nodes if new_status[node] == 'S'}
            current_i = {node for node in all_nodes if new_status[node] == 'I'}
            current_r = {node for node in all_nodes if new_status[node] == 'R'}

        # 记录每个时间步的感染节点数量
        while len(I_t) < T + 1:
            S_t.append(len(current_s))
            I_t.append(len(current_i))
            R_t.append(len(current_r))

        total_S += np.array(S_t) / N
        total_I += np.array(I_t) / N
        total_R += np.array(R_t) / N

    avg_S = total_S / num_runs
    avg_I = total_I / num_runs
    avg_R = total_R / num_runs

    # 绘图
    time_steps = np.arange(T + 1)

    plt.figure(figsize=(8, 5))
    plt.plot(time_steps, avg_S, label='Susceptible (S)', color='blue')
    plt.plot(time_steps, avg_I, label='Infected (I)',     color='gray', linestyle='--')
    plt.plot(time_steps, avg_R, label='Recovered (R)',    color='green')

    plt.xlabel('Time step', fontsize=12)
    plt.ylabel('Fraction of nodes', fontsize=12)
    plt.legend()
    plt.tight_layout()
    os.makedirs(f'figure/{args.data}', exist_ok=True)
    plt.savefig(f'figure/{args.data}/HSIR.jpg', dpi=300)
    plt.show()

    # 输出最终平均结果
    print(f"Total nodes: {N}")
    print(f"Average final susceptible fraction (S): {avg_S[-1]:.4f}")
    print(f"Average final infected fraction (I): {avg_I[-1]:.4f}")
    print(f"Average final recovered fraction (R): {avg_R[-1]:.4f}")


if __name__ == "__main__":
    main()