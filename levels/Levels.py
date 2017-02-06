n = numRows = numCols = 17
walls = [['0' for i in range(n)] for j in range(n)]
m = n//2
walls[n-5][n-5] = walls[n-6][n-6] = 's'
for i in range(3, numRows-3, 2):
    walls[i][1] = walls[1][i] = walls[i][n-2] = walls[n-2][i] = 'g'
grid = [[walls[j][i][0] for j in range(1,n-1)] for i in range(1, n-1)]
print '\n'.join([''.join(row) for row in grid])
