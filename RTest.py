__author__ = 'Spencer'

import rpy2.robjects as robjects

def main():
    pi = robjects.r('pi')
    pi2 = [x for x in pi]
    print(pi2)

if __name__ == '__main__':
    main()