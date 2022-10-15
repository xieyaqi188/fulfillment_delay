# The Benefits of Delay to Online Decision-Making

Code for numerical experiments in [**Yaqi Xie, Will Ma, Linwei Xin. The Benefits of Delay to Online Decision-Making.**](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4248326)

### Multisecretary Problem

1. "./secretary_problem/test.py" runs Algorithm 1 with different parameter settings.
2. "./secretary_problem/result_plot.py" runs plots.

### Order-Fulfillment Problem

Note: Some file paths to read or save .csv file or .np file are absolute paths, please change them in local computers.

1. We use a dataset of JD.com by [Shen Z, Tang C, Wu D, Yuan R, Zhou W (2020) Jd.com: Transaction level data for the 2020 msom data driven research challenge. Manufacturing & Service Operations Management Forthcoming.](https://pubsonline.informs.org/doi/abs/10.1287/msom.2020.0900) **Add the dataset into the file "./jd_data/JD_data".** Their two tables "JD_order_data.csv" and "JD_network_data.csv" are used as follows in "./fdc_rdc_fulfillment/sample.py".

```python
network = pd.read_csv("D:/Pycharm/fulfillment_delay/jd_data/JD_data/JD_network_data.csv")
order = pd.read_csv("D:/Pycharm/fulfillment_delay/jd_data/pre_data/order_1p.csv")
```

To get the table "order_1p.csv" preprocessed from "JD_order_data.csv", run "./jd_data/data_filter.ipynb".

2. "./fdc_rdc_fulfillment/main_test.py" runs Algorithm 2 with different FDCs and other parameters settings. Note that `fdc` must be distribution centers that are not RDC.
3. "./fdc_rdc_fulfillment/result_plot.py" runs plots.
