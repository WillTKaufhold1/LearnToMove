#!/home/wtk23/anaconda3/bin/python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import run

positions = [[0,0,0],[1,0,0],[0,1,0],[0,0,1]]

bonds = [[0,1],[0,2],[0,3],[1,2],[2,3]]

lengths = run.define_bonds(positions,bonds)

out = run.run_simulation(positions = positions, 
                         bonds = bonds,
                         lengths = lengths)
out = np.array(out)

breakpoint()
