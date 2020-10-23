# import qcware
from qiskit.providers import (BackendV1, Provider, JobStatus, Options)
from qiskit.providers.models import (BackendConfiguration)
from qiskit.result.models import (ExperimentResult, ExperimentResultData)
from qiskit.circuit import QuantumCircuit
from quasar import Circuit as QuasarCircuit
from quasar import ProbabilityHistogram as QuasarProbabilityHistogram
from quasar import CountHistogram as QuasarCountHistogram
from quasar import QuasarSimulatorBackend
from typing import Union, List
from uuid import uuid4
from .qcware_job import QcwareJob

# based in part on the documentation located at
# https://github.com/Qiskit/qiskit-tutorials/blob/master/legacy_tutorials/terra/6_creating_a_provider.ipynb
# and from the AQT backend, https://github.com/qiskit-community/qiskit-aqt-provider
# also look at https://github.com/Qiskit/qiskit-terra/blob/master/qiskit/providers/basicaer/qasm_simulator.py
# for example of local simulator backend

EVERY_JOB_ID = 42


class LocalQuasarBackend(BackendV1):
    """
    A qiskit wrapper backend for the qcware-quasar QuasarSimulator
    backend, providing a local simulator for testing and validation
    of circuit translation, etc.
    """
    def __init__(self, provider: Provider = None):
        configuration = {
            'backend_name': 'local_quasar_simulator',
            'backend_version': '0.0.0',
            'url': 'http://www.qcware.com',
            'simulator': True,
            'local': True,
            'coupling_map': None,
            'description':
            "Wrapper for the QuasarSimulator classical testing simulator",
            'basis_gates': ['h', 'x'],
            'memory': True,
            'n_qubits': 30,
            'conditional': False,
            'max_shots': 100000,
            'open_pulse': False,
            'gates': [{
                'name': 'TODO',
                'parameters': [],
                'qasm_def': 'TODO'
            }],
        }

        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(shots=1000)

    def _qiskit_circuit_to_quasar_circuit(self,
                                          c: QuantumCircuit) -> QuasarCircuit:
        result = Circuit()
        result.H(0).CX(0, 1)
        return result

    def _execute_quasar_circuit_measurement(
            self, c: QuasarCircuit) -> QuasarProbabilityHistogram:
        backend = QuasarSimulatorBackend()
        return backend.run_measurement(c)

    def _quasar_histogram_to_qiskit(
            self, h: QuasarProbabilityHistogram) -> ExperimentResult:
        count_histogram = h.to_count_histogram()
        # count histogram is a dict of integer representations of state to counts
        qiskit_counts = {hex(k): v for k, v in count_histogram.items()}
        experiment_data = ExperimentResultData(counts=qiskit_counts)
        experiment_result = ExperimentResult(
            shots=count_histogram.nmeasurement,
            success=True,
            data=experiment_data)
        # meas_level = MeasLevel.CLASSIFIED, meas_return = MeasLevel.AVERAGE ?
        # TODO must set jobj_id and job_id

    def experiment_result_from_circuit(c: QuasarCircuit) -> ExperimentResult:
        qh: QuasarHistogram = self._execute_quasar_circuit_measurement(c)
        er: ExperimentResult = self._quasar_histogram_to_qiskit(qh)
        return er

    def run(self, run_input: Union[QuantumCircuit, List[QuantumCircuit]],
            **options) -> QcwareJob:
        """
        Run a circuit or list of circuits

        Returns: QcwareJob
        """
        # the AQT backend submits the call here to get an ID.  This is also
        # duplicated in the AqtJob.submit
        # function
        # in qiskit.execute, you see blocks like
        #    start_time = time()
        #    job = backend.run(...)
        #    end_time = time()
        #
        # implying that run() should handle everything, so the use of
        # submit/cancel/status in job is mildly confusing.  They log
        # "submission time" so perhaps only submission is counted and
        # the job is used to look up the result in qasm_simulator,
        # this creates the job, assigns a uuid for the job id,
        # provides a call back function to actually run the job
        # (backend._run_job) and then "submits" it; the job class has
        # a process pool executor and it's the job that actually
        # executes the result.
        job: QcwareJob = QcwareJob(self, uuid4(), qobj=qobj)
        job._status = JobStatus.RUNNING
        # actually fill in the result here using a dummy circuit for now
        c: QuasarCircuit = QuasarCircuit()
        c.H(0).CX(0, 1)
        er = self.experiment_result_from_circuit(c)
        # currently only handling one circuit
        job._result = Result(
            backend_name=self._configuration.backend_name,
            backend_version=self._configuration.backend_version,
            qobj_id=None,
            job_id=job.job_id(),
            success=True,
            results=[er])
        job._status = JobStatus.DONE
        return job
