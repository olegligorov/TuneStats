from dataclasses import dataclass, field

@dataclass(frozen=True)
class Track:
    name: str
    artist: str
    artist_id: str
    track_id: str
    image: str
    album_name: str
