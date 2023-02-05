
# @date: 2022/07/21

import numpy as np
from tqdm import tqdm
from lp_policy import lp_relax, ip, bayes_selector, lp_relax_obj2, ip_obj2
import copy
import datetime


def offline(demand, inv_num, consume, flag, obj):
    """
    Offline Policy (Hindsight Benchmark)
    :return: hindsight optimum
    """
    if obj == 'order':
        if flag == 'LP':
            off_val = lp_relax(demand, inv_num, consume)[1]
        elif flag == 'IP':
            off_val = ip(demand, inv_num, consume)[1]
    elif obj == 'item':
        if flag == 'LP':
            off_val = lp_relax_obj2(demand, inv_num, consume)[1]
        elif flag == 'IP':
            off_val = ip_obj2(demand, inv_num, consume)[1]
    return off_val


def current_demand(new_data, prob, order_list, current_time, delta, delay_num, delay_period):
    """
    online demand
    :param new_data:
    :param prob:
    :param order_list: [0, 1, 2, ...] feasible order types
    :param current_time: the order time of current order
    :param delta:
    :param delay_num:
    :param delay_period:
    :return:
    """
    one_day = datetime.timedelta(days=1)
    delta_num = int(one_day / delta)

    demand = [0] * len(order_list)

    abs_time_list = new_data.index.tolist()
    end_time = current_time + delay_num * delay_period
    for t in abs_time_list:
        if current_time <= t <= end_time:
            temp_order = new_data.loc[t, 'order_type']
            if temp_order in order_list:
                demand[order_list.index(temp_order)] += 1

    current = datetime.timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
    current_delta_num = current // delta
    for i in range(len(order_list)):
        current_order = order_list[i]
        demand[i] += (1 - (current % delta) / delta) * prob[current_order][current_delta_num]
        for num in range(current_delta_num + 1, delta_num):
            demand[i] += prob[current_order][num]
    return demand


def online(new_data, prob, inv_num, consume, order_dict, order_list, delta, delay_num, delay_period, obj):
    """
    Online policy --- delay = `period`
    """

    on_val = 0
    copy_inv = copy.deepcopy(inv_num)
    time_list = new_data.index.tolist()

    for time in tqdm(range(len(time_list))):
        consume, order_list = update_order_bundle(copy_inv, consume, order_list)
        quantity = np.sum(consume, axis=0)

        t = time_list[time]
        current_order = new_data.loc[t, 'order_type']
        current = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        # whether the final time period `time` is added
        index = 0
        if current + delay_num * delay_period < datetime.timedelta(hours=24):
            index = 1
            if current_order in order_list:
                exp_demand = current_demand(new_data, prob, order_list, t, delta, delay_num, delay_period)

                # decision = 0, 1
                decision = bayes_selector(exp_demand, copy_inv, current_order, consume, order_list, obj)
                if decision == 1:
                    if obj == 'order':
                        on_val += 1
                    elif obj == 'item':
                        on_val += quantity[order_list.index(current_order)]
                    current_consume = order_dict[current_order]
                    for sku_key, sku_quantity in current_consume.items():
                        copy_inv[sku_key] -= sku_quantity
        else:
            break

    if index == 0:
        remain_list = time_list[time:]
        print('end_time', t, 'remain', remain_list)
        remain_order = new_data.loc[remain_list]['order_type'].values.tolist()
        remain_demand = [remain_order.count(order_list[i]) for i in range(len(order_list))]
        on_val += offline(remain_demand, copy_inv, consume, 'IP', obj)
    return on_val


def update_order_bundle(inv_num, consume, order_list):
    row = np.size(consume, 0)
    col = np.size(consume, 1)
    new_col = []
    for c in range(col):
        tmp = list(consume[0:row, c])
        tmp1 = [tmp[i] <= inv_num[i] for i in range(row)]
        if tmp1.count(False) == 0:
            new_col.append(c)
    new_consume = consume[0:row, new_col]
    new_order_list = [order_list[i] for i in new_col]
    return new_consume, new_order_list




