import os
import re

import pytest

from pycondor.job import Job
from pycondor.dagman import Dagman
from pycondor.visualize import visualize, extract_format, dag_to_graphviz
from pycondor.utils import clear_pycondor_environment_variables

graphviz = pytest.importorskip('graphviz')  # noqa: E402

clear_pycondor_environment_variables()

here = os.path.abspath(os.path.dirname(__file__))
example_script = os.path.join(here, 'example_script.py')


@pytest.fixture()
def dagman(tmpdir_factory):
    dag = Dagman(name='example_dagman')

    merge = Job(name='merge',
                executable='merge.py',
                dag=dag)

    for i in range(5):
        processing = Job(name='processing_{}'.format(i),
                         executable='process.py',
                         dag=dag)
        merge.add_parent(processing)

    cleanup_dag = Dagman(name='cleanup',
                         dag=dag)
    cleanup_dag.add_parent(merge)
    return dag


def test_visualize_save_file(dagman, tmpdir):
    filename = str(tmpdir.join('viz.png'))
    visualize(dagman, filename)
    assert os.path.exists(filename)


@pytest.mark.parametrize('filename, expected', [
    ('myfile.png', 'png'),
    ('myfile.pdf', 'pdf'),
    ('myfile.dot', 'dot'),
    ('myfile.svg', 'svg'),
    ('myfile.jpeg', 'jpeg'),
    ('myfile.jpg', 'jpg'),
])
def test_extract_format(filename, expected):
    assert extract_format(filename) == expected


def test_extract_format_invalid_format(dagman):
    with pytest.raises(ValueError) as excinfo:
        extract_format('dag_graph.csv')
    assert 'invalid format' in str(excinfo.value).lower()


def test_dag_to_graphviz(dagman):
    g = dag_to_graphviz(dagman)
    assert isinstance(g, graphviz.Digraph)


def test_graph_shapes(dagman):
    g = dag_to_graphviz(dagman)

    shapes = {}
    label_shape_re = re.compile(r'.*\[label=(.*?) shape=(.*?)\]')
    for line in g.body:
        match = label_shape_re.match(line)
        if match:
            name = match.group(1)
            shape = match.group(2)
            shapes[name] = shape
        else:
            continue

    # Check node names
    assert set(node.name for node in dagman) == set(shapes.keys())
    # Check node shapes
    for node in dagman:
        expected_shape = 'circle' if isinstance(node, Job) else 'square'
        assert shapes[node.name] == expected_shape


def test_visualize_method(dagman):
    graph_vis_func = visualize(dagman).body
    graph_vis_method = dagman.visualize().body
    assert graph_vis_func == graph_vis_method
