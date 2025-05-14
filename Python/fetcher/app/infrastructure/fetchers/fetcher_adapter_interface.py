from abc import ABC, abstractmethod
from typing import Dict, List


class FetcherAdapterInterface(ABC):

    @abstractmethod
    def fetch(self, count: int) -> List[Dict]:
        pass


