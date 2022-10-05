# @author: Yaqi Xie
# @email: xieyq188@gmail.com
# @date: 2022/07/16

import numpy as np
from gurobipy import *
setParam("OutputFlag", 0)
setParam("MIPGap", 0.01)


def lp_relax(demand, inv_num, consume):
    """
    Fluid LP Relaxation, Offline LP Relaxation
    :param demand: expected demand, hindsight demand of each order type j
    :param inv_num: inventory of each SKU i
    :param consume: matrix i * j, a_{ij},
    :return: LP's optimal solution and value
    max \sum_{j} x[j]
    s.t. \sum_{j} consume[i, j] x[j] <= inv_num[i], \forall i
         x[j] <= demand[j], \forall j
         x[j] > =0, \forall j
    """

    sku_num = np.size(consume, 0)
    order_num = np.size(consume, 1)

    model = Model()
    x = model.addVars(order_num, name="x")
    obj = quicksum(x[j] for j in range(order_num))
    model.setObjective(obj, GRB.MAXIMIZE)

    model.addConstrs(x[j] <= demand[j] for j in range(order_num))
    model.addConstrs((quicksum(consume[i, j] * x[j] for j in range(order_num)) <= inv_num[i] for i in range(sku_num)))
    model.addConstrs((x[j] >= 0 for j in range(order_num)))

    model.optimize()

    return model.getAttr('X'), model.getAttr('ObjVal')


def ip(demand, inv_num, consume):
    """
    Offline IP
    """

    sku_num = np.size(consume, 0)
    order_num = np.size(consume, 1)

    model = Model()
    x = model.addVars(order_num, vtype=GRB.INTEGER, name="x")
    obj = quicksum(x[j] for j in range(order_num))
    model.setObjective(obj, GRB.MAXIMIZE)

    model.addConstrs(x[j] <= demand[j] for j in range(order_num))
    model.addConstrs((quicksum(consume[i, j] * x[j] for j in range(order_num)) <= inv_num[i] for i in range(sku_num)))
    model.addConstrs((x[j] >= 0 for j in range(order_num)))

    model.optimize()

    return model.getAttr('X'), model.getAttr('ObjVal')


def lp_relax_obj2(demand, inv_num, consume):
    """
    max \sum_{j} x[j] * sum of consume's column j
    s.t. \sum_{j} consume[i, j] x[j] <= inv_num[i], \forall i
         x[j] <= demand[j], \forall j
         x[j] > =0, \forall j
    """

    sku_num = np.size(consume, 0)
    order_num = np.size(consume, 1)
    quantity = np.sum(consume, axis=0)

    model = Model()
    x = model.addVars(order_num, name="x")
    obj = quicksum(x[j] * quantity[j] for j in range(order_num))
    model.setObjective(obj, GRB.MAXIMIZE)

    model.addConstrs(x[j] <= demand[j] for j in range(order_num))
    model.addConstrs((quicksum(consume[i, j] * x[j] for j in range(order_num)) <= inv_num[i] for i in range(sku_num)))
    model.addConstrs((x[j] >= 0 for j in range(order_num)))

    model.optimize()

    return model.getAttr('X'), model.getAttr('ObjVal')


def ip_obj2(demand, inv_num, consume):
    """
    Offline IP
    """

    sku_num = np.size(consume, 0)
    order_num = np.size(consume, 1)
    quantity = np.sum(consume, axis=0)

    model = Model()
    x = model.addVars(order_num, vtype=GRB.INTEGER, name="x")
    obj = quicksum(x[j] * quantity[j] for j in range(order_num))
    model.setObjective(obj, GRB.MAXIMIZE)

    model.addConstrs(x[j] <= demand[j] for j in range(order_num))
    model.addConstrs((quicksum(consume[i, j] * x[j] for j in range(order_num)) <= inv_num[i] for i in range(sku_num)))
    model.addConstrs((x[j] >= 0 for j in range(order_num)))

    model.optimize()

    return model.getAttr('X'), model.getAttr('ObjVal')


def bayes_selector(exp_demand, inv_num, order, consume, order_list, obj):
    """
    Fluid Bayes Selector
    """
    if obj == 'order':
        lp_sol = lp_relax(exp_demand, inv_num, consume)[0]
    elif obj == 'item':
        lp_sol = lp_relax_obj2(exp_demand, inv_num, consume)[0]
    order_index = order_list.index(order)

    # 1 = accept to FDC
    dec = 0
    current_order_sol = lp_sol[order_index]
    if current_order_sol > exp_demand[order_index] / 2:
        dec = 1
    return dec


if __name__ == '__main__':
    dmd = [5, 5, 5, 6, 8, 10]
    inv = [10, 5, 6]
    con = np.array([[1, 0, 0, 1, 0, 2],
                       [0, 1, 2, 0, 0, 0],
                       [1, 2, 0, 0, 1, 0]])

    print(ip(dmd, inv, con)[0], ip(dmd, inv, con)[1])
    print(lp_relax(dmd, inv, con)[0], lp_relax(dmd, inv, con)[1])
