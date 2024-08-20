
# @date: 2022/08/18

import numpy as np
import matplotlib.pyplot as plt
import os


if __name__ == '__main__':
    results = os.listdir('./new_result')
    delay_list = [0, 30, 60, 90, 120, 180, 240]
    n = 0
    rt = [0] * (len(delay_list))
    batch_rt = [0] * (len(delay_list))
    for i in results:
        print(i)
        n += 1
        tmp = os.path.join('./new_result/'+i)
        instance = np.load(tmp, allow_pickle=True)
        # {"FDC": fdc, "RDC": rdc, "off_IP": test_ip, "off_LP": test_lp, "on_delay": on_delay, "on_batch": on_batch,
        #               "delay": delay}
        instance = instance.item()
        # fdc = instance['FDC']
        # rdc = instance['RDC']
        offline = instance['off_LP']
        online = instance['on_delay']
        batch = instance['on_batch']
        # regret_delay = [offline - on for on in online]
        ratio = [on / offline for on in online]
        batch_ratio = [on / offline for on in batch]
        rt = [x + y for x, y in zip(rt, ratio)]
        batch_rt = [x + y for x, y in zip(batch_rt, batch_ratio)]

    rt = [1 - r / n for r in rt]
    batch_rt = [1 - r / n for r in batch_rt]
    print('The number of samples:', n)
    print('delay', rt)
    print('batch', batch_rt)

    # plt.title("Regret for Order Fulfillment Problem")
    # plt.xticks(delay_list)
    # plt.xlabel("Delay Period (min)")
    # plt.ylabel("Regret")
    # plt.plot(delay_list, regret_delay, marker='o', markersize=2,
    #          label='FDC {FDC} and RDC {RDC}'.format(FDC=fdc, RDC=rdc))
    # plt.legend(prop={"size": 12})
    # plt.savefig('regret_fdc.png')
    # plt.show()

    plt.title("Regret Ratios for Order Fulfillment Problem")
    plt.xticks(delay_list)
    plt.xlabel("Length of Delay (min)")
    plt.ylabel("Regret Ratio")
    # plt.plot(delay_list, ratio, marker='o', markersize=2, label='FDC {FDC} and RDC {RDC}'.format(FDC=fdc, RDC=rdc))
    plt.plot(delay_list, rt, marker='o', markersize=2, label='Delay')
    plt.plot(delay_list, batch_rt, marker='o', markersize=2, label='Batching')
    plt.legend(prop={"size": 12})
    plt.savefig('ratio_fdc.png')
    plt.show()
