import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vectorA, vectorB):
    """
    Calulates the dot product of 2 vectors (lists)
    Input : 2 lists of equal size
    Ouput : dot product
    """
    if len(vectorA) != len(vectorB):
        raise(ValueError, "The lengths of vector should be equal for dot product")
        
    d_p = 0
    for i in range(len(vectorA)):
        d_p += vectorA[i] * vectorB[i]
        
    return d_p

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            return (self.g[0][0])    #determinant for 1x1 matrix
        else:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]
            return (a*d - b*c)    #determinant for 2x2 matrix
        
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        sum = 0
        for i in range(self.h):
            sum += self.g[i][i]
        
        return sum

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        det = self.determinant()    #Calculates the determinant of the matrix
        
        if self.h == 1:
            return Matrix([[1/det]])
        else:
            if det == 0:                 #Check if matrix has an Inverse
                raise(ValueError, "Determinant doesn't exist")
            else:
                a = self.g[0][0] / det
                b = self.g[0][1] / det
                c = self.g[1][0] / det
                d = self.g[1][1] / det
                return Matrix([[d, -b], [-c, a]])
    
    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        transpose = []
        
        for column in range(self.w):
            temp_row = []
            for row in range(self.h):
                temp_row.append(self.g[row][column])
            transpose.append(temp_row)
        
        return Matrix(transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        sum_matrix = []
        
        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                temp_row.append(self.g[row][column] + other.g[row][column]) # add corresponding elements of both the matrices
            sum_matrix.append(temp_row)
        
        return Matrix(sum_matrix)
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        negative = []
        
        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                temp_row.append(-self.g[row][column])
            negative.append(temp_row)
                
        return Matrix(negative)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
            
        subtracted_matrix = []
        
        for row in range(self.h):
            temp_row = []
            for column in range(self.w):
                temp_row.append(self.g[row][column] - other.g[row][column]) # add corresponding elements of both the matrices
            subtracted_matrix.append(temp_row)
        
        return Matrix(subtracted_matrix)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if self.w != other.h:
            raise(ValueError, "The column of 1st matrix should be equal to row of 2nd matrix for matrix multiplication")
            
        transpose_other = other.T()
        
        mat_product = []
        
        for rowA in self.g:
            temp_row = []
            for rowB in transpose_other.g:
                temp_row.append(dot_product(rowA, rowB))
            mat_product.append(temp_row)
            
        return Matrix(mat_product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            mat_product = []
            
            for row in self.g:
                temp_row = []
                for element in row:
                    temp_row.append(element * other)
                mat_product.append(temp_row)
                
            return Matrix(mat_product)
           
            