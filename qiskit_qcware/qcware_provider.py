from qiskit.providers import ProviderV1, Backend
from qiskit.providers.providerutils import filter_backends
from .qcware_backend import LocalQuasarMeasurementBackend, LocalQuasarStatevectorBackend
from typing import List


class QcwareProvider(ProviderV1):
    def __init__(self):
        self._backends = [LocalQuasarMeasurementBackend(provider=self),
                          LocalQuasarStatevectorBackend(provider=self)]

    def backends(self, name: str = None, **kwargs) -> List[Backend]:
        """
        Returns a list of backends matching the specified filtering.
        """
        backends = self._backends if name is None else [
            backend for backend in self._backends if backend.name() == name
        ]
        return filter_backends(backends, filters=None, **kwargs)
