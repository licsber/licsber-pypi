from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


def wait_for_execute(
        fn,
        iterator,
        total=None,
        max_workers=None,
        initializer=None,
        return_iter=False
):
    """
    简易的自带进度条的多线程执行
    :param fn: 处理单个iterator的返回函数
    :param iterator: 可迭代即可
    :param total: 显示总数 不传则无总体进度条
    :param max_workers: 最大干活线程数
    :param initializer: 初始化函数
    :param return_iter: 是否直接返回结果
    :return:
    """
    with ThreadPoolExecutor(initializer=initializer, max_workers=max_workers) as p:
        it = p.map(fn, iterator)
        bar = tqdm(it, total=total)
        return list(bar) if not return_iter else bar
