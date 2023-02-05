
# @date: 2022/09/07

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


def sample_filter(fdc):
    network = pd.read_csv("D:/Pycharm/fulfillment_delay/jd_data/JD_data/JD_network_data.csv")
    order = pd.read_csv("D:/Pycharm/fulfillment_delay/jd_data/pre_data/order_1p.csv")
    order['order_date'] = pd.to_datetime(order['order_date'])
    order['order_time'] = pd.to_datetime(order['order_time'])

    rdc = int(network[network['dc_ID'] == fdc]['region_ID'])
    print(fdc, rdc)
    order_fdc = order[order['dc_des'] == fdc]
    order_fdc_fdc_rdc = order_fdc[order_fdc.dc_ori.isin([fdc, rdc])]

    # duplicate orders with the same datetime
    tmp_order_fdc_fdc_rdc = order_fdc_fdc_rdc.drop_duplicates(subset=['order_ID'], keep='first')
    time = tmp_order_fdc_fdc_rdc['order_time'].unique()
    order_fdc_fdc_rdc = order_fdc_fdc_rdc.set_index(['order_ID', 'sku_ID'])
    for t in time:
        tmp_co = tmp_order_fdc_fdc_rdc[tmp_order_fdc_fdc_rdc['order_time'] == t]
        tmp_clen = len(tmp_co.index)
        if tmp_clen > 1:
            ci = tmp_co.index.tolist()
            for i in range(1, tmp_clen):
                cr_date = tmp_co.loc[ci[i]]['order_time']
                while cr_date in time:
                    a = int(np.random.choice(range(1, 61)))
                    cr_date += datetime.timedelta(seconds=a)
                oi = tmp_order_fdc_fdc_rdc.loc[ci[i], 'order_ID']
                order_fdc_fdc_rdc.loc[
                    order_fdc_fdc_rdc.index.get_level_values('order_ID') == oi, 'order_time'] = cr_date
                tmp_order_fdc_fdc_rdc.loc[ci[i], 'order_time'] = cr_date
                time = tmp_order_fdc_fdc_rdc['order_time'].unique()
    order_fdc_fdc_rdc.reset_index(inplace=True)
    order_fdc_fdc_rdc.to_csv('D:/Pycharm/fulfillment_delay/jd_data/pre_data/order_fdc_fdc_rdc.csv', index=False)

    order = order_fdc_fdc_rdc
    temp = order.drop_duplicates(subset=['order_ID'], keep='first')
    order = order.set_index('order_time')
    order = order.sort_index()
    temp = temp.set_index('order_time')
    temp = temp.sort_index()
    # tmp: Selling in each day
    temp["count"] = 1
    temp_fdc = temp[temp['dc_ori'] == fdc]
    temp_rdc = temp[temp['dc_ori'] == rdc]
    temp_fdc_one_day = temp_fdc.resample('D').sum()
    temp_rdc_one_day = temp_rdc.resample('D').sum()
    day_list = temp_rdc_one_day.index.format()

    fdc_day_num = temp_fdc_one_day['count'].tolist()
    rdc_day_num = temp_rdc_one_day['count'].tolist()
    print(day_list, len(day_list))
    print(fdc_day_num, sum(fdc_day_num))
    print(rdc_day_num, sum(rdc_day_num))

    # count order number by fdc and rdc per day: {date: (total #, fdc #, rdc #)}
    fdc_rdc = {}
    fdc_rdc_day_num = []
    for i in range(len(day_list)):
        fdc_rdc_day_num.append(fdc_day_num[i] + rdc_day_num[i])
        fdc_rdc[day_list[i]] = (fdc_day_num[i] + rdc_day_num[i], fdc_day_num[i], rdc_day_num[i])
    print("FDC", fdc, ", RDC", rdc, "---", fdc_rdc)

    print(sorted(fdc_rdc_day_num))
    our_day_list = []
    our_demand = {}
    demand_num = 0
    for i in range(len(day_list)):
        d = day_list[i]
        if 10000 >= fdc_rdc_day_num[i] >= 0:
            our_demand[d] = fdc_rdc_day_num[i]
            our_day_list.append(d)
            demand_num += fdc_rdc_day_num[i]
    print(our_demand, len(our_demand))
    print(demand_num, demand_num / len(our_day_list))

    order_our_date = pd.DataFrame(data=None)
    for i in range(len(our_day_list)):
        temp_data = order.loc[our_day_list[i]]
        order_our_date = pd.concat([order_our_date, temp_data])
    order_our_date = order_our_date.sort_index()
    order_our_date.head()
    para_input = {"sample_set": order_our_date, "day_set": our_day_list, "fdc": fdc, "rdc": rdc}
    np.save('D:/Pycharm/fulfillment_delay/jd_data/pre_data/setting.npy', para_input)
    return para_input

