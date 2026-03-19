import pytest
import json
import os
from ΞKernel import XiKernel

@pytest.fixture
def kernel():
    return XiKernel('test_library.json')

def test_init(kernel):
    assert os.path.exists(kernel.library_path)
    assert 'MetaLibrary' in kernel.library

def test_generate_triples(kernel):
    G, triples = kernel.generate_triples()
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 4
    assert len(triples) == 64
    spec = triples[0]
    assert 'Seed' in spec
    assert 'Mask' in spec
    assert 'Ritual' in spec
    assert 'TripleInterp' in spec

def test_triples_loop(tmp_path):
    lib_path = tmp_path / 'test_library.json'
    os.rename('Meta-Library.json', lib_path)
    kernel = XiKernel(str(lib_path))
    results = kernel.test_triples_loop(cycles=5)
    assert results['cycles'] == 5
    assert results['json_valid']
    assert results['new_seeds'] >= 0
    post_seeds = json.load(open(lib_path))['MetaLibrary']['Seeds']
    assert len(post_seeds) >= 10  # Growth possible
    assert 'convergence_delta' in json.load(open(lib_path))['ΞKernel']['State']['SymbolGraph']

def test_autopoiesis(tmp_path):
    lib_path = tmp_path / 'test_library.json'
    os.rename('Meta-Library.json', lib_path)
    kernel = XiKernel(str(lib_path))
    pre = len(kernel.library['MetaLibrary']['Seeds'])
    kernel.test_triples_loop(cycles=3)
    post = len(kernel.library['MetaLibrary']['Seeds'])
    assert post >= pre  # Autopoiesis

if __name__ == '__main__':
    pytest.main(['-v'])
