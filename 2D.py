""" 2D double broadcas matrix multiplication """

from sys import argv

from math import sqrt
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

Q = int(sqrt(size))

myrow,   mycol =   int(rank//Q),             int(rank%Q)
rowComm, colComm = comm.Split(myrow, mycol), comm.Split(mycol, myrow)

N = int(argv[1])//Q
A = np.random.randint(-1000, 1000, (N, N))
B = np.random.randint(-1000, 1000, (N, N))

# with open(f'data\\data-A-{rank}.dat', 'rb') as f:
# 	A = np.load(f)
# with open(f'data\\data-B-{rank}.dat', 'rb') as f:
# 	B = np.load(f)

BuffA = np.empty(A.shape, dtype='i')
BuffB = np.empty(B.shape, dtype='i')
C = np.zeros(A.shape)

t0 = MPI.Wtime()

for k in range(Q):
	tmpA = A if mycol == k else BuffA
	tmpB = B if myrow == k else BuffB

	rowComm.Bcast(tmpA, root=k)
	colComm.Bcast(tmpB, root=k)

	C += np.matmul(tmpA, tmpB)

tn = MPI.Wtime()

t0s = comm.gather(t0, root=0)
tns = comm.gather(tn, root=0)

if rank == 0:
	print(round(max(tns) - min(t0s), 4))

# with open(f'res\\res-{rank}.dat', 'wb') as f:
# 	np.save(f, C)
