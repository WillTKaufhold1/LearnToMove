#todo: TABULATED POTENTIAL!

import numpy as np 

def get_length(positions,A,B):
    positions = np.array(positions)
    return np.sqrt(np.sum((positions[A] - positions[B])**2))

def define_bonds(positions,bonds):
    bond_lengths = []
    for i in bonds:
        bond_lengths.append(get_length(positions,i[0],i[1]))
    return bond_lengths

def run_simulation(N_steps = 1e7, 
                   positions = [[0,0,0],[1,0,0]], 
                   bonds = [[0,1]],
                   lengths = [[1,1]],
                   RANDOM_SEED = 1):


    import gsd.hoomd
    import hoomd
    import hoomd.md
    hoomd.context.initialize("")
    
    snapshot = hoomd.data.make_snapshot(N=len(positions),
                                        box = hoomd.data.boxdim(Lx=200, Ly=200,Lz = 200),
                                        particle_types = ['A'],
                                        bond_types=[f'dna{i}' for i in range(len(bonds))]
                                       )

    snapshot.particles.position[:] = positions
    snapshot.particles.typeid[:] = 0
    snapshot.bonds.resize(len(bonds))

    snapshot.bonds.group[:] = bonds
    snapshot.bonds.types = [f'dna{i}' for i in range(len(bonds))]
    snapshot.bonds.typeid[:] = np.arange(len(bonds)).astype(dtype = int)


    print (snapshot.bonds.types) 
    hoomd.init.read_snapshot(snapshot)

    nl = hoomd.md.nlist.tree()

    lj = hoomd.md.pair.lj(r_cut=2.5, nlist=nl)
    lj.pair_coeff.set('A','A',epsilon = 10.000,sigma = 0.3)

    harmonic = hoomd.md.bond.harmonic()
    for index,i in enumerate(lengths):  
        print (f'dna{index}')
        harmonic.bond_coeff.set(f'dna{index}', k=10.0, r0=i); 

    hoomd.md.integrate.mode_standard(dt=0.002)
    all = hoomd.group.all()
    hoomd.md.integrate.langevin(group=all, kT=0.2, seed=42)
    
    hoomd.md.update.zero_momentum(period = 4)
    
    hoomd.analyze.log(filename="log-output.log",
                  quantities=['potential_energy', 'temperature'],
                  period=2e5,
                  overwrite=True)

    TRAJ_DUMP_PERIOD = 2e5

    hoomd.dump.gsd(f"trajectory{RANDOM_SEED}.gsd", period=TRAJ_DUMP_PERIOD, group=all, overwrite=True)

    hoomd.run(N_steps)

    pos = []
    fname = gsd.hoomd.open(f'./trajectory{RANDOM_SEED}.gsd')
    for i in range(int(N_steps / TRAJ_DUMP_PERIOD)):
        pos.append(fname.read_frame(i).particles.position)
    return pos

def get_distance_distribution(particles,A,B):
    import numpy as np
    particles = np.array(particles)
    dists = np.sqrt(np.sum((particles[:,A,:] - particles[:,B,:])**2,axis = 1))
    return dists