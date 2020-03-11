#todo: TABULATED POTENTIAL!

def run_simulation(N_steps = 1e6, 
                   positions = [[0,0,0],[1,0,0]], 
                   bonds = [[0,1]],
                   lengths = [[1,1]]):
    import gsd.hoomd
    import hoomd
    import hoomd.md
    hoomd.context.initialize("")
    
    snapshot = hoomd.data.make_snapshot(N=len(positions),
                                        box = hoomd.data.boxdim(Lx=200, Ly=200,Lz = 200),
                                        particle_types = ['A'],
                                        bond_types=['dna']
                                       )

    snapshot.particles.position[:] = positions
    snapshot.particles.typeid[:] = 0
    snapshot.bonds.resize(len(bonds))
    snapshot.bonds.group[:] = bonds
    
    hoomd.init.read_snapshot(snapshot)

    nl = hoomd.md.nlist.tree()
    
    lj = hoomd.md.pair.lj(r_cut=2.5, nlist=nl)
    lj.pair_coeff.set('A','A',epsilon = 0.000,sigma = 0.01)

    
    harmonic = hoomd.md.bond.harmonic()
    harmonic.bond_coeff.set('dna', k=100.0, r0=1); # sort this out.
    




    hoomd.md.integrate.mode_standard(dt=0.002)
    all = hoomd.group.all()
    hoomd.md.integrate.langevin(group=all, kT=0.2, seed=42)
    
    hoomd.md.update.zero_momentum(period = 4)
    
    hoomd.analyze.log(filename="log-output.log",
                  quantities=['potential_energy', 'temperature'],
                  period=100,
                  overwrite=True)

    hoomd.dump.gsd("trajectory.gsd", period=2e3, group=all, overwrite=True)
    hoomd.run(N_steps)

    pos = []
    fname = gsd.hoomd.open('./trajectory.gsd')
    for i in range(int(N_steps / 2e3)):
        pos.append(fname.read_frame(i).particles.position)
    return pos

def get_distance_distribution(particles,A,B):
    import numpy as np
    particles = np.array(particles)
    dists = np.sqrt(np.sum((particles[:,A,:] - particles[:,B,:])**2,axis = 1))
    return dists