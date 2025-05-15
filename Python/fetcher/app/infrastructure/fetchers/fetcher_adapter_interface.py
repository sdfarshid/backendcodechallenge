from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class FetcherAdapterInterface(ABC):

    @property
    @abstractmethod
    def default_per_page(self) -> Optional[int]:
        pass


    @abstractmethod
    async def fetch(self, count: int, page:int) -> List[Dict]:
        pass


