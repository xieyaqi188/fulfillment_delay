
# @date: 2022/07/20

import numpy as np
import pandas as pd
import datetime


def sku(data):
    """
    determine SKU dict
    """
    # inventory, SKU
    # sku_dict = {i: SKU id}
    sku_list = data['sku_ID'].unique().tolist()
    sku_dict = {}
    for i in range(len(sku_list)):
        sku_dict[i] = sku_list[i]
    print("SKU --- ", len(sku_list), sku_dict)
    return sku_dict


def inv_1(data, fdc, day_set):
    """
    SKU inventory in the FDC each day
    :param data:
    :param fdc:
    :param day_set:
    :return: inv_dict = {day: [SKU #]}
    """
    inv_dict = {}
    order_fdc = data[data['dc_ori'] == fdc]
    sku_list = data['sku_ID'].unique().tolist()
    for d in range(len(day_set)):
        inv_the_day = []
        day = day_set[d]
        order_fdc_the_day = order_fdc.loc[day]
        for i in range(len(sku_list)):
            tmp_sku_order = order_fdc_the_day[order_fdc_the_day['sku_ID'] == sku_list[i]]
            inv_the_day.append(tmp_sku_order['quantity'].sum())
        inv_dict[day] = inv_the_day
    print("inventory:", inv_dict)
    return inv_dict


def inv_2(data, fdc, day_set, load):
    """
    total SKU inventory in the FDC / day #
    :param data:
    :param fdc:
    :param day_set:
    :return: inv_num = [SKU #]
    """

    inv_num = []
    order_fdc = data[data['dc_ori'] == fdc]
    sku_list = data['sku_ID'].unique().tolist()
    for i in range(len(sku_list)):
        tmp_sku_order = order_fdc[order_fdc['sku_ID'] == sku_list[i]]
        inv_num.append(round(load * tmp_sku_order['quantity'].sum() / len(day_set)))
    print("inventory:", len(inv_num), inv_num)
    return inv_num


def order_demand(data, day_set, delta):
    """
    order types, demand probability in each time delta
    :param data:
    :param day_set:
    :param delta:
    :return: order_dict = {j: {sku key: #}}, prob = {order: {timedelta: lambda}}
            new_data = Dataframe[order_type, order_time]
    """

    order_id_list = data['order_ID'].unique().tolist()
    sku_list = data['sku_ID'].unique().tolist()
    order_dict = {}
    # prob = {}
    prob = {'weekday': {}, 'weekend': {}}
    index_j = 0

    one_day = datetime.timedelta(days=1)
    delta_num = int(one_day / delta)

    new_data = pd.DataFrame(data=None)

    for i in order_id_list:
        tmp = data[data['order_ID'] == i]
        tmp_list = tmp['sku_ID'].values.tolist()
        tmp_list2 = [sku_list.index(j) for j in tmp_list]
        tmp_list3 = sorted(tmp_list2)
        tmp_list3 = list(dict.fromkeys(tmp_list3))

        t = tmp[tmp['sku_ID'] == tmp_list[0]].index.tolist()
        time = datetime.timedelta(hours=t[0].hour, minutes=t[0].minute, seconds=t[0].second)
        current_delta = time // delta
        tt = pd.to_datetime(t[0])
        is_weekend = tt.dayofweek >= 5

        tmp_value = {}
        for j in range(0, len(tmp_list3)):
            tmp_value[tmp_list3[j]] = int(tmp[tmp['sku_ID'] == sku_list[tmp_list3[j]]]['quantity'])
        if tmp_value in order_dict.values():
            key_list = list(order_dict.keys())
            value_list = list(order_dict.values())
            tmp_key = key_list[value_list.index(tmp_value)]
            # prob[tmp_key][current_delta] += 1
            prob['weekend' if is_weekend else 'weekday'][tmp_key][current_delta] += 1
            tmp_data = pd.DataFrame(data=[[tmp_key, t[0]]], columns=['order_type', 'order_time'])
            new_data = pd.concat([new_data, tmp_data])
        else:
            order_dict[index_j] = tmp_value
            # prob[index_j] = {}
            # for num in range(delta_num):
            #     prob[index_j][num] = 0
            # prob[index_j][current_delta] = 1
            prob['weekday'][index_j] = {n: 0 for n in range(delta_num)}
            prob['weekend'][index_j] = {n: 0 for n in range(delta_num)}
            prob['weekend' if is_weekend else 'weekday'][index_j][current_delta] = 1
            tmp_data = pd.DataFrame(data=[[index_j, t[0]]], columns=['order_type', 'order_time'])
            new_data = pd.concat([new_data, tmp_data])
            index_j += 1

        # Normalize probabilities by the number of days in each category
        weekday_count = sum(1 for d in day_set if pd.to_datetime(d).dayofweek < 5)
        weekend_count = len(day_set) - weekday_count

    for o in range(index_j):
        for num in range(delta_num):
            # prob[o][num] = prob[o][num] / len(day_set)
            prob['weekday'][o][num] /= weekday_count
            prob['weekend'][o][num] /= weekend_count

    new_data = new_data.set_index('order_time')
    new_data = new_data.sort_index()

    # print("Order: ", len(order_dict), order_dict)
    # print("Probability: ", prob)
    print("Order: ", len(order_dict), order_dict)
    print("Probability: ", len(order_dict), delta_num)
    print("New data:", len(new_data.index.tolist()))
    return order_dict, prob, new_data


def consume_mat(inv_num, order_dict):
    sku_num = len(inv_num)
    order_num = len(order_dict)
    consume = np.full((sku_num, order_num), 0)
    for order_key, order in order_dict.items():
        for sku_key, sku_quantity in order.items():
            consume[sku_key, order_key] = sku_quantity
    print(consume)
    return consume


if __name__ == '__main__':
    set = np.load('D:/Pycharm/fulfillment_delay/jd_data/pre_data/setting.npy', allow_pickle=True)
    set = set.item()
    sample_set = set['sample_set']
    day = set['day_set']
    dc = set['fdc']
    load = 1
    time_delta = datetime.timedelta(minutes=60)
    print("FDC", dc)
    print(len(day), day)

    sku(sample_set)
    inv_1(sample_set, dc, day)
    inv = inv_2(sample_set, dc, day, load)
    order, p, new = order_demand(sample_set, day, time_delta)
    consume_mat(inv, order)



