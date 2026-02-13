from __future__ import annotations

import tkinter as tk
from typing import Optional


def rounded_rect(
    canvas: tk.Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    radius: int,
    fill: str,
    outline: str,
    width: int = 0,
    tag: str | None = None,
) -> Optional[int]:
    tags = (tag,) if tag else ()
    rect_id = canvas.create_rectangle(
        x1 + radius, y1, x2 - radius, y2, fill=fill, outline=fill, tags=tags
    )
    canvas.create_rectangle(
        x1, y1 + radius, x2, y2 - radius, fill=fill, outline=fill, tags=tags
    )

    canvas.create_arc(
        x1,
        y1,
        x1 + 2 * radius,
        y1 + 2 * radius,
        start=90,
        extent=90,
        style="pieslice",
        fill=fill,
        outline=fill,
        tags=tags,
    )
    canvas.create_arc(
        x2 - 2 * radius,
        y1,
        x2,
        y1 + 2 * radius,
        start=0,
        extent=90,
        style="pieslice",
        fill=fill,
        outline=fill,
        tags=tags,
    )
    canvas.create_arc(
        x2 - 2 * radius,
        y2 - 2 * radius,
        x2,
        y2,
        start=270,
        extent=90,
        style="pieslice",
        fill=fill,
        outline=fill,
        tags=tags,
    )
    canvas.create_arc(
        x1,
        y2 - 2 * radius,
        x1 + 2 * radius,
        y2,
        start=180,
        extent=90,
        style="pieslice",
        fill=fill,
        outline=fill,
        tags=tags,
    )

    if outline:
        canvas.create_arc(
            x1,
            y1,
            x1 + 2 * radius,
            y1 + 2 * radius,
            start=90,
            extent=90,
            style="arc",
            outline=outline,
            width=width,
            tags=tags,
        )
        canvas.create_arc(
            x2 - 2 * radius,
            y1,
            x2,
            y1 + 2 * radius,
            start=0,
            extent=90,
            style="arc",
            outline=outline,
            width=width,
            tags=tags,
        )
        canvas.create_arc(
            x2 - 2 * radius,
            y2 - 2 * radius,
            x2,
            y2,
            start=270,
            extent=90,
            style="arc",
            outline=outline,
            width=width,
            tags=tags,
        )
        canvas.create_arc(
            x1,
            y2 - 2 * radius,
            x1 + 2 * radius,
            y2,
            start=180,
            extent=90,
            style="arc",
            outline=outline,
            width=width,
            tags=tags,
        )
        canvas.create_line(
            x1 + radius, y1, x2 - radius, y1, fill=outline, width=width, tags=tags
        )
        canvas.create_line(
            x1 + radius, y2, x2 - radius, y2, fill=outline, width=width, tags=tags
        )
        canvas.create_line(
            x1, y1 + radius, x1, y2 - radius, fill=outline, width=width, tags=tags
        )
        canvas.create_line(
            x2, y1 + radius, x2, y2 - radius, fill=outline, width=width, tags=tags
        )

    return rect_id


def place_image(
    canvas: tk.Canvas,
    photo: Optional[tk.PhotoImage],
    x: int,
    y: int,
) -> Optional[int]:
    if photo is None:
        return None
    return canvas.create_image(x, y, image=photo, anchor="nw")
