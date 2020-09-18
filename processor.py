# Matrix operations
def add_matrix(matrix_1, matrix_2):
    if len(matrix_1[0]) != len(matrix_2[0]) or len(matrix_1) != len(matrix_2):
        print("ERROR")
        exit()
    matrix_z = []
    for row in range(len(matrix_1)):
        matrix_x = matrix_2[row]
        matrix_y = matrix_1[row]
        lst = []
        for value in range(len(matrix_y)):
            lst.append(matrix_x[value] + matrix_y[value])
        matrix_z.append(lst)
    return print_matrix(matrix_z)


def mult_by_constant(matrix, constant):
    matrix_z = []
    for row in range(len(matrix)):
        matrix_y = matrix[row]
        lst = []
        for value in range(len(matrix_y)):
            lst.append(constant * matrix_y[value])
        matrix_z.append(lst)
    return print_matrix(matrix_z)


def mult_matrix(matrix_1, matrix_2):
    result = [[0 for x in range(len(matrix_2[0]))] for y in range(len(matrix_1))]
    if len(matrix_2) != len(matrix_1[0]):
        print("ERROR")
        exit()
    for i in range(len(matrix_1)):  # rows
        for j in range(len(matrix_2[0])):  # columns
            for k in range(len(matrix_2)):
                result[i][j] = result[i][j] + matrix_1[i][k] * matrix_2[k][j]
    return print_matrix(result)


def transpose_matrix(matrix, choice):
    unnest = [x for y in matrix for x in y]
    n = len(matrix[0])
    if choice == '1':  # main diagonal
        main_diagonal = [unnest[x::n] for x in range(len(matrix))]
        return print_matrix(main_diagonal)
    elif choice == '2':  # side diagonal
        reverse = unnest[::-1]
        side_diagonal = [reverse[x::n] for x in range(len(matrix))]
        return print_matrix(side_diagonal)
    elif choice == '3':
        vertical = []  # Transpose along vertical
        for i in range(len(matrix)):
            vertical.append(matrix[i][::-1])
        return print_matrix(vertical)
    elif choice == '4':
        horizontal = matrix[::-1]
        return print_matrix(horizontal)


def find_det(matrix):
    if len(matrix) != len(matrix[0]):
        print("""The operation cannot be performed.""")
        return main()
    elif len(matrix) == 1:
        return matrix[0].pop(0)
    elif len(matrix[0]) == 2:  # base case
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        determinant = 0
        for a in range(len(matrix)):
            if a % 2 == 0:
                inner = []
                for i in range(len(matrix)):
                    inner.append(matrix[i][:a] + matrix[i][a + 1:])
                inner.pop(0)
                determinant += matrix[0][a] * find_det(inner)
            else:
                inner = []
                for i in range(len(matrix)):
                    inner.append(matrix[i][:a] + matrix[i][a + 1:])
                inner.pop(0)
                determinant -= matrix[0][a] * find_det(inner)
        return determinant


def find_inverse(matrix):
    cofactors_of_matrix = []
    for a in range(len(matrix)):
        cofactors_of_rows = []
        for j in range(len(matrix[0])):
            inner = []
            for i in range(len(matrix)):
                inner.append(matrix[i][:j] + matrix[i][j + 1:])
            inner.pop(a)
            cofactors_of_rows.append((-1)**((a + 1) + (j + 1)) * find_det(inner))
        cofactors_of_matrix.append(cofactors_of_rows)
    unnest = [x for y in cofactors_of_matrix for x in y]
    n = len(cofactors_of_matrix)
    adj_of_matrix = [unnest[x::n] for x in range(len(cofactors_of_matrix))]
    full_inverse = []
    for a in range(len(matrix)):
        inverse_rows = []
        for j in range(len(matrix[0])):
            result = (1/find_det(matrix)) * adj_of_matrix[a][j]
            if result == 0.0 or result == -0.0:
                result = abs(result)
            inverse_rows.append(result)
        full_inverse.append(inverse_rows)
    return full_inverse


# Main() and input processing
def matrix_maker(lst):
    matrix = []

    for i in range(lst[0]):
        raw_input = input()
        row = raw_input.split()
        row = [float(x) for x in row]
        matrix.append(row)
    if len(matrix[0]) != lst[1]:
        print("The operation cannot be performed.")
        return main()
    else:
        return matrix


def matrix_checker(string):
    matrix_dimensions = [int(x) for x in string.split()]
    if len(matrix_dimensions) != 2:
        print("""The operation cannot be performed.""")
        return main()
    else:
        return matrix_dimensions


def print_matrix(matrix):
    print('The result is:')
    for row in matrix:
        rows = [str(x) for x in row]
        rows = ' '.join(rows)
        print(rows)
    return main()


def main():
    print("""1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices \n4. Transpose matrix
5. Calculate a determinant\n6. Inverse matrix\n0. Exit""")
    choice = input("Your choice: ")
    if choice == '1':
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter first matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)

        matrix_b_dimensions = matrix_checker(input("Enter size of second matrix: "))
        print("Enter second matrix: ")
        matrix_b = matrix_maker(matrix_b_dimensions)
        return add_matrix(matrix_a, matrix_b)
    elif choice == '2':
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter first matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)

        constant = float(input('Enter constant: '))
        return mult_by_constant(matrix_a, constant)
    elif choice == '3':
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter first matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)

        matrix_b_dimensions = matrix_checker(input("Enter size of second matrix: "))
        print("Enter second matrix: ")
        matrix_b = matrix_maker(matrix_b_dimensions)
        return mult_matrix(matrix_a, matrix_b)
    elif choice == '4':
        print("""1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line""")
        choice = input("Your choice: ")
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)
        return transpose_matrix(matrix_a, choice)
    elif choice == '5':
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)
        print(f"""The result is:\n{find_det(matrix_a)}\n""")
        return main()
    elif choice == '6':
        matrix_a_dimensions = matrix_checker(input("Enter size of first matrix: "))
        print("Enter matrix: ")
        matrix_a = matrix_maker(matrix_a_dimensions)
        print(f"""The result is:\n{print_matrix(find_inverse(matrix_a))}\n""")
        return main()
    elif choice == '0':
        exit()


main()
