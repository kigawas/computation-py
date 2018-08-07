def detect(arr, func):
    for i in arr:
        if func(i):
            return i
