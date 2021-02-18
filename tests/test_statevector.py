from qiskit_qcware import QcwareProvider
import qiskit
import numpy
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_statevector():
    qc: qiskit.QuantumCircuit = qiskit.QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    # addition of a measure gate "locks" the bit in qiskit-aer's
    # statevector simulator such that
    # the statevector measured after that has that bit "locked".
    # This is not how quasar works, so we will focus on gates without
    # measurements
    provider = QcwareProvider()
    sv1 = qiskit.execute(qc, backend=provider.get_backend(
        'local_statevector')).result().data()['statevector']
    aer_backend = qiskit.Aer.get_backend('statevector_simulator')
    sv2 = qiskit.execute(qc, aer_backend).result().data()['statevector']
    assert (numpy.allclose(sv1, sv2))
