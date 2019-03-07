import sys


if __name__ == '__main__':
    a = sys.stdin.readline()
    b = map(int, sys.stdin.readline().strip().split(" "))
    c = sorted(b)
    print(*c)