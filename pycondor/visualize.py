
from __future__ import division, print_function
import os
try:
    import graphviz
except ImportError:
    pass

from .job import Job


def dag_to_graphviz(dag):
    if not graphviz:
        raise ImportError('Visualizing Dagman graphs requires graphviz '
                          'to be installed.')
    from .dagman import Dagman
    if not isinstance(dag, Dagman):
        raise TypeError('Input must be a Dagman instance, '
                        'got {}'.format(type(dag)))
    graph_attr = {}
    graph_attr['rankdir'] = 'BT'

    g = graphviz.Digraph(graph_attr=graph_attr)

    for node in dag:
        shape = 'circle' if isinstance(node, Job) else 'square'
        g.node(node.name, node.name, shape=shape)
        for parent in node.parents:
            g.edge(parent.name, node.name)

    return g


def extract_format(filename):
    """Extract file format based on file extension

    Examples
    --------
    >>> filename = '/path/to/my_image.png'
    >>> extract_format(filename)
    png
    """
    _, ext = os.path.splitext(filename)
    fmt = ext[1:].lower()
    valid_formats = ('png', 'pdf', 'dot', 'svg', 'jpeg', 'jpg')
    if fmt not in valid_formats:
        raise ValueError('Invalid format {} entered. Must be one '
                         'of: {}'.format(fmt, valid_formats))
    return fmt


def visualize(dag, filename=None):
    """Visualize Dagman graph

    Parameters
    ----------
    dag : pycondor.Dagman
        Dagman to visualize.
    filename : str or None, optional
        File to save graph image to. If ``None`` then no file is saved.
        Valid file extensions are 'png', 'pdf', 'dot', 'svg', 'jpeg', 'jpg'.
    """
    g = dag_to_graphviz(dag)

    if filename is not None:
        fmt = extract_format(filename)
        data = g.pipe(format=fmt)
        with open(filename, 'wb') as f:
            f.write(data)

    return g
