from random import randint


def clamp(n, minn, maxn):
    return max(min(n, maxn), minn)


def rand_seq(n, minn, maxn):
    return [randint(minn, maxn) for _ in range(n)]
