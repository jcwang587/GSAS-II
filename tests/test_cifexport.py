'''
test_cifexport.py
=================
Checks that a phase exported to CIF by GSASIIscriptable reads back in the
same setting: on rhombohedral axes where the phase is on rhombohedral axes,
on hexagonal axes where it is on hexagonal axes.
'''

import os
import sys
import tempfile

import importlib.util
G2loc = None
try:
    G2loc = importlib.util.find_spec('GSASII.GSASIIscriptable')
except ModuleNotFoundError:
    print('ModuleNotFound for GSASII.GSASIIscriptable')

if G2loc is None: # fixup path if GSASII not installed into Python
    print('GSAS-II not installed in Python; Hacking sys.path')
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import GSASII.GSASIIscriptable as G2sc

def test_rhombohedral_export():
    'A phase exported to CIF reads back on the axes it was exported on'
    work = tempfile.mkdtemp()
    gpx = G2sc.G2Project(newgpx=os.path.join(work, 'test_cifexport.gpx'))
    for name, spacegroup, cell, laue in (
            ('rhombohedral', 'R -3 m R', [5.0, 5.0, 5.0, 55.0, 55.0, 55.0], '3mR'),
            ('hexagonal', 'R -3 m', [2.9, 2.9, 14.2, 90.0, 90.0, 120.0], '3m1')):
        phase = gpx.add_phase(phasename=name, spacegroup=spacegroup, cell=cell)
        phase.add_atom(0.0, 0.0, 0.0, 'Ni', 'Ni1')
        ciffile = os.path.join(work, name + '.cif')
        phase.export_CIF(ciffile)
        reread = gpx.add_phase(ciffile, phasename=name + '_reread', fmthint='CIF')
        SGData = reread.data['General']['SGData']
        assert SGData['SGLaue'] == laue, f"{name} phase read back as {SGData['SpGrp']}"

if __name__ == '__main__':
    test_rhombohedral_export()
    print('OK')
