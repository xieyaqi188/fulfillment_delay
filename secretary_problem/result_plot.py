
# @date: 2022/08/17

import numpy as np
import matplotlib.pyplot as plt
import math


def data(instance):
    # output = {"on_delay": ratio_online, "delay_list": delay_list}
    instance = instance.item()
    online_ratio = instance['on_delay']
    delay_list = instance['delay_list']
    print(delay_list)

    regret_ratio = [1 - on for on in online_ratio]
    diff = [0] * (len(delay_list) - 1)
    rho = [0] * len(delay_list)
    for K in range(len(delay_list) - 1):
        diff[K] = regret_ratio[K] - regret_ratio[K + 1]
        rho[K] = regret_ratio[K + 1] / regret_ratio[K]
        print(K, regret_ratio[K])
    print("Ratio", regret_ratio)
    print("Difference", diff)
    print("Rho", rho)
    return regret_ratio, delay_list, diff, rho


if __name__ == '__main__':
    # inv_num = 25, 50, 75
    # flag = "delay", "batch", "unknown"
    inv_num = 75
    flag = "unknown"

    if flag == "delay":
        instance1 = np.load('./result_secretary/setting25delay.npy', allow_pickle=True)
        regret1 = data(instance1)[0]
        delay_list = data(instance1)[1]

        instance2 = np.load('./result_secretary/setting50delay.npy', allow_pickle=True)
        regret2 = data(instance2)[0]

        instance3 = np.load('./result_secretary/setting75delay.npy', allow_pickle=True)
        regret3 = data(instance3)[0]

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
    elif flag == "batch":
        # output = {"on_delay": regret_online, "delay_list": delay_list, "on_batch": ratio_online}
        eg2 = np.load('./result_secretary/setting%d%s.npy' % (inv_num, flag), allow_pickle=True)
        instance = eg2.item()
        online_ratio2 = instance['on_delay']
        regret_ratio2 = [1 - on for on in online_ratio2]
        delay_list2 = instance['delay_list']
        online_batch2 = instance['on_batch']
        batch_ratio2 = [1 - on for on in online_batch2]

        plt.title("Regret Ratio for Multisecretary Problem with Delay and Batching")
        delay_list = delay_list2[1: len(delay_list2)]
        plt.xticks(delay_list)
        plt.tick_params(labelsize=7)
        plt.xlabel("Amount of Delay K")
        plt.ylabel("Regret Ratio")
        plt.plot(delay_list, regret_ratio2[1: len(delay_list)+1], marker='o', markersize=2, label='B = %d - Delay' % inv_num)
        plt.plot(delay_list, batch_ratio2[1: len(delay_list)+1], marker='o', markersize=2, label='B = %d - Batching'%inv_num)
        plt.legend(prop={"size": 12})
        plt.savefig('ratio_secretary%d%s.png'% (inv_num, flag))
        plt.show()
    elif flag == "unknown":
        # output = {"on_delay": regret_online, "delay_list": delay_list, "on_unknown": ratio_online}
        eg3 = np.load('./result_secretary/setting%d%s.npy' % (inv_num, flag), allow_pickle=True)
        instance = eg3.item()
        online_ratio3 = instance['on_delay']
        regret_ratio3 = [1 - on for on in online_ratio3]
        delay_list3 = instance['delay_list']
        online_unknown3 = instance['on_unknown']
        unknown_ratio3 = [1 - on for on in online_unknown3]
        diff_regret = [0] * (len(delay_list3) - 1)
        diff_unknown = [0] * (len(delay_list3) - 1)
        rho = [0] * len(delay_list3)
        for K in range(len(delay_list3) - 1):
            diff_regret[K] = regret_ratio3[K] - regret_ratio3[K + 1]
            diff_unknown[K] = unknown_ratio3[K] - unknown_ratio3[K + 1]

        delay_list = delay_list3[2:len(delay_list3)]
        plt.title("Marginal Benefit (Decrease in Regret Ratio) for Multisecretary Problem")
        plt.xticks(delay_list)
        plt.xlabel("Amount of Delay K")
        plt.ylabel("Ratio")
        plt.plot(delay_list, diff_regret[1: len(delay_list) + 1], marker='o', markersize=2,
                 label='B = %d - Known' % inv_num)
        plt.plot(delay_list, diff_unknown[1: len(delay_list) + 1], marker='o', markersize=2,
                 label='B = %d - Unknown' % inv_num)
        plt.legend(prop={"size": 12})
        plt.savefig('ratio_secretary%d%s.png' % (inv_num, flag))
        plt.show()


