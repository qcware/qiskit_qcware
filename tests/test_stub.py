from qiskit_qcware import LocalQuasarBackend, QcwareProvider
from qiskit import execute, QuantumCircuit, QuantumRegister, ClassicalRegister


def test_stub():
    qreg=QuantumRegister(2)
    creg=ClassicalRegister(2)
    qc: QuantumCircuit = QuantumCircuit(qreg, creg)
    qc.h(qreg[0])
    qc.cx(qreg[0], qreg[1])
    # qc.measure(qreg, creg)

    provider = QcwareProvider()
    stub_job = execute(qc, backend=provider.get_backend('local_quasar_simulator'), shots=100)
    print(stub_job.result())
    assert(False)
