from __future__ import annotations

from pathlib import Path
import tkinter as tk
import webbrowser
from tkinter import font as tkfont
from tkinter import messagebox

from .assets import AssetLoader
from backend import AuthService, Backend, BankDatabase
from .layout import Colors, Fonts, Layout
from .menu_window import MenuWindow
from .registration_window import RegistrationWindow


class BankApp(tk.Tk):
    """Static bank window mockup based on fixed coordinates."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Уралсиб — макет")
        self.geometry("1200x740")
        self.minsize(1200, 740)
        self.maxsize(1200, 740)
        self.resizable(False, False)

        self.colors = Colors(
            header="#250F56",
            left="#5F5180",
            content="#E3E2ED",
            accent="#250F56",
            text_light="#FFFFFF",
            text_dark="#250F56",
            white="#FFFFFF",
            input="#E3E2ED",
            input_text="#250F56",
        )
        self.fonts = Fonts(
            title=("Poppins", 20, "bold"),
            subtitle=("Poppins", 16, "bold"),
            label=("Poppins", 24, "bold"),
            medium=("Poppins", 20, "bold"),
            small=("Poppins", 15, "bold"),
        )

        self._init_fonts()
        self._entries: list[tk.Entry] = []
        self.login_entry: tk.Entry | None = None
        self.password_entry: tk.Entry | None = None
        self.registration_window: RegistrationWindow | None = None
        self.menu_window: MenuWindow | None = None

        asset_dir = Path(__file__).resolve().parent.parent / "asset"
        self.assets = AssetLoader(asset_dir)
        if not self.assets.can_load():
            messagebox.showerror(
                "Pillow не установлен",
                "Для отображения изображений нужен пакет Pillow.\n"
                "Установите: pip install pillow",
            )

        db_path = Path(__file__).resolve().parent.parent / "data" / "bank.db"
        auth_service = AuthService(BankDatabase(db_path))
        auth_service.bootstrap()
        self.backend = Backend(auth_service)

        self.canvas = tk.Canvas(
            self,
            width=1200,
            height=740,
            bg=self.colors.content,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        layout = Layout(
            self.canvas,
            self.colors,
            self.fonts,
            self.assets,
            self._open_adv_link,
            self.backend.on_help,
            self._open_menu_window,
            self._on_login_click,
            self._open_registration_window,
            self.backend.on_transfer,
            self.backend.on_remember_toggle,
        )
        layout.draw()
        self._place_entries()

    def _init_fonts(self) -> None:
        try:
            tkfont.Font(family="Poppins", size=12)
        except tk.TclError:
            # Fallback to default fonts if Poppins is not installed.
            self.fonts = Fonts(
                title=("Helvetica", 20, "bold"),
                subtitle=("Helvetica", 16, "bold"),
                label=("Helvetica", 24, "bold"),
                medium=("Helvetica", 20, "bold"),
                small=("Helvetica", 15, "bold"),
            )

    def _place_entries(self) -> None:
        self._entries.clear()
        self.login_entry = self._make_entry(42, 124, 315, 42)
        self.password_entry = self._make_entry(42, 194, 315, 42, show="•")
        self._entries.extend(
            [
                self.login_entry,
                self.password_entry,
                self._make_entry(444, 271, 312, 42),
                self._make_entry(444, 341, 132, 42),
                self._make_entry(624, 341, 132, 42),
                self._make_entry(425, 490, 350, 42),
                self._make_entry(425, 587, 350, 42),
            ]
        )

    def _make_entry(
        self, x: int, y: int, width: int, height: int, show: str | None = None
    ) -> tk.Entry:
        entry = tk.Entry(
            self,
            bg=self.colors.input,
            fg=self.colors.input_text,
            relief="flat",
            highlightthickness=0,
            font=self.fonts.small,
            show=show or "",
        )
        entry.place(x=x, y=y, width=width, height=height)
        return entry

    @staticmethod
    def _open_adv_link(_event: tk.Event) -> None:
        webbrowser.open("https://i.pinimg.com/originals/3c/94/2c/3c942c625b2177e2390920ee1e8ebfda.jpg")

    def _on_login_click(self) -> None:
        if self.login_entry is None or self.password_entry is None:
            messagebox.showerror("Авторизация", "Поля логина и пароля не инициализированы.")
            return

        self.backend.on_login(self.login_entry.get(), self.password_entry.get())

    def _open_registration_window(self) -> None:
        if self.registration_window is not None and self.registration_window.winfo_exists():
            self.registration_window.lift()
            self.registration_window.focus_force()
            return

        self.registration_window = RegistrationWindow(
            master=self,
            colors=self.colors,
            fonts=self.fonts,
            on_submit=self._submit_registration,
        )
        self.registration_window.protocol("WM_DELETE_WINDOW", self._close_registration_window)

    def _submit_registration(self, data: dict[str, str]) -> bool:
        ok = self.backend.on_register_submit(
            login=data.get("login", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            password=data.get("password", ""),
        )
        if ok:
            self._close_registration_window()
        return ok

    def _close_registration_window(self) -> None:
        if self.registration_window is not None and self.registration_window.winfo_exists():
            self.registration_window.destroy()
        self.registration_window = None

    def _open_menu_window(self) -> None:
        if self.menu_window is not None and self.menu_window.winfo_exists():
            self.menu_window.lift()
            self.menu_window.focus_force()
            return

        self.menu_window = MenuWindow(
            master=self,
            colors=self.colors,
            fonts=self.fonts,
            on_profile=self.backend.on_profile,
            on_settings=self.backend.on_settings,
            on_security=self.backend.on_security,
            on_support=self.backend.on_support,
            on_logout=self._on_logout_click,
        )
        self.menu_window.protocol("WM_DELETE_WINDOW", self._close_menu_window)

    def _on_logout_click(self) -> None:
        if self.login_entry is not None:
            self.login_entry.delete(0, "end")
        if self.password_entry is not None:
            self.password_entry.delete(0, "end")
        self.backend.on_logout()
        self._close_menu_window()

    def _close_menu_window(self) -> None:
        if self.menu_window is not None and self.menu_window.winfo_exists():
            self.menu_window.destroy()
        self.menu_window = None
