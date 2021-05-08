def idd_split_path(idd, suffix=None):
    idd = str(idd)
    if suffix:
        return f"{idd[2:4]}/{idd[7:8]}/{idd[23:]}/{idd}.{suffix}"
    return f"{idd[2:4]}/{idd[7:8]}/{idd[23:]}"
