"""回归分析模块：OLS 与有序 Logit。"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel


def run_ols(df, y_col, x_cols):
    """执行多元线性回归（自动添加常数项），返回拟合结果。"""
    X = sm.add_constant(df[x_cols])
    y = df[y_col]
    return sm.OLS(y, X).fit()


def run_ordered_logit(df, y_col, x_cols):
    """执行有序 Logit 回归，返回拟合结果。"""
    X = df[x_cols]
    y = df[y_col]
    return OrderedModel(y, X, distr="logit").fit(method="bfgs")
