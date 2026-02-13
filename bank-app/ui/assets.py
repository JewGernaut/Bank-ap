from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageOps, ImageTk
except ImportError:  # pragma: no cover - runtime dependency check
    Image = None
    ImageOps = None
    ImageTk = None


class AssetLoader:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.images: dict[str, ImageTk.PhotoImage] = {}

    def can_load(self) -> bool:
        return Image is not None and ImageTk is not None and ImageOps is not None

    def load_image(
        self,
        key: str,
        filename: str,
        width: int,
        height: int,
        fill: bool = False,
    ) -> Optional[ImageTk.PhotoImage]:
        if not self.can_load():
            return None

        path = self.base_dir / filename
        if not path.exists():
            return None

        image = Image.open(path)
        if fill:
            image = ImageOps.fit(image, (width, height), method=Image.LANCZOS)
        else:
            image = image.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.images[key] = photo
        return photo
