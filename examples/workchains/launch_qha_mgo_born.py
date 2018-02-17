from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()

from aiida.orm import CalculationFactory, DataFactory, WorkflowFactory
from aiida.work.run import run, submit
from aiida.orm.data.structure import StructureData
from aiida.orm.data.base import Str, Float, Bool, Int


KpointsData = DataFactory("array.kpoints")
ParameterData = DataFactory('parameter')


# Define structure

import numpy as np

cell = [[ 4.2119998932, 0,            0],
        [ 0.0,          4.2119998932, 0],
        [ 0.0,          0,           4.2119998932]]

structure = StructureData(cell=cell)

scaled_positions=[(0.0000000,  0.0000000,  0.0000000),
                  (0.0000000,  0.5000000,  0.5000000),
                  (0.5000000,  0.0000000,  0.5000000),
                  (0.5000000,  0.5000000,  0.0000000),
                  (0.5000000,  0.5000000,  0.5000000),
                  (0.5000000,  0.0000000,  0.0000000),
                  (0.0000000,  0.5000000,  0.0000000),
                  (0.0000000,  0.0000000,  0.5000000)]

symbols=['Mg', 'Mg', 'Mg', 'Mg', 'O', 'O', 'O', 'O']

positions = np.dot(scaled_positions, cell)

for i, scaled_position in enumerate(scaled_positions):
    structure.append_atom(position=np.dot(scaled_position, cell).tolist(),
                          symbols=symbols[i])

# Machine
machine_dict = {'resources': {'num_machines': 1,
                              'parallel_env': 'mpi*',
                              'tot_num_mpiprocs': 16},
                'max_wallclock_seconds': 3600 * 10,
                }

# PHONOPY settings
ph_settings = ParameterData(dict={'supercell': [[2, 0, 0],
                                                [0, 2, 0],
                                                [0, 0, 2]],
                                  'primitive': [[0.0, 0.5, 0.5],
                                                [0.5, 0.0, 0.5],
                                                [0.5, 0.5, 0.0]],
                                  'distance': 0.01,
                                  'mesh': [20, 20, 20],
                                  'symmetry_precision': 1e-5,
                                  # Uncomment the following lines to use phonopy remotely
                                  # 'code': 'phonopy_tot@boston_in', # this uses phonopy.force_constants plugin
                                  # 'machine': machine_dict
                                  })

# VASP SPECIFIC
incar_dict = {
    'NELMIN' : 5,
    'NELM'   : 100,
    'ENCUT'  : 400,
    'ALGO'   : 38,
    'ISMEAR' : 0,
    'SIGMA'  : 0.01,
    'GGA'    : 'PS'
}

settings_dict = {'code': {'optimize': 'vasp@stern',
                          'forces': 'vasp@stern',
                          'born_charges': 'vasp@stern'},
                 'parameters': incar_dict,
                 'kpoints_density': 0.5,  # k-point density,
                 'pseudos_family': 'pbe_test_family',
                 'family_folder': '/Users/abel/VASP/test_paw/',
                 'machine': machine_dict
                 }

es_settings = ParameterData(dict=settings_dict)

QHAPhonopy = WorkflowFactory('phonopy.qha')

# Chose how to run the calculation
run_by_deamon = False
if not run_by_deamon:
    result = run(QHAPhonopy,
                 structure=structure,
                 es_settings=es_settings,
                 ph_settings=ph_settings,
                 # Optional settings
                 num_expansions=Int(10),
                 use_nac=Bool(True),
                 )

    print (result)
else:
    future = submit(QHAPhonopy,
                    structure=structure,
                    es_settings=es_settings,
                    ph_settings=ph_settings,
                    # Optional settings
                    num_expansions=Int(10),
                    use_nac=Bool(True),
                    )

    print future
    print('Running workchain with pk={}'.format(future.pid))