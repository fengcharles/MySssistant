# -*-coding:utf-8-*-


a = 10

def show():
    global a
    a += 19
    print(a)


if __name__ == "__main__":
    a = 1
    b = 2

    print("%s,%d,%d" % (a, b, a))
