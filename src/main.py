import os, sys
#print(os.getcwd)
#print(sys.path)

#add this path to python for search module
# sys.path.append("..")
# print(sys.path)

from d04_modelling.test_train import sample

# can do this because we have __init__ in folder


def main():

    x = [1,2,3,4,5]
    y =[1,4,9,16,25]
    sample(x,y)
        



if __name__ == '__main__':
    main()