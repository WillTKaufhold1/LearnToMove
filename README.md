# LearnToMove

## Objective 

Propose candidate monomers for auxetic materials, to be built with DNA. 

Idea is to use wireframe DNA origami to create precise patten of struts and joins, which are synthesized bottom up. 

Workflow is:

Design monomers using LearnToMove -> validate simulation of monomers using MRDNA / oxDNA -> Build monomers at Carlos's lab -> Assemble materials back at Imperial.

## LearnToMove Model

The objective of the model is to provide the simplest possible description of wireframe DNA origami that captures mechanical properties. Finite element analysis / nucleotide level descriptions are too computaionally intensive to be useful evaluation steps in optimization. 

One alternative is to describe the system as a set of edges which represent single helices, and a set of nodes, which represent junctions between helices. The junctions can be represented as beads, with a tabulated potential between adjacent nodes which encodes the repulsive effect of the double helix.


## Implementation 

Implementation of the evaluator is in GPU accelerate HOOMD-BLUE. Implementation of the optimizer is in Python3.

I may end up transitioning to a very coarse MRDNA representation if excluded volume ends up being important. But I think the HOOMD blue representation is fairly flexible, and makes sense a s a first attempt...

### Units 

Fundamental units in HOOMD-BLUE are distance / energy / mass.

Here, the specific units we use are: ...

### Parameters

NORMAL MODES?

### Evaluation

For intra-node repulsion, a tabulated bond is used. The tabulated bond we use initially is a Gaussian, although this is for convenience, and realistically, we'll probably end up using something much closer to an empirically derived potential.


### State space 

Genotype - phenotype map?

### Optimization





