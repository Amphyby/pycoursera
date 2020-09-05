# This is a sample Python script.
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def sum_of_digits():
    print(sum([int(x) for x in sys.argv[1]]))

def stairs():
    height = int(sys.argv[1])
    for i in range(height):
        j = height - i - 1
        line = " "*j+"#"*(i+1)
        print (line)
# Press the green button in the gutter to run the script.
def roots():
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
    desc = b ** 2 - 4 * a * c
    r1 = (-b + desc ** 0.5) / 2 / a
    r2 = (-b - desc ** 0.5) / 2 / a
    print(int(r1))
    print(int(r2))

if __name__ == '__main__':
    roots()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
