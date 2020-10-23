"""
This is a qiskit provider for the QC Ware "Forge" product,
allowing evaluation of circuits on a local simulator or 
our hosted GPU-accelerated quantum simulators
"""

from .qcware_backend import LocalQuasarBackend
from .qcware_job import QcwareJob
from .version import __version__
