Examples of Use
===============

Getting started with the QCWare Qiskit provider is straightforward;
just create your circuits as usual with qiskit and then use
the QCWare provider to create a backend of your choice.::

  >>>import qiskit
  >>>from qiskit_qcware import QcwareProvider

  >>>c = qiskit.QuantumCircuit(2)
  >>>c.h(0)
  >>>c.cx(0,1)

With the circuit created, you can execute it just as you would in Aer::

  >>>qiskit.execute(c, qiskit.Aer.get_backend('statevector_simulator')).result().data()['statevector']
  array([0.70710678+0.j, 0.        +0.j, 0.        +0.j, 0.70710678+0.j])

  >>>c2 = c.copy()
  >>>c2.measure_all()
  >>>qiskit.execute(c2, qiskit.Aer.get_backend('qasm_simulator')).result().data()
  {'counts': {'0x0': 527, '0x3': 497}}

For statevectors, replace `statevector_simulator` with a QCWare statevector simulator name
(such as `local_statevector`) and for measurements with a QCWare measurement-enabled
backend (such as `local_measurement`)::

  >>> qiskit.execute(c, QcwareProvider().get_backend('local_statevector')).result().data()['statevector']
  array([0.70710678+0.j, 0.        +0.j, 0.        +0.j, 0.70710678+0.j])
  >>> qiskit.execute(c2, QcwareProvider().get_backend('local_measurement')).result().data()['counts']
  {'0x0': 561, '0x3': 463}
