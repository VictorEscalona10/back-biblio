import flet as ft
import requests
from utils.constants import BASE_URL

def load_profile(page, content_panel, user_name, user_email):
    content_panel.controls.clear()
    try:
        # Hacer la petición para obtener los libros del usuario
        response = requests.post(f"{BASE_URL}/books/user", json={"email": user_email})
        if response.status_code == 200:
            books = response.json().get("books", [])
            book_list = ft.ListView(
                controls=[
                    ft.Text(f"- {book['title']}", size=18, color=ft.colors.BLUE)
                    for book in books
                ],
                expand=True,
            )
        else:
            book_list = ft.Text(response.json().get("error"), color=ft.colors.RED)

        # Crear el diseño del perfil
        profile_layout = ft.Column(
            [
                ft.Text("Perfil del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nombre: {user_name}", size=20),
                ft.Text(f"Correo: {user_email}", size=20),
                ft.Text("Libros guardados:", size=20, weight=ft.FontWeight.BOLD),
                book_list,
            ],
            spacing=15,
        )

        content_panel.controls.append(profile_layout)
    except Exception as e:
        content_panel.controls.append(ft.Text(f"Error: {e}", size=20, color=ft.colors.RED))
    content_panel.update()