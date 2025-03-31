import flet as ft
import requests
from utils.constants import BASE_URL
from utils.jwt_utils import decode_jwt

def login_page(page: ft.Page):
    # Limpiar la página antes de agregar elementos
    page.clean()

    def show_register(e):
        page.go("/register")
        
    # Configuración inicial
    title = ft.Text("Iniciar sesión", size=30, weight=ft.FontWeight.NORMAL, color=ft.colors.BLACK, text_align=ft.TextAlign.CENTER)
    message = ft.Text(value="", size=20, color=ft.colors.GREEN)
    email_input = ft.TextField(label="Email", width=300, color=ft.colors.BLACK)
    password_input = ft.TextField(label="Password", password=True, width=300, color=ft.colors.BLACK)
    login_button = ft.ElevatedButton(text="Login",color=ft.colors.WHITE, bgcolor=ft.colors.BLACK, width=300,height=35, on_click=lambda e: login(e, page, message, email_input, password_input), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)))
    register_button = ft.ElevatedButton("Registrarse", on_click=show_register, color=ft.colors.WHITE, bgcolor=ft.colors.BLACK, width=118,height=35, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)))

    page.title = "Biblioteca - login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    message.value = ""
    email_input.value = ""
    password_input.value = ""

    col = ft.Column(
        [
            title,
            message, 
            email_input, 
            password_input, 
            login_button,
            ft.Row(
                [
                    ft.Text("¿No tienes cuenta?", size=20, color='#000000'),
                    register_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(
        content=col,
        bgcolor='#ffffff',
        border_radius=5,
        padding=50,
        width=500,
    ))
    page.update()

def login(e, page, message, email_input, password_input):
    email = email_input.value
    password = password_input.value

    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        jwt_token = response.cookies.get("authToken")
        if jwt_token:
            page.client_storage.set("jwt", jwt_token)
            page.go("/main")
        else:
            message.value = "Error: No se recibió un token de autenticación."
            message.color = ft.colors.RED
            page.update()
    else:
        message.value = response.json().get("error", "Error desconocido")
        message.color = ft.colors.RED
        page.update()

    email_input.value = ""
    password_input.value = ""
    page.update()