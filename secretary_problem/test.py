
# @date: 2022/05/28

import numpy as np
from tqdm import tqdm

from policy import online, offline, batch, unknown


# secretary problem test
if __name__ == '__main__':
    """
    :param val: valuations from smallest to largest 
    :param prob: probability distribution corresponding to val
    :param time_num: number of time periods/candidates
    :param inv_num: number of inventory
    :param delay_num: maximum number of delay
    """
    # flag = "delay", "batch", "unknown"
    flag = "batch"

    # val = [i for i in np.linspace(1, 100, 100)]
    # prob = [0.01] * 100
    # val = [50, 60, 70, 80]
    # prob = [0.25, 0.25, 0.25, 0.25]
    val = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # prob = [0, 0.3, 0.6, 0.1]
    time_num = 100
    # B
    inv_num = 25
    delay_num = 20
    delay_list = [d - 1 for d in range(delay_num + 2)]

    test_number = 100
    total_ratio_online = [0] * len(delay_list)
    total_ratio_regret = [0] * len(delay_list)
    rho = [0] * (len(delay_list) - 1)
    prob_num = 100
    for n in tqdm(range(prob_num)):
        p = np.random.exponential(scale=1, size=len(val))
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
            # total_offline += off_result
            copy_on = 1
            for K in delay_list:
                if flag == "delay":
                    on_result = online(val, prob, time_num, inv_num, sample_path, K)
                    total_ratio_online[delay_list.index(K)] += on_result / off_result
                    if delay_list.index(K) >= 1:
                        if off_result - copy_on > 0:
                            rho[delay_list.index(K) - 1] += on_result / copy_on
                    copy_on = on_result
                    # averaged results (expected results)
                    ratio_online = [index / test_number / prob_num for index in total_ratio_online]
                    rho_on = [index / test_number / prob_num for index in rho]
                    print("Ratio of Online Reward", ratio_online)
                    print("Rho", rho_on)
                    output = {"on_delay": ratio_online, "delay_list": delay_list}
                    np.save('./result_secretary/setting%d%s.npy' % (inv_num, flag), output)
                elif flag == "batch":
                    # delay
                    on_regret = online(val, prob, time_num, inv_num, sample_path, K)
                    total_ratio_regret[delay_list.index(K)] += on_regret / off_result
                    # batch
                    on_result = batch(val, prob, time_num, inv_num, sample_path, K)
                    total_ratio_online[delay_list.index(K)] += on_result / off_result
                    #
                    regret_online = [index / test_number / prob_num for index in total_ratio_regret]
                    ratio_online = [index / test_number / prob_num for index in total_ratio_online]
                    output = {"on_delay": regret_online, "delay_list": delay_list, "on_batch": ratio_online}
                    # np.save('./result_secretary/setting%d%s.npy' % (inv_num, flag), output)
                    np.save('./result_secretary/setting%d%s%d.npy' % (inv_num, flag, time_num), output)
                elif flag == "unknown":
                    # delay
                    on_regret = online(val, prob, time_num, inv_num, sample_path, K)
                    total_ratio_regret[delay_list.index(K)] += on_regret / off_result
                    # unknown
                    on_result = unknown(val, time_num, inv_num, sample_path, K)
                    total_ratio_online[delay_list.index(K)] += on_result / off_result
                    if delay_list.index(K) >= 1:
                        rho[delay_list.index(K) - 1] += on_result / copy_on
                    copy_on = on_result
                    # averaged results (expected results)
                    #
                    regret_online = [index / test_number / prob_num for index in total_ratio_regret]
                    ratio_online = [index / test_number / prob_num for index in total_ratio_online]
                    output = {"on_delay": regret_online, "delay_list": delay_list, "on_unknown": ratio_online}
                    np.save('./result_secretary/setting%d%s.npy' % (inv_num, flag), output)



