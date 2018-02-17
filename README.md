# This is a personal fork of Abel's AiiDA Phonopy plugin
The master branch in my repository is developed on the basis 
of 'development' branch of Dr. Abel Carreras Conill's
 [aiida-phonopy](https://github.com/abelcarreras/aiida-phonopy),
  a copy of his 'development' branch is also included in this repository
  with the same branch name. 




# Below is Abel's original READEME

AiiDA Phonopy plugin
====================

This a phonopy plugin for AiiDA. This plugin includes workflows to calculate
phonon band structure, DOS, thermal properties and mode Gruneisen parameters.
It provides interfaces for VASP, Quantum ESPRESSO and LAMMPS to calculate the 
atomic forces and relax the crystal structure. 


Examples
--------
Some test calculations are found in the folder **/examples**

- plugins: examples of basic functionality of phonopy remote plugin. These tests require 
the previous calculation of forces or force constants that should be already stored in the database
- workchains: examples of the full phonon calculation / gruneisen parameters from scratch. These workflows
require the installation of plugins for VASP, LAMMPS or QuantumESPRESSO.
- tools: example scripts for visualize the results of phonon/gruneisen workchains. These scripts require
 matplotlib.
