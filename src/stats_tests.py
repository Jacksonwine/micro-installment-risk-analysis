"""统计检验模块：卡方检验与 Spearman 相关分析。"""

import pandas as pd
from scipy import stats


def chi_square_test(df, col1, col2):
    """对两个分类变量执行卡方检验。

    打印列联表、卡方值、自由度、p 值与结论，
    返回 (卡方值, p 值)。
    """
    table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    print(f"\n===== {col1} × {col2} =====")
    print(table)
    print(f"卡方值：{chi2:.4f}，自由度：{dof}，p值：{p:.4f}")
    print("结论：显著相关" if p < 0.05 else "结论：不显著，独立")
    return chi2, p


def spearman_pair(df, col_a, col_b):
    """计算两个有序变量的 Spearman 相关系数与 p 值，返回 (rho, p)。"""
    rho, p = stats.spearmanr(df[col_a], df[col_b])
    return rho, p
