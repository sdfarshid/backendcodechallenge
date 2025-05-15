from abc import ABC, abstractmethod
from typing import Dict, List


class FetcherAdapterInterface(ABC):

    @abstractmethod
    async def fetch(self, count: int, page:int) -> List[Dict]:
        pass


