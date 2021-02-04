from qiskit_qcware.conversions import remap_histogram_key
import pytest

@pytest.mark.parametrize("val,bit_map,expected", [(5, {0: 0, 2: 1}, 3)])
def test_remap_histogram_key(val, bit_map, expected):
    assert remap_histogram_key(val, bit_map) == expected
