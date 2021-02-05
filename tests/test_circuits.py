from qcware_transpile.dialects import qiskit as qiskit_dialect
from qcware_transpile.translations.qiskit.to_quasar import (
    translation_set, native_is_translatable)  # type: ignore
from .strategies.qiskit import gates, circuits  # type: ignore
from qiskit_qcware import QcwareProvider
import quasar
import qiskit
from hypothesis import given, settings, note, assume
import numpy

ts = translation_set()
translatable_gatedefs = [
    x for x in qiskit_dialect.dialect().gate_defs if x.name not in {}
]
translatable_circuits = circuits(1, 3, 1, 4,
                                 gates(gate_list=translatable_gatedefs))


def qcware_probability_vector(circuit: quasar.Circuit):
    backend = QcwareProvider().get_backend('local_statevector')
    sv = qiskit.execute(circuit, backend).result().data()['statevector']
    return abs(sv)


def aer_probability_vector(circuit: qiskit.QuantumCircuit):
    backend = qiskit.Aer.get_backend('statevector_simulator')
    sv = qiskit.execute(circuit, backend).result().data()['statevector']
    return abs(sv)


@given(translatable_circuits)
@settings(deadline=None)
def test_qiskit_qcware(qiskit_circuit):
    assume(native_is_translatable(qiskit_circuit))
    note(qiskit_circuit.draw())
    pv_qcware = qcware_probability_vector(qiskit_circuit)
    pv_aer = aer_probability_vector(qiskit_circuit)
    assert (numpy.allclose(pv_aer, pv_qcware, atol=0.0000001))
