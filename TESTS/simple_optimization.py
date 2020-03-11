#!/home/wtk23/anaconda3/bin/python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import run
from multiprocessing import Pool

positions = [[0,0,0],[1,0,0],[0,1,0],[0,0,1]]
bonds = [[0,1],[0,2],[0,3],[1,2],[2,3]]

lengths = run.define_bonds(positions,bonds)

def get_distribution(x):
    out = run.run_simulation(positions = positions, 
                         bonds = bonds,
                         lengths = lengths,RANDOM_SEED=x)
    return out

p = Pool(5)

a = p.map(get_distribution, np.random.rand(5))

breakpoint()
