import flet as ft
import requests
from utils.constants import BASE_URL

def register_page(page: ft.Page):
    # Elementos para el registro
    title = ft.Text("Registro", size=30, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
    register_message = ft.Text(value="", size=20)
    register_name_input = ft.TextField(label="Nombre completo", width=300)
    register_email_input = ft.TextField(label="Email", width=300, )
    register_password_input = ft.TextField(label="Contraseña", password=True, width=300)
    register_repeat_password_input = ft.TextField(label="Repetir contraseña", password=True, width=300)

    page.clean()
    page.title = "Biblioteca - registro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    register_message.value = ""
    register_name_input.value = ""
    register_email_input.value = ""
    register_password_input.value = ""
    register_repeat_password_input.value = ""

    col = ft.Column(
        [
            title,
            register_message,
            register_name_input,
            register_email_input,
            register_password_input,
            register_repeat_password_input,
            ft.Row(
                [
                    ft.ElevatedButton("Registrarse", on_click=lambda e: register(e, page, register_message, register_name_input, register_email_input, register_password_input, register_repeat_password_input)),
                    ft.ElevatedButton("Volver al Login", on_click=lambda e: back_to_login(e, page))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(
        content=col,
        bgcolor='#424242',
        border_radius=5,
        padding=50,
        width=500,
        ))
    page.update()

def register(e, page, register_message, register_name_input, register_email_input, register_password_input, register_repeat_password_input):
    name = register_name_input.value
    email = register_email_input.value
    password = register_password_input.value
    repeat_password = register_repeat_password_input.value

    if password != repeat_password:
        register_message.value = "Las contraseñas no coinciden"
        register_message.color = ft.colors.RED
        page.update()
        return

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"name": name, "email": email, "password": password, "repeatPassword": repeat_password}
    )

    if response.status_code == 200:
        register_message.value = response.json().get("message", "Registro exitoso")
        register_message.color = ft.colors.GREEN
        # Limpiar campos después de registro exitoso
        register_name_input.value = ""
        register_email_input.value = ""
        register_password_input.value = ""
        register_repeat_password_input.value = ""
    else:
        register_message.value = response.json().get("error", "Error desconocido en el registro")
        register_message.color = ft.colors.RED

    page.update()

def back_to_login(e, page):
    page.go("/login")