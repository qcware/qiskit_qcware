# import qcware
from qiskit.providers import (BackendV1, Provider, JobStatus, Options)
from qiskit.providers.models import (BackendConfiguration)
from qiskit.result import Result
from qiskit.circuit import QuantumCircuit
from quasar import QuasarSimulatorBackend
from typing import Union, List
from uuid import uuid4
from .qcware_job import QcwareJob
from .conversions import (measurement_result_from_qiskit_circuit,
                          statevector_result_from_qiskit_circuit)
from qcware_transpile.translations.qiskit.to_quasar import basis_gates # type: ignore

# based in part on the documentation located at
# https://github.com/Qiskit/qiskit-tutorials/blob/master/legacy_tutorials/terra/6_creating_a_provider.ipynb
# and from the AQT backend, https://github.com/qiskit-community/qiskit-aqt-provider
# also look at https://github.com/Qiskit/qiskit-terra/blob/master/qiskit/providers/basicaer/qasm_simulator.py
# for example of local simulator backend

EVERY_JOB_ID = 42


class LocalQuasarMeasurementBackend(BackendV1):
    """
    A qiskit wrapper backend for the qcware-quasar QuasarSimulator
    backend, providing a local simulator for testing and validation
    of circuit translation, etc.
    """
    def __init__(self, provider: Provider = None):
        configuration = {
            'backend_name': 'local_measurement',
            'backend_version': '0.0.0',
            'url': 'http://www.qcware.com',
            'simulator': True,
            'local': True,
            'coupling_map': None,
            'description':
            "Wrapper for the QuasarSimulator classical testing simulator",
            'basis_gates': basis_gates(),
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
        # merge options with self.options
        job_options = self.options
        job_options.update_options(**options)

        job: QcwareJob = QcwareJob(self, str(uuid4()))
        job._status = JobStatus.RUNNING

        if isinstance(run_input, QuantumCircuit):
            run_input = [run_input]
        experiment_results = [
            measurement_result_from_qiskit_circuit(c, job_options,
                                                   QuasarSimulatorBackend())
            for c in run_input
        ]
        # currently only handling one circuit
        job._result = Result(
            backend_name=self._configuration.backend_name,
            backend_version=self._configuration.backend_version,
            qobj_id=None,
            job_id=job.job_id(),
            success=True,
            results=experiment_results)
        job._status = JobStatus.DONE
        return job


class LocalQuasarStatevectorBackend(BackendV1):
    """
    A qiskit wrapper backend for the qcware-quasar QuasarSimulator
    backend, providing a local simulator for testing and validation
    of circuit translation, etc.
    """
    def __init__(self, provider: Provider = None):
        configuration = {
            'backend_name': 'local_statevector',
            'backend_version': '0.0.0',
            'url': 'http://www.qcware.com',
            'simulator': True,
            'local': True,
            'coupling_map': None,
            'description':
            "Wrapper for the QuasarSimulator classical testing simulator",
            'basis_gates': basis_gates(),
            'memory': True,
            'n_qubits': 30,
            'conditional': False,
            'max_shots': 1,
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
        return Options(shots=1)

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
        # merge options with self.options
        job_options = self.options
        job_options.update_options(**options)

        job: QcwareJob = QcwareJob(self, str(uuid4()))
        job._status = JobStatus.RUNNING

        if isinstance(run_input, QuantumCircuit):
            run_input = [run_input]
        experiment_results = [
            statevector_result_from_qiskit_circuit(c, job_options,
                                                   QuasarSimulatorBackend())
            for c in run_input
        ]
        # currently only handling one circuit
        job._result = Result(
            backend_name=self._configuration.backend_name,
            backend_version=self._configuration.backend_version,
            qobj_id=None,
            job_id=job.job_id(),
            success=True,
            results=experiment_results)
        job._status = JobStatus.DONE
        return job
