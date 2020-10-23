from qiskit.providers import Options
from qiskit.circuit import QuantumCircuit as QiskitCircuit
from qiskit.result.models import (ExperimentResult, ExperimentResultData)
from quasar import Circuit as QuasarCircuit
from quasar import Backend as QuasarBackend
from quasar import ProbabilityHistogram as QuasarProbabilityHistogram
from qusetta import Qiskit as qusetta_qiskit
from qusetta import Quasar as qusetta_quasar
from typing import List, Dict

QusettaCircuit = List[str]

def quasar_circuit_from_qiskit(c: QiskitCircuit)->QuasarCircuit:
    return qusetta_quasar.from_qusetta(qusetta_qiskit.to_qusetta(c))

def qiskit_experiment_result_from_quasar_probability_histogram(
        h: QuasarProbabilityHistogram) -> ExperimentResult:
    count_histogram = h.to_count_histogram()
    # count histogram is a dict of integer representations of state to counts
    qiskit_counts: Dict[str,int] = {hex(k): v for k, v in count_histogram.items()}
    experiment_data = ExperimentResultData(counts=qiskit_counts)
    experiment_result = ExperimentResult(
        shots=count_histogram.nmeasurement,
        success=True,
        data=experiment_data)
    # meas_level = MeasLevel.CLASSIFIED, meas_return = MeasLevel.AVERAGE ?
    # TODO must set jobj_id and job_id
    return experiment_result

def measurement_result_from_qiskit_circuit(qiskit_circuit: QiskitCircuit, options: Options, backend: QuasarBackend, )->ExperimentResult:
    quasar_circuit: QuasarCircuit = quasar_circuit_from_qiskit(qiskit_circuit)
    probability_histogram: QuasarProbabilityHistogram = backend.run_measurement(quasar_circuit, nmeasurement=options.shots)
    result: ExperimentResult = qiskit_experiment_result_from_quasar_probability_histogram(probability_histogram)
    return result
    
