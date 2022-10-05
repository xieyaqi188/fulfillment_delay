# @author: Yaqi Xie
# @email: xieyq188@gmail.com
# @date: 2022/05/28

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from policy import online, offline


# secretary problem test
if __name__ == '__main__':
    """
    :param val: valuations from smallest to largest 
    :param prob: probability distribution corresponding to val
    :param time_num: number of time periods/candidates
    :param inv_num: number of inventory
    :param delay_num: maximum number of delay
    """

    # val = [i for i in np.linspace(1, 100, 100)]
    # prob = [0.01] * 100
    # val = [50, 60, 70, 80]
    # prob = [0.25, 0.25, 0.25, 0.25]
    val = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # prob = [0, 0.3, 0.6, 0.1]
    time_num = 100
    # B
    inv_num = 75
    delay_num = 10
    delay_list = [d - 1 for d in range(delay_num + 2)]

    test_number = 100
    total_test_offline = 0
    total_test_online = [0] * (delay_num + 2)
    prob_num = 100
    for n in tqdm(range(prob_num)):
        p = np.random.exponential(scale=1, size=10)
        prob = [pp / sum(p) for pp in p]
        # test delay = 0, ..., delay_num
        for i in range(test_number):
            # generate samples
            temp_sample = np.random.choice(len(val), p=prob, size=time_num)
            sample_path = []
            for index in temp_sample:
                sample_path.append(val[index])
            # run algorithm
            off_result = offline(val, inv_num, sample_path)
            total_test_offline += off_result
            for K in delay_list:
                on_result = online(val, prob, time_num, inv_num, sample_path, K)
                total_test_online[delay_list.index(K)] += on_result / off_result

    # averaged results (expected results)
    test_offline = total_test_offline / test_number / prob_num
    test_online = [index / test_number / prob_num for index in total_test_online]
    regret_delay = [test_offline - on for on in test_online]
    ratio = [on / test_offline for on in test_online]
    print(test_offline)
    print(test_online)
    print(regret_delay)
    print(ratio)
    output = {"off": test_offline, "on_delay": test_online, "delay_num": delay_num}
    np.save('./result_secretary/setting75.npy', output)
    # regret_plot(val, prob, inv_num, delay_num, regret_delay)



