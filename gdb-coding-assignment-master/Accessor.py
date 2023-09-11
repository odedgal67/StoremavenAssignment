from abc import ABC, abstractmethod
from typing import List

from FeaturedSong import FeaturedSong


class Accessor(ABC):
    @abstractmethod
    def is_invalid_category(self, category: str):
        pass

    @abstractmethod
    def get_playlists(self, category, country):
        pass

    @abstractmethod
    async def get_all_tracks_from_playlists(self, playlists) -> List[FeaturedSong]:
        pass
