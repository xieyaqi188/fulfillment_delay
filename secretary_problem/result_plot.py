# @author: Yaqi Xie
# @email: xieyq188@gmail.com
# @date: 2022/08/17

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as op


def data(instance):
    # output = {"off": test_offline, "on_delay": test_online, "delay_num": delay_num}
    instance = instance.item()
    offline = instance['off']
    online = instance['on_delay']
    delay_num = instance['delay_num']
    regret_delay = [1 - on for on in online]
    ratio = online
    return regret_delay, ratio, delay_num


if __name__ == '__main__':
    instance1 = np.load('./result_secretary/setting25.npy', allow_pickle=True)
    regret1 = data(instance1)[0]
    ratio1 = data(instance1)[1]
    delay_num = data(instance1)[2]

    instance2 = np.load('./result_secretary/setting50.npy', allow_pickle=True)
    regret2 = data(instance2)[0]
    ratio2 = data(instance2)[1]

    instance3 = np.load('./result_secretary/setting75.npy', allow_pickle=True)
    regret3 = data(instance3)[0]
    ratio3 = data(instance3)[1]
    #
    # instance4 = np.load('./result_secretary/setting4.npy', allow_pickle=True)
    # regret4 = data(instance4)[0]
    # ratio4 = data(instance4)[1]

    delay_list = [K - 1 for K in range(delay_num + 2)]

    plt.title("Regret Ratios for Multisecretary Problem")
    plt.xticks(delay_list)
    plt.xlabel("Amount of Delay K")
    plt.ylabel("Regret Ratio")
    plt.plot(delay_list, regret1, marker='o', markersize=2, label='B = 25')
    plt.plot(delay_list, regret2, marker='o', markersize=2, label='B = 50')
    plt.plot(delay_list, regret3, marker='o', markersize=2, label='B = 75')
    # plt.plot(delay_list, regret4, marker='o', markersize=2, label='Instance 4')
    plt.legend(prop={"size": 12})
    plt.savefig('ratio_secretary.png')
    plt.show()

    # plt.title("Ratio for Multisecretary Problem")
    # plt.xticks(range(0, len(delay_list), 2))
    # plt.xlabel("Number of Delay K")
    # plt.ylabel("Ratio")
    # plt.plot(delay_list, ratio1, marker='o', markersize=2, label='Instance 1')
    # plt.plot(delay_list, ratio2, marker='o', markersize=2, label='Instance 2')
    # plt.plot(delay_list, ratio3, marker='o', markersize=2, label='Instance 3')
    # plt.plot(delay_list, ratio4, marker='o', markersize=2, label='Instance 4')
    # plt.legend(prop={"size": 12})
    # plt.savefig('ratio_secretary.png')
    # plt.show()
