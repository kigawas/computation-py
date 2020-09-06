def detect(arr, func):
    return next(filter(func, arr), None)
