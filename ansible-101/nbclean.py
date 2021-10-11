"""
Usage: python remove_output.py notebook.ipynb [ > without_output.ipynb ]
Modified from remove_output by Minrk

"""
import io
import os
import sys

from nbformat.current import read, write


def remove_outputs(nb):
    """remove the outputs from a notebook"""
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type == 'code':
                cell.outputs = []

if __name__ == '__main__':
    fname = sys.argv[1]
    with io.open(fname, 'r') as f:
        nb = read(f, 'json')
    remove_outputs(nb)
    base, ext = os.path.splitext(fname)
    new_ipynb = "%s_removed%s" % (base, ext)
    with io.open(new_ipynb, 'w', encoding='utf8') as f:
        write(nb, f, version=4)
    print "wrote %s" % new_ipynb
