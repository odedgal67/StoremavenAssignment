from typing import Optional, List
from pydantic import BaseModel


class FeaturedSong(BaseModel):
    track_id: str
    track_name: str
    playlist_id: str
    playlist_name: str
    album_name: Optional[str]
    album_tracks: Optional[int]  # if this track is part of an album, this number represents how many tracks there are on the album
    artist_names: List[str]

    playlist_rank: int  # position of the playlist in the api results
    track_rank: int  # position of the track in the playlist
