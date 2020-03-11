def run_simulation(N_steps = 1e7, positions = [[0,0,0],[1,0,0]], bonds = [[0,1]]):

    import hoomd
    import hoomd.md
    hoomd.context.initialize("")
    
    snapshot = hoomd.data.make_snapshot(N=len(positions),
                                        box = hoomd.data.boxdim(Lx=50, Ly=50,Lz = 50),
                                        particle_types = ['A'],
                                        bond_types=['dna']
                                       )
    #need to get automated positions...
    snapshot.particles.position[:] = positions
    
    snapshot.particles.typeid[:] = 0
    
    snapshot.bonds.resize(len(bonds))
    snapshot.bonds.group[:] = bonds
    
    hoomd.init.read_snapshot(snapshot)
    
    nl = hoomd.md.nlist.tree()
    
    lj = hoomd.md.pair.lj(r_cut=2.5, nlist=nl)
    lj.pair_coeff.set('A','A',epsilon = 0.001,sigma = 0.01)
    
    harmonic = hoomd.md.bond.harmonic()
    harmonic.bond_coeff.set('dna', k=100.0, r0=1); # sort this out.
    
    hoomd.md.integrate.mode_standard(dt=0.005)
    all = hoomd.group.all()
    hoomd.md.integrate.langevin(group=all, kT=0.2, seed=42)
    
    hoomd.md.update.zero_momentum(period = 4)
    
    hoomd.analyze.log(filename="log-output.log",
                  quantities=['potential_energy', 'temperature'],
                  period=100,
                  overwrite=True)

    hoomd.dump.gsd("trajectory.gsd", period=2e3, group=all, overwrite=True)
    hoomd.run(N_steps)


run_simulation()