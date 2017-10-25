__author__ = 'Spencer'
import json
import pprint

def main():
    x = json.load(open("/Users/Spencer/R-Projects/AdjustmentEnumeration/babak.json"))
    z = reformatR(x)# print(json.dumps(x,sort_keys=True, indent=4))
    # print(json.dumps(y,sort_keys=True, indent=4))
    print(z)


def reformatR(x):
    y = []
    for ta in x:
        treatment = ta[0]
        adjustments = ta[1]
        adjustmentsList = [adj for adj in adjustments.values()]
        y.append([treatment, adjustmentsList])

    # we want to map closures to lists of admissible treatments. The number of unique closures is what is relevant.
    z = {}
    for ta in y:
        treatment = ta[0]
        adjustments = ta[1]
        for adj in adjustments:
            closureList = (treatment + adj)
            closureList.sort()
            closure = tuple(closureList)
            if (closure not in z):
                z[closure] = [adj]
            else:
                z[closure].append(adj)

    return z


if __name__ == '__main__':
    main()