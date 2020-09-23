import numpy as np

if __name__ == '__main__':
    N = np.random.normal(size=100)
    Y, X = np.histogram(N)
    dtype = [ ('X', np.float64), ('Y', np.float64) ]
    Z = np.array([ *zip(X, Y) ], dtype=dtype)
    np.savetxt('example.csv', Z, delimiter=',', fmt=['%f', '%f'], header='X,Y', comments='')

