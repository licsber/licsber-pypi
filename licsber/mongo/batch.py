def random_get(db, size=512, match=None, project=None, stream=False):
    """
    随机获取表中size条数据.
    :param db: mongo表.
    :param size: 大小, 表条目总数小于此值时返回所有.
    :param match: 额外查找条件.
    :param project: 过滤返回字段.
    :param stream: 是否直接加载到本地.
    :return: 可遍历的条目.
    """
    if match is None:
        match = {}

    if project:
        res = db.aggregate([
            {'$match': match},
            {'$sample': {'size': size}},
            {'$project': project},
        ])
    else:
        res = db.aggregate([
            {'$match': match},
            {'$sample': {'size': size}},
        ])

    if not stream:
        res = list(res)
        print(f"随机获取数据库{len(res)}条记录.")

    return res
