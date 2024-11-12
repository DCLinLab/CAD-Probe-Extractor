import ezdxf
from pathlib import Path
from probeinterface import Probe, write_probeinterface
from probeinterface.plotting import plot_probe
import numpy as np
import matplotlib.pyplot as plt


def get_polyline(doc, layer='New_CrAu'):
    ch = []
    x = []
    y = []
    modelspace = doc.modelspace()
    # Loop through each polyline and get the coordinates
    for entity in modelspace.query("LWPOLYLINE"):  # for lightweight polylines
        if entity.get_dxf_attrib('layer') == layer:
            if entity.has_xdata('PE_URL'):
                n = entity.get_xdata('PE_URL')[0].value
                if n.startswith('in'):
                    ch.append(n[2:])
                    x.append(entity[0][0])
                    y.append(entity[0][1])
    return ch, x, y


def make_kilosort_probe(ch, x, y, exclude=()):
    probe = {
        'chanMap': [],
        'xc': [],
        'yc': [],
        'kcoords': [],
        'n_chan': len(ch)
    }
    for a, b, c in zip(ch, x, y):
        a = int(a)
        if a in exclude:
            continue
        probe['chanMap'].append(a)
        probe['xc'].append(b)
        probe['yc'].append(c)
        probe['kcoords'].append(0)
    return probe


def make_probe(ch, x, y):
    probe = Probe(ndim=2, si_units='um')
    probe.set_contacts(positions=np.array([x, y]).T, shapes='circle')
    probe.set_device_channel_indices(ch)
    return probe


if __name__ == '__main__':
    indir = Path('input')
    outdir = Path('output')
    for i in indir.glob('*.dxf'):
        doc = ezdxf.readfile(i)
        temp = get_polyline(doc)
        probe = make_probe(*temp)
        write_probeinterface(outdir / i.with_suffix('.json').name, probe)
        # plot_probe(probe, with_device_index=True)
        # plt.show()