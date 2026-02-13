from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Callable

from .assets import AssetLoader
from .draw import place_image, rounded_rect


@dataclass(frozen=True)
class Colors:
    header: str
    left: str
    content: str
    accent: str
    text_light: str
    text_dark: str
    white: str
    input: str
    input_text: str


@dataclass(frozen=True)
class Fonts:
    title: tuple
    subtitle: tuple
    label: tuple
    medium: tuple
    small: tuple


class Layout:
    def __init__(
        self,
        canvas: tk.Canvas,
        colors: Colors,
        fonts: Fonts,
        assets: AssetLoader,
        on_adv_click: Callable[[tk.Event], None],
        on_help: Callable[[], None],
        on_menu: Callable[[], None],
        on_login: Callable[[], None],
        on_register: Callable[[], None],
        on_transfer: Callable[[], None],
        on_remember_toggle: Callable[[], None],
    ) -> None:
        self.canvas = canvas
        self.colors = colors
        self.fonts = fonts
        self.assets = assets
        self.on_adv_click = on_adv_click
        self.on_help = on_help
        self.on_menu = on_menu
        self.on_login = on_login
        self.on_register = on_register
        self.on_transfer = on_transfer
        self.on_remember_toggle = on_remember_toggle

    def draw(self) -> None:
        self._draw_background()
        self._draw_header()
        self._draw_left_panel()
        self._draw_main_content()

    def _bind_clickable(self, tag: str, callback: Callable[[], None]) -> None:
        self.canvas.tag_bind(tag, "<Button-1>", lambda _e: callback())
        self.canvas.tag_bind(tag, "<Enter>", lambda _e: self.canvas.configure(cursor="hand2"))
        self.canvas.tag_bind(tag, "<Leave>", lambda _e: self.canvas.configure(cursor=""))

    def _draw_background(self) -> None:
        self.canvas.create_rectangle(
            0, 0, 400, 740, fill=self.colors.left, outline=self.colors.left
        )
        self.canvas.create_rectangle(
            400, 0, 1200, 740, fill=self.colors.content, outline=self.colors.content
        )

    def _draw_header(self) -> None:
        self.canvas.create_rectangle(
            0, 0, 1200, 80, fill=self.colors.header, outline=self.colors.header
        )

        logo = self.assets.load_image("logo", "logo.jpg", 355, 80)
        place_image(self.canvas, logo, 0, 0)

        self.canvas.create_rectangle(
            1040,
            14,
            1090,
            64,
            outline=self.colors.text_light,
            width=1,
            tags=("help_btn",),
        )
        self.canvas.create_text(
            1065,
            39,
            text="?",
            fill=self.colors.text_light,
            font=("Poppins", 34, "bold"),
            tags=("help_btn",),
        )
        self._bind_clickable("help_btn", self.on_help)

        self.canvas.create_rectangle(
            1130,
            14,
            1180,
            64,
            outline=self.colors.text_light,
            width=1,
            fill=self.colors.header,
            tags=("menu_btn",),
        )
        self.canvas.create_line(
            1140,
            24,
            1170,
            24,
            fill=self.colors.text_light,
            width=5,
            tags=("menu_btn",),
        )
        self.canvas.create_line(
            1140,
            39,
            1170,
            39,
            fill=self.colors.text_light,
            width=5,
            tags=("menu_btn",),
        )
        self.canvas.create_line(
            1140,
            54,
            1170,
            54,
            fill=self.colors.text_light,
            width=5,
            tags=("menu_btn",),
        )
        self._bind_clickable("menu_btn", self.on_menu)

    def _draw_left_panel(self) -> None:
        rounded_rect(self.canvas, 38, 120, 361, 170, 10, self.colors.input, "")
        rounded_rect(self.canvas, 38, 190, 361, 240, 10, self.colors.input, "")

        self.canvas.create_text(
            54,
            145,
            text="ЛОГИН",
            anchor="w",
            fill=self.colors.white,
            font=self.fonts.label,
        )
        self.canvas.create_text(
            54,
            215,
            text="ПАРОЛЬ",
            anchor="w",
            fill=self.colors.white,
            font=self.fonts.label,
        )

        self.canvas.create_text(
            38,
            278,
            text="Запомнить логин",
            anchor="w",
            fill=self.colors.text_light,
            font=self.fonts.label,
        )

        self.canvas.create_rectangle(
            331, 263, 361, 293, outline="#EEE0E5", width=1, tags=("remember_btn",)
        )
        self.canvas.create_text(
            346,
            278,
            text="✓",
            fill=self.colors.text_light,
            font=("Poppins", 24, "bold"),
            tags=("remember_btn",),
        )
        self._bind_clickable("remember_btn", self.on_remember_toggle)

        rounded_rect(
            self.canvas,
            38,
            336,
            361,
            396,
            10,
            self.colors.accent,
            "",
            tag="login_btn",
        )
        self.canvas.create_text(
            200,
            366,
            text="АВТОРИЗОВАТЬСЯ",
            fill=self.colors.text_light,
            font=self.fonts.label,
            tags=("login_btn",),
        )
        self._bind_clickable("login_btn", self.on_login)

        self.canvas.create_text(
            38,
            451,
            text="Это длинный текст перед..",
            anchor="w",
            fill=self.colors.text_light,
            font=self.fonts.small,
        )
        man = self.assets.load_image("man", "man.png", 30, 30)
        place_image(self.canvas, man, 331, 436)

        rounded_rect(
            self.canvas,
            38,
            486,
            361,
            536,
            10,
            self.colors.white,
            "",
            tag="register_btn",
        )
        self.canvas.create_text(
            200,
            511,
            text="ЗАРЕГИСТРИРОВАТЬСЯ",
            fill=self.colors.text_dark,
            font=self.fonts.medium,
            tags=("register_btn",),
        )
        self._bind_clickable("register_btn", self.on_register)

    def _draw_main_content(self) -> None:
        self.canvas.create_text(
            410,
            112,
            text="УМНАЯ СИСТЕМА ПЕРЕВОДОВ",
            anchor="w",
            fill=self.colors.text_dark,
            font=self.fonts.title,
        )
        self.canvas.create_text(
            415,
            145,
            text="С ВНЕДРЕНИЕМ СОВРЕМЕННЫХ ИИ",
            anchor="w",
            fill=self.colors.text_dark,
            font=self.fonts.subtitle,
        )
        self.canvas.create_text(
            880,
            112,
            text="НАМ ДОВЕРЯЮТ",
            anchor="w",
            fill=self.colors.text_dark,
            font=self.fonts.title,
        )

        rounded_rect(self.canvas, 420, 190, 780, 419, 16, self.colors.accent, "")
        self.canvas.create_text(
            450,
            236,
            text="Уралсиб",
            anchor="w",
            fill=self.colors.white,
            font=("Poppins", 18, "bold"),
        )
        self.canvas.create_text(
            740,
            236,
            text="Business",
            anchor="e",
            fill=self.colors.white,
            font=("Poppins", 14, "bold"),
        )

        rounded_rect(self.canvas, 440, 267, 760, 317, 10, self.colors.input, "")
        rounded_rect(self.canvas, 440, 337, 580, 387, 10, self.colors.input, "")
        rounded_rect(self.canvas, 620, 337, 760, 387, 10, self.colors.input, "")

        self.canvas.create_text(
            451,
            292,
            text="НОМЕР КАРТЫ",
            anchor="w",
            fill=self.colors.white,
            font=self.fonts.label,
        )
        self.canvas.create_text(
            451,
            362,
            text="MM/ГГ",
            anchor="w",
            fill=self.colors.white,
            font=self.fonts.label,
        )
        self.canvas.create_text(
            631,
            362,
            text="CVC/CVV",
            anchor="w",
            fill=self.colors.white,
            font=self.fonts.label,
        )

        self.canvas.create_text(
            426,
            470,
            text="Сумма перевода",
            anchor="w",
            fill=self.colors.text_dark,
            font=self.fonts.small,
        )
        rounded_rect(
            self.canvas, 421, 486, 779, 536, 10, self.colors.input, self.colors.accent, 1
        )

        self.canvas.create_text(
            426,
            567,
            text="Сообщение получателю",
            anchor="w",
            fill=self.colors.text_dark,
            font=self.fonts.small,
        )
        rounded_rect(
            self.canvas, 421, 583, 779, 633, 10, self.colors.input, self.colors.accent, 1
        )

        rounded_rect(
            self.canvas,
            421,
            653,
            779,
            713,
            10,
            self.colors.accent,
            "",
            tag="transfer_btn",
        )
        self.canvas.create_text(
            600,
            683,
            text="ПЕРЕВЕСТИ",
            fill=self.colors.text_light,
            font=self.fonts.label,
            tags=("transfer_btn",),
        )
        self._bind_clickable("transfer_btn", self.on_transfer)

        self.canvas.create_rectangle(804, 138, 1182, 735, outline=self.colors.accent, width=3)
        adv = self.assets.load_image("adv", "adv.jpg", 372, 591, fill=True)
        adv_id = place_image(self.canvas, adv, 807, 141)
        if adv_id is not None:
            self.canvas.tag_bind(adv_id, "<Button-1>", self.on_adv_click)
            self.canvas.tag_bind(adv_id, "<Enter>", lambda _e: self.canvas.configure(cursor="hand2"))
            self.canvas.tag_bind(adv_id, "<Leave>", lambda _e: self.canvas.configure(cursor=""))
