def merge_dict(dic1, dic2):
    """Merge dic2 to dic1 without changing dic1"""
    return {k: v for d in (dic1, dic2) for k, v in d.items()}
