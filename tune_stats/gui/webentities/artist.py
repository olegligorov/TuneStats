from dataclasses import dataclass, field

@dataclass(frozen=True)
class ArtistModel:
    name: str
    id: str
    spotify_url: str
    genres: tuple[str] = field(default_factory=tuple)

    image: str = field(default="")
