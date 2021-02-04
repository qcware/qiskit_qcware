Caveats
=======

Since Quasar (the underlying circuit-model manipulation library
used by QCWare) has some different assumptions from Qiskit, there
are a few subtle gotchas.

Because qiskit transpiles circuits to the set of basis gates supported
by quasar, it may introduce a global phase into the mix.  As a result,
while measurements will behave normally, there is a chance that the
statevector produced by a qiskit circuit run on Aer will be different
from that produced by the same circuit run on a QCWare simulator.
The probabilities for measurement should be the same (and this is checked
in the automated test suite for the translation layer).

Because QCWare's Quasar simulators are pure statevector simulators,
the circuit is run to completion and _then_ measurements are made from
the final statevector.  As a result, mid-circuit measurements _may_ not
result in expected outcomes, and the mechanism that a measurement prior
to the final statevector will "fix" bits is not supported.

As a result, we strongly recommend against running mid-circuit measurements,
although any measurement gates will be ignored by the statevector backends
(so it is safe to ask for a statevector from a circuit with measurements).

