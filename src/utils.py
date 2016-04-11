from __future__ import print_function

def merge_dict(dic1, dic2):
    dm = {}
    for k,v in dic1.iteritems():
        dm[k] = v
    for k,v in dic2.iteritems():
        dm[k] = v
    return dm

def test():
    d1 = {'a':1,'b':2,'c':3}
    d2 = {'aaa':2}
    print(merge_dict(d1,d2))

if __name__ == '__main__':
    test()
