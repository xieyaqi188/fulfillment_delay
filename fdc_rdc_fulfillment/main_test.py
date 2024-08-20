
# @date: 2022/07/21

import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime

from online_offline import offline, online, batch
from setting import sku, inv_1, inv_2, order_demand, consume_mat
from lp_policy import ip, lp_relax
from sample import sample_filter


if __name__ == '__main__':
    """
    FDC RDC order fulfillment 
    :param sku_dict: {sku type: SKU ID} 
    :param inv_num: [inv #]
    :param order_dict: {order type: {sku key: sku #}}
    :param prob: {order type: {timedelta: lambda}}
    :param new_data: Dataframe[order_time, order_type]
    :param consume: sku * order
    :param delay_period: the length of one period
    
    :param delay_list: 
    :param delta: timedelta for `prob`
    """

    fdc = 46
    sett = sample_filter(fdc)
    # sett = np.load('D:/Pycharm/fulfillment_delay/jd_data/pre_data/setting.npy', allow_pickle=True)
    # sett = sett.item()
    sample_set = sett['sample_set']
    day_set = sett['day_set']
    fdc = sett['fdc']
    rdc = sett['rdc']
    print("\n ---Generating Sample--- \n")
    print("FDC", fdc, "RDC", rdc)
    print(len(day_set), day_set)

    sku_dict = sku(sample_set)

    # # INV1: true inventory from raw data
    # inv_num_set = inv_1(sample_set, fdc, day_set)
    # INV2: average inventory
    load = 1
    inv_num = inv_2(sample_set, fdc, day_set, load)

    delta = datetime.timedelta(minutes=30)
    order_dict, prob, new_data = order_demand(sample_set, day_set, delta)
    order_list = list(order_dict.keys())

    # delay
    delay_period = datetime.timedelta(minutes=30)
    delay_list = [0, 1, 2, 3, 4, 6, 8]
    delay = [delay_period * d for d in delay_list]

    # objective function: obj = 'order', 'item'
    obj = 'order'

    # result = {day: {'cur': cur_val, 'opt': opt_val, 'online_delay': []}
    result = {}
    total_ip_opt = 0
    total_lp_opt = 0
    total_online_val = [0] * len(delay_list)
    total_batch_val = [0] * len(delay_list)
    runtime = datetime.timedelta(seconds=0)

    for i in range(len(day_set)):

        d = day_set[i]
        # INV1:
        # inv_num = inv_num_set[d]
        consume = consume_mat(inv_num, order_dict)

        # INV1: gap(): {day: [fdc, rdc, day, (np.size(consume, 0), np.size(consume, 1)), cur_val, opt_val]}
        # res = gap(fdc, [d])
        # result[d]['cur'] = res[d][4]
        # result[d]['opt'] = res[d][5]
        # print(d, 'cur_val:', res[d][4], 'opt_val:', res[d][5])

        current_data = new_data.loc[d]
        time_list = current_data.index.tolist()
        # run algorithm
        # result[d] = {}
        run_start = datetime.datetime.now()

        # optimal IP & LP
        remain_order = current_data.loc[time_list]['order_type'].values.tolist()
        off_demand = [remain_order.count(order_list[i]) for i in range(len(order_list))]
        run_start = datetime.datetime.now()
        ip_opt_val = offline(off_demand, inv_num, consume, 'IP', obj)
        run_end = datetime.datetime.now()
        print('\nIP running time', run_end - run_start)
        run_start = datetime.datetime.now()
        lp_opt_val = offline(off_demand, inv_num, consume, 'LP', obj)
        run_end = datetime.datetime.now()
        print('\nLP running time', run_end - run_start)
        print("optimal IP value: ", ip_opt_val)
        print("optimal LP value: ", lp_opt_val)
        total_ip_opt += ip_opt_val
        total_lp_opt += lp_opt_val

        online_val = [0] * len(delay_list)
        batch_val = [0] * len(delay_list)
        for K in delay_list:
            if K == 0:
                on_res = online(current_data, prob, inv_num, consume, order_dict, order_list, delta, K, delay_period, obj)
                batch_res = on_res
            else:
                batch_res = batch(current_data, prob, inv_num, consume, order_dict, order_list, delta, K, delay_period, obj)
                on_res = online(current_data, prob, inv_num, consume, order_dict, order_list, delta, K, delay_period, obj)
            online_val[delay_list.index(K)] = on_res
            batch_val[delay_list.index(K)] = batch_res
            print(d, ' with delay', K, 'online', on_res, '; batch', batch_res)
            total_online_val[delay_list.index(K)] += on_res
            total_batch_val[delay_list.index(K)] += batch_res
        # result[d]['online_delay'] = online_val
        # result[d]['online_batch'] = batch_val
        run_end = datetime.datetime.now()
        runtime += run_end - run_start
        # print(d, 'cur_val', res[d][4], 'opt_val', res[d][5], 'online', online_val)
        print(d, 'IP_opt_val', ip_opt_val, 'LP_opt_val', lp_opt_val, 'online', online_val, 'batch', batch_val)

    test_ip = total_ip_opt / len(day_set)
    test_lp = total_lp_opt / len(day_set)
    on_delay = [a / len(day_set) for a in total_online_val]
    on_batch = [a / len(day_set) for a in total_batch_val]
    print('FDC', fdc, 'RDC', rdc)
    print('average IP value: ', test_ip, 'average LP value: ', test_lp)
    print('average online values - delay: ', on_delay)
    print('average online values - batch: ', on_batch)
    print('average running time: ', runtime / len(day_set) / len(delay_list))

    # save results
    output = {"FDC": fdc, "RDC": rdc, "off_IP": test_ip, "off_LP": test_lp, "on_delay": on_delay, "on_batch": on_batch,
              "delay": delay}
    np.save('./new_result/time_batch_fdc{FDC}_rdc{RDC}.npy'.format(FDC=fdc, RDC=rdc), output)

