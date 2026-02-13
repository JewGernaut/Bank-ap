from __future__ import annotations

from dataclasses import dataclass
from tkinter import messagebox

from .auth_service import AuthService


@dataclass
class Backend:
    auth_service: AuthService

    def on_help(self) -> None:
        messagebox.showinfo("Помощь", "Да помоги вам богъ.")

    def on_menu(self) -> None:
        messagebox.showinfo("Меню", "Не лезь оно тебя тебя сожрет.")

    def on_profile(self) -> None:
        messagebox.showinfo("Профиль", "Nice Backend bro😉.")

    def on_settings(self) -> None:
        messagebox.showinfo("Настройки", "У вас недостаточно прав доступа, свяжитесь с администратором.")

    def on_security(self) -> None:
        messagebox.showinfo("Безопасность", "Это вам не понадобяться, мы и так самый безопасный банк, век воли не видать.")

    def on_support(self) -> None:
        messagebox.showinfo("Поддержка", "+7 (495) 989-50-50-телефон доверия.")

    def on_logout(self) -> None:
        messagebox.showinfo("Выход", "Один раз зайдя, оставь надежду всяк сюда входящий.")

    def on_login(self, login: str, password: str) -> None:
        if not login.strip() or not password:
            messagebox.showwarning("Авторизация", "Введите логин и пароль.")
            return

        result = self.auth_service.authenticate(login.strip(), password)
        if result.ok:
            messagebox.showinfo("Авторизация", result.message)
            return

        messagebox.showerror("Авторизация", result.message)

    def on_register(self) -> None:
        messagebox.showinfo(
            "Регистрация",
            "Кнопка регистрации пока заглушка.\n"
            "Для теста авторизации используйте: demo / demo123",
        )

    def on_register_submit(
        self,
        login: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> bool:
        login = login.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        password = password.strip()

        if not all([login, first_name, last_name, password]):
            messagebox.showwarning("Регистрация", "Заполните все поля.")
            return False

        result = self.auth_service.register_user(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        if result.ok:
            messagebox.showinfo(
                "Регистрация",
                "Пользователь зарегистрирован.\n"
                "Лицевой счет и номер карты созданы автоматически.",
            )
            return True

        messagebox.showerror("Регистрация", result.message)
        return False

    def on_transfer(self) -> None:
        messagebox.showinfo("Перевод", "Перевод успешно выполнен! Ваши средства ушли в пользу общака.")

    def on_remember_toggle(self) -> None:
        messagebox.showinfo("Запомнить", "Переключатель запоминания (заглушка).")
