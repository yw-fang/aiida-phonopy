# Calculate DOS Band structure and thermal properties
# Additionally if DATA_SETS (forces) are used force constants are also calculated
from aiida import load_dbenv
load_dbenv()

from aiida.orm import Code, DataFactory, load_node
StructureData = DataFactory('structure')
ParameterData = DataFactory('parameter')

import numpy as np
import os

codename = 'phonopy_tot@boston_in'
code = Code.get_from_string(codename)

cell = [[ 3.1900000572, 0,           0],
        [-1.5950000286, 2.762621076, 0],
        [ 0.0,          0,           5.1890001297]]

scaled_positions=[(0.6666669,  0.3333334,  0.0000000),
                  (0.3333331,  0.6666663,  0.5000000),
                  (0.6666669,  0.3333334,  0.3750000),
                  (0.3333331,  0.6666663,  0.8750000)]

symbols=['Ga', 'Ga', 'N', 'N']

structure = StructureData(cell=cell)

for i, scaled_position in enumerate(scaled_positions):
    structure.append_atom(position=np.dot(scaled_position, cell).tolist(),
                          symbols=symbols[i])

parameters = ParameterData(dict={'supercell': [[2, 0, 0],
                                               [0, 2, 0],
                                               [0, 0, 2]],
                                 'primitive': [[1.0, 0.0, 0.0],
                                               [0.0, 1.0, 0.0],
                                               [0.0, 0.0, 1.0]],
                                 'distance': 0.01,
                                 'mesh': [40, 40, 40],
                                 'symmetry_precision': 1e-5}
                          )

calc = code.new_calc(max_wallclock_seconds=3600,
                     resources={"num_machines": 1,
                                "parallel_env":"mpi*",
                                "tot_num_mpiprocs": 6})

calc.label = "test phonopy calculation"
calc.description = "A much longer description"

calc.use_structure(structure)
calc.use_code(code)
calc.use_parameters(parameters)

# Chose to use forces or force constants
if True:
    calc.use_data_sets(load_node(46680))  # This node should contain a ForceSetsData object
else:
    calc.use_force_constants(load_node(46683))  # This node should contain a ForceConstantsData object


# Set bands (optional)
from aiida_phonopy.workchains.phonon import get_primitive, get_path_using_seekpath
primitive = get_primitive(structure, parameters)['primitive_structure']
bands = get_path_using_seekpath(primitive, band_resolution=30)
calc.use_bands(bands)

if False:
    subfolder, script_filename = calc.submit_test()
    print "Test_submit for calculation (uuid='{}')".format(calc.uuid)
    print "Submit file in {}".format(os.path.join(
        os.path.relpath(subfolder.abspath),
        script_filename))
else:
    calc.store_all()
    print "created calculation with PK={}".format(calc.pk)
    calc.submit()