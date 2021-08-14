import numpy as np

matriz = np.array([['caso1','caso2','caso3','caso4'], ['caso2', 'caso4', 'caso6', 'caso0']])
vec_comp = np.array(['caso3','caso6', 'caso0', 'caso0'])
print( matriz == vec_comp)
np.equal(matriz , np.arange(vec_comp))


#matriz = np.array([[1, 3, 4, 5], [3, 5, 6, 7]])
#vec_comp = np.array([2, 5]).reshape((2, 1))

#print(vec_comp-matriz)