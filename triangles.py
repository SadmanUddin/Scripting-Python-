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