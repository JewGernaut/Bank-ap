from __future__ import annotations

import tkinter as tk
from typing import Callable

from .draw import rounded_rect
from .layout import Colors, Fonts


class RegistrationWindow(tk.Toplevel):
    def __init__(
        self,
        master: tk.Misc,
        colors: Colors,
        fonts: Fonts,
        on_submit: Callable[[dict[str, str]], bool],
    ) -> None:
        super().__init__(master)
        self.colors = colors
        self.fonts = fonts
        self.on_submit = on_submit
        self._accent_hover = "#331772"

        self.title("Регистрация")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(bg=self.colors.content)
        self.transient(master)
        self.grab_set()

        self._entries: dict[str, tk.Entry] = {}
        self._build_ui()
        self._center_over_master(master)
        self._entries["login"].focus_set()

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=self.colors.header, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ",
            bg=self.colors.header,
            fg=self.colors.text_light,
            font=self.fonts.subtitle,
        ).pack(pady=18)

        body = tk.Frame(self, bg=self.colors.content)
        body.pack(fill="both", expand=True, padx=28, pady=20)

        fields = [
            ("login", "Логин"),
            ("first_name", "Имя"),
            ("last_name", "Фамилия"),
            ("password", "Пароль"),
        ]

        for idx, (name, title) in enumerate(fields):
            tk.Label(
                body,
                text=title,
                bg=self.colors.content,
                fg=self.colors.text_dark,
                font=self.fonts.small,
                anchor="w",
            ).grid(row=idx * 2, column=0, sticky="w", pady=(0, 4))

            show = "•" if name == "password" else ""
            entry = tk.Entry(
                body,
                bg=self.colors.input,
                fg=self.colors.input_text,
                font=self.fonts.small,
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.colors.accent,
                highlightcolor=self.colors.accent,
                show=show,
            )
            entry.grid(row=idx * 2 + 1, column=0, sticky="ew", pady=(0, 12), ipady=8)
            self._entries[name] = entry

        body.grid_columnconfigure(0, weight=1)

        actions = tk.Frame(self, bg=self.colors.content)
        actions.pack(fill="x", padx=28, pady=(0, 22))

        self._action_button(
            actions,
            text="ЗАРЕГИСТРИРОВАТЬСЯ",
            command=self._handle_submit,
        ).pack(fill="x")

    def _action_button(
        self, parent: tk.Misc, text: str, command: Callable[[], None]
    ) -> tk.Canvas:
        button = tk.Canvas(
            parent,
            bg=self.colors.content,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            height=54,
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

    def _handle_submit(self) -> None:
        data = {key: entry.get() for key, entry in self._entries.items()}
        self.on_submit(data)

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
