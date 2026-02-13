from __future__ import annotations

import tkinter as tk
from typing import Callable

from .draw import rounded_rect
from .layout import Colors, Fonts


class MenuWindow(tk.Toplevel):
    def __init__(
        self,
        master: tk.Misc,
        colors: Colors,
        fonts: Fonts,
        on_profile: Callable[[], None],
        on_settings: Callable[[], None],
        on_security: Callable[[], None],
        on_support: Callable[[], None],
        on_logout: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self.colors = colors
        self.fonts = fonts
        self._accent_hover = "#331772"

        self.title("Меню")
        self.geometry("360x390")
        self.resizable(False, False)
        self.configure(bg=self.colors.content)
        self.transient(master)
        self.grab_set()

        self._build_ui(
            on_profile=on_profile,
            on_settings=on_settings,
            on_security=on_security,
            on_support=on_support,
            on_logout=on_logout,
        )
        self._center_over_master(master)

    def _build_ui(
        self,
        on_profile: Callable[[], None],
        on_settings: Callable[[], None],
        on_security: Callable[[], None],
        on_support: Callable[[], None],
        on_logout: Callable[[], None],
    ) -> None:
        header = tk.Frame(self, bg=self.colors.header, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="МЕНЮ",
            bg=self.colors.header,
            fg=self.colors.text_light,
            font=self.fonts.title,
        ).pack(pady=16)

        body = tk.Frame(self, bg=self.colors.content)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        self._menu_button(body, "ПРОФИЛЬ", on_profile).pack(fill="x", pady=(0, 10))
        self._menu_button(body, "НАСТРОЙКИ", on_settings).pack(fill="x", pady=(0, 10))
        self._menu_button(body, "БЕЗОПАСНОСТЬ", on_security).pack(fill="x", pady=(0, 10))
        self._menu_button(body, "ПОДДЕРЖКА", on_support).pack(fill="x", pady=(0, 10))
        self._menu_button(body, "ВЫХОД", on_logout).pack(fill="x")

    def _menu_button(self, parent: tk.Misc, text: str, command: Callable[[], None]) -> tk.Canvas:
        button = tk.Canvas(
            parent,
            bg=self.colors.content,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            height=52,
        )

        hover = {"active": False}

        def redraw(_event: tk.Event | None = None) -> None:
            button.delete("btn")
            width = max(button.winfo_width(), 2)
            height = max(button.winfo_height(), 2)
            fill = self._accent_hover if hover["active"] else self.colors.accent
            rounded_rect(
                button,
                1,
                1,
                width - 1,
                height - 1,
                radius=12,
                fill=fill,
                outline="",
                tag="btn",
            )
            button.create_text(
                width // 2,
                height // 2,
                text=text,
                fill=self.colors.text_light,
                font=self.fonts.small,
                tags=("btn",),
            )

        def on_click(_event: tk.Event) -> None:
            command()

        def on_enter(_event: tk.Event) -> None:
            hover["active"] = True
            redraw()

        def on_leave(_event: tk.Event) -> None:
            hover["active"] = False
            redraw()

        button.bind("<Configure>", redraw)
        button.bind("<Button-1>", on_click)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    def _center_over_master(self, master: tk.Misc) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_w = master.winfo_width()
        master_h = master.winfo_height()

        x = master_x + (master_w - width) // 2
        y = master_y + (master_h - height) // 2
        self.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")
