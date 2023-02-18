from dataclasses import dataclass, field

@dataclass(frozen=True)
class DetailedTrack:
    name: str
    artist: str
    artist_id: str
    track_id: str
    image: str
    album_name: str
    radio_chart: str
    audio_features: dict = field(default_factory=dict)