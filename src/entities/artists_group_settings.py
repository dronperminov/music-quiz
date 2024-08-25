from dataclasses import dataclass


@dataclass
class ArtistsGroupSettings:
    max_variants: int

    def to_dict(self) -> dict:
        return {
            "max_variants": self.max_variants
        }

    @classmethod
    def from_dict(cls: "ArtistsGroupSettings", data: dict) -> "ArtistsGroupSettings":
        return cls(
            max_variants=data["max_variants"]
        )

    @classmethod
    def default(cls: "ArtistsGroupSettings") -> "ArtistsGroupSettings":
        return cls(max_variants=4)
