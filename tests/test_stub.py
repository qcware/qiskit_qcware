from qiskit_qcware import QcwareProvider
import qiskit
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def test_circuit():
    qc: qiskit.QuantumCircuit = qiskit.QuantumCircuit(2, 2)
    qc.x(0)
    qc.id(1)
    qc.measure(1, 0)
    qc.measure(0, 1)
    return qc


def test_stub():
    qc = test_circuit()
    provider = QcwareProvider()
    backend = provider.get_backend('local_measurement')
    # backend.forge_backend = 'qcware/gpu_simulator'
    qcware_counts = qiskit.execute(
        qc, backend=provider.get_backend('forge_measurement'),
        shots=100).result().data()['counts']
    aer_backend = qiskit.Aer.get_backend('qasm_simulator')
    aer_counts = qiskit.execute(qc, aer_backend,
                                shots=100).result().data()['counts']
    # results should have the same keys
    assert set(qcware_counts.keys()) == set(aer_counts.keys())
