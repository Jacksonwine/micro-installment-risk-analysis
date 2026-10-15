"""数据清洗与量化编码模块。

本模块与 notebooks/01_data_cleaning.ipynb 中的内联逻辑等价，
将问卷原始作答映射为可分析的数值变量，便于在其他脚本中复用。
"""

import re

import pandas as pd

# 第 3 题（多选）的选项短名，用于拆分 0/1 变量
SCENE_OPTIONS = [
    "文娱票务",
    "潮玩周边",
    "户外与娱乐用品",
    "假期旅游",
    "数码电子",
    "服饰美妆",
    "二手交易",
]


def find_col(df_raw, prefix):
    """按前缀查找原始列名（容忍不可见空白字符）。"""
    for c in df_raw.columns:
        c_clean = str(c).strip().replace("\xa0", " ").replace("\u3000", " ")
        if c_clean.startswith(prefix):
            return c
    return None


def clean_text(s):
    """清洗文本字段中的不可见字符与多余空白。"""
    if not isinstance(s, str):
        return s
    s = s.replace("\xa0", " ").replace("\u3000", " ").replace("\u200b", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# 原始列名前缀 -> 分析用短名
COL_MAP = {
    "age": "1、",
    "impulse": "2、",
    "scene": "3、",
    "demand_4": "4、",
    "cooling": "5、",
    "focus": "6、",
    "living": "7、",
    "disposable": "8、",
    "installment_use": "9、",
    "shortage": "10、",
    "limit_accept": "11、",
    "demand": "12、",
    "trust": "13、",
}

# 有序变量量化编码（选项 -> 等级/数值）
LIVING_MAP = {
    "1000–1500元": 1250,
    "1500–2000元": 1750,
    "2000–3000元": 2500,
    "3000元以上": 3500,
}
DISPOSABLE_MAP = {
    "10%以下": 0.05,
    "10%–20%": 0.15,
    "20%–30%": 0.25,
    "30%以上": 0.35,
}
IMPULSE_RANK = {
    "几乎没有，消费很理性": 1,
    "偶尔会有": 2,
    "经常有，经常不知不觉花超预算": 3,
}
DEMAND_RANK = {
    "完全没有": 1,
    "几乎没有": 2,
    "偶尔有": 3,
    "经常有": 4,
}
DEMAND4_RANK = {
    "不会，不需要分期": 1,
    "可能会": 2,
    "会，极大降低了购买门槛": 3,
}
COOLING_RANK = {
    "不需要": 1,
    "一般/无所谓": 2,
    "能，提供了一层很好的后悔与冷静机制": 3,
}
TRUST_RANK = {
    "都怀疑": 1,
    "差不多": 2,
    "更信任": 3,
}
INSTALLMENT_RANK = {
    "从没用过": 1,
    "用过，但已经关掉/不再用了": 2,
    "用过几次，基本按时还": 3,
}
SHORTAGE_RANK = {
    "借新的钱来还旧的": 1,
    "找朋友或家人借": 2,
    "减少开支撑过去": 3,
}
LIMIT_RANK = {
    "不能接受": 1,
    "一般": 2,
    "能接受": 3,
}


def rename_columns(df_raw):
    """将原始列名映射为分析用短名，并仅保留 13 道题目列。"""
    rename_map = {}
    for new_name, prefix in COL_MAP.items():
        old = find_col(df_raw, prefix)
        if old is not None:
            rename_map[old] = new_name
    df = df_raw.rename(columns=rename_map)
    return df[list(COL_MAP.keys())].copy()


def encode_variables(df):
    """将分类变量映射为有序数值变量，返回新增量化列后的 DataFrame。"""
    df = df.copy()
    df["living_num"] = df["living"].map(LIVING_MAP)
    df["disposable_num"] = df["disposable"].map(DISPOSABLE_MAP)
    df["impulse_rank"] = df["impulse"].map(IMPULSE_RANK)
    df["demand_rank"] = df["demand"].map(DEMAND_RANK)
    df["demand4_rank"] = df["demand_4"].map(DEMAND4_RANK)
    df["cooling_rank"] = df["cooling"].map(COOLING_RANK)
    df["trust_rank"] = df["trust"].map(TRUST_RANK)
    df["installment_rank"] = df["installment_use"].map(INSTALLMENT_RANK)
    df["shortage_rank"] = df["shortage"].map(SHORTAGE_RANK)
    df["limit_rank"] = df["limit_accept"].map(LIMIT_RANK)
    return df


def split_multi_select(df, scene_options=None):
    """将第 3 题多选题拆分为多个 0/1 变量（scene_<选项>）。"""
    if scene_options is None:
        scene_options = SCENE_OPTIONS
    df = df.copy()
    for opt in scene_options:
        df[f"scene_{opt}"] = df["scene"].fillna("").str.contains(opt).astype(int)
    return df
