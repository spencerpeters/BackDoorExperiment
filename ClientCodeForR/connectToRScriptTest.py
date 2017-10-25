from oldCode.jsonTest import reformatR

__author__ = 'Spencer'

import json

def main():
    filepath = "/Users/Spencer/R-Projects/AdjustmentEnumeration/RtoPyTest.json"
    # subprocess.call(["Rscript",
    #                  "/Users/Spencer/R-Projects/AdjustmentEnumeration/ScriptServingPython.R",
    #                  "1",
    #                  "10",
    #                  "0.3",
    #                  filepath])
    result = json.load(open(filepath))
    for sink in result[0]:
        sink = reformatR(sink)
        print(2**9)
        print(len(sink))
        print(sink)
        print("\n")

if __name__ == '__main__':
    main()