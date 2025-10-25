#You must create a Python script called triangles.py that builds and explores Pascal’s Triangle without using any external libraries. The program should ask the user for the triangle’s depth, then generate and display the full Pascal’s Triangle using nested lists. You’ll implement four functions: generate(), which constructs the triangle and prints it; prime(row, triangle), which checks whether all numbers in a given row (by row number, not index) are divisible by that row number—true for rows where the row number is a prime; reflect(triangle), which displays and returns the triangle flipped upside down; and binary(triangle), which converts all odd numbers to 1 and even numbers to 0, creating a binary version of the triangle. All new triangle variants must be generated using list operations like .append() to build rows and elements step by step.

triangle = []

def generate():
    X = int(input())

    print(X)
    
    for i in range(X):
        row = [1]
        if i > 0:
            for j in range(1, i):
                row.append(triangle[i-1][j-1] + triangle[i-1][j])
            row.append(1)
        triangle.append(row)

    for i in triangle:
        for j in range(len(i)):
            if j == len(i)-1:
                print(i[j],end="")
            else:
                print(i[j],end=" ")
        print()
    return triangle

def prime(row,triangle):
    row_num = row
    
    if row_num < 1 or row_num > len(triangle):
        print("False")
        return

    if row_num < 2:
        print("False")
        return

    for k in range(2, row_num // 2 + 1):
        if row_num % k == 0:
            print("False")
            return

    index = triangle[row_num - 1]
    for i in index[1:-1]:
        if i % row_num != 0:
            print("False")
            return

    print("True")

def reflect(triangle):
    for i in triangle[::-1]:
        for j in range(len(i)):
            if j == len(i)-1:
                print(i[j],end="")
            else:
                print(i[j],end=" ")
        print()
    
def binary(triangle):
    for i in triangle:
        for j in range(len(i)):
            if i[j] % 2 !=0:
                print(1, end="")
            else:
                print(0,end="")
            
            if j != len(i)-1:
                print(" ",end="")
        print()


if __name__ == "__main__":
    print("Pascal's Triangle:")
    print("Depth:")
    generate()

    print("Prime row:")
    row = int(input())
    print(row)
    prime(row,triangle)

    print("Reflected Triangle:")
    reflect(triangle)

    print("Binary Triangle:")
    binary(triangle)
