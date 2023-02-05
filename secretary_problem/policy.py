
# @date: 2022/05/28

import numpy as np
import pandas as pd
from tqdm import tqdm


def fluid_bayes(val, prob, time, inv_num, sample, delay):
    """
    Fluid Bayes Selector
    :param val: valuation
    :param prob: distribution
    :param time: current time period, time_num-1, ..., 0
    :param inv_num: current inventory
    :param sample: current sample
    :param delay: number of delays
    :return: current decision
    """

    # CDF
    cdf_prob = []
    for i in range(len(prob)):
        cdf_prob.append(sum(prob[0:i+1]))

    current_val = sample[time]
    current_j = val.index(current_val)
    indicate1 = [val > current_val for val in sample[time-delay:time+1]]
    indicate2 = [val == current_val for val in sample[time-delay:time+1]]
    indicate = (1 - cdf_prob[current_j] + prob[current_j]/2) * (time - delay - 1) + sum(indicate1) + sum(indicate2)/2
    # print(indicate)
    if inv_num >= indicate:
        # 1 = accept, 0 = reject
        decision = 1
    else:
        decision = 0
    return decision


def offline(val, inv_num, sample):
    """
    Offline Policy (Hindsight Benchmark)
    :return: total valuation by offline policy
    """
    total_val = 0
    hind_demand = [0] * len(val)
    for s in sample:
        hind_demand[val.index(s)] += 1

    for index in range(len(val)-1, -1, -1):
        if hind_demand[index] <= inv_num:
            total_val += hind_demand[index] * val[index]
            inv_num -= hind_demand[index]
        else:
            total_val += inv_num * val[index]
            inv_num = 0
    return total_val


def online(val, prob, time_num, inv_num, sample, delay):
    """
    Online Policy with Delay
    :param val: valuation
    :param prob: distribution
    :param time_num: number of time periods
    :param inv_num: number of inventory
    :param sample: a certain sample path
    :param delay: number of delays
    :return: total valuation by online policy
    """
    total_val = 0
    # one-by-one decision for t = time_num-1, ..., delay+1
    for t in range(time_num-1, delay, -1):
        decision = fluid_bayes(val, prob, t, inv_num, sample, delay)
        # print(t, decision)
        # decision = {0, 1}: 1 = accept, 0 = reject
        total_val += sample[t] * decision
        inv_num -= decision

    # last (delay+1)-period decision for t = delay, ..., 0
    total_val += offline(val, inv_num, sample[0:delay+1])
    return total_val


def batch(val, prob, time_num, inv_num, sample, delay):
    """
    K-Batching
    """
    total_val = 0
    # one-by-one decision for t = time_num-1, ..., delay+1
    for t in range(time_num - 1, delay, -1):
        if delay == -1:
            current_delay = -1
        else:
            current_delay = delay - (time_num - t) % (delay + 1)
        decision = fluid_bayes(val, prob, t, inv_num, sample, current_delay)
        # print(t, decision)
        # decision = {0, 1}: 1 = accept, 0 = reject
        total_val += sample[t] * decision
        inv_num -= decision

    # last (delay+1)-period decision for t = delay, ..., 0
    total_val += offline(val, inv_num, sample[0:delay + 1])
    return total_val


def unknown(val, time_num, inv_num, sample, delay):
    """
    Unknown Distributions --- Sample Average + Delay
    """
    total_val = 0
    # one-by-one decision for t = time_num-1, ..., delay+1
    for t in range(time_num-1, delay, -1):
        realized_demand = [0] * len(val)
        if delay == -1:
            for s in sample[t - (delay + 1): time_num-1]:
                realized_demand[val.index(s)] += 1
            prob = [r / (time_num - 1 - (t - (delay + 1)) + 1) for r in realized_demand]
        else:
            for s in sample[t - delay: time_num-1]:
                realized_demand[val.index(s)] += 1
            prob = [r / (time_num - 1 - (t - delay) + 1) for r in realized_demand]
        decision = fluid_bayes(val, prob, t, inv_num, sample, delay)
        # print(t, decision)
        # decision = {0, 1}: 1 = accept, 0 = reject
        total_val += sample[t] * decision
        inv_num -= decision

    # last (delay+1)-period decision for t = delay, ..., 0
    total_val += offline(val, inv_num, sample[0:delay+1])
    return total_val


if __name__ == '__main__':
    # valuation from smallest to largest
    Val = [10, 100]
    Prob = [0.01, 0.99]
    Time_num = 10
    Inv_num = 1
    delay_num = 0

    temp_sample = np.random.choice(len(Val), p=Prob, size=Time_num)
    sample_path = []
    for index in temp_sample:
        sample_path.append(Val[index])
    print(sample_path)
    on_result = online(Val, Prob, Time_num, Inv_num, sample_path, 0)

    # off_result = offline(val, inv_num, sample_path)
    # print("off:", off_result)
    # on_result = online(val, prob, time_num, inv_num, sample_path, 0)

