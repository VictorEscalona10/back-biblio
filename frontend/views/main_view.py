import flet as ft
from utils.jwt_utils import decode_jwt
from views.books_view import load_books, add_book_page
from views.profile_view import load_profile

def main_page(page: ft.Page):
    page.clean()

    # Verificar si el usuario está autenticado
    jwt_token = page.client_storage.get("jwt")
    if not jwt_token:
        page.go("/login")
        return

    # Decodificar el JWT para obtener información del usuario
    user_info = decode_jwt(jwt_token)
    user_name = user_info.get("name", "Usuario") if user_info else "Usuario"
    user_email = user_info.get("email", None) if user_info else None

    page.title = f"Biblioteca - {user_name}"

    # Crear el panel izquierdo
    def show_view(view_name):
        content_panel.controls.clear()
        if view_name == "Inicio":
            content_panel.controls.append(ft.Text("Vista de Inicio", size=20))
        elif view_name == "Libros":
            load_books(page, content_panel)
        elif view_name == "Agregar Libro":
            add_book_page(page, content_panel, user_email)
        elif view_name == "Perfil":
            load_profile(page, content_panel, user_name, user_email)
        elif view_name == "Configuración":
            content_panel.controls.append(ft.Text("Vista de Configuración", size=20))
        content_panel.update()

    def logout(e):
        page.client_storage.remove("jwt")
        page.go("/login")

    # Botones de navegación
    navigation_buttons = ft.Column(
        [
            ft.Text(f"Bienvenido, {user_name}!", size=20, color=ft.colors.GREEN),
            ft.ElevatedButton("Inicio", on_click=lambda e: show_view("Inicio")),
            ft.ElevatedButton("Libros", on_click=lambda e: show_view("Libros")),
            ft.ElevatedButton("Agregar Libro", on_click=lambda e: show_view("Agregar Libro")),
            ft.ElevatedButton("Perfil", on_click=lambda e: show_view("Perfil")),
            ft.ElevatedButton("Configuración", on_click=lambda e: show_view("Configuración")),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    )

    # Botón de logout al final
    logout_button = ft.Container(
        ft.ElevatedButton("Logout", on_click=logout),
        alignment=ft.alignment.bottom_center,
    )

    # Contenedor del panel izquierdo
    sidebar = ft.Container(
        ft.Column(
            [
                navigation_buttons,
                logout_button,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        width=200,
        bgcolor=ft.colors.BLUE_GREY_100,
    )

    # Crear el área de contenido principal
    content_panel = ft.Column(
        [ft.Text("Selecciona una opción del menú", size=20)],
        expand=True,
    )

    # Disponer el panel izquierdo y el área de contenido en un Row
    layout = ft.Row(
        [sidebar, content_panel],
        expand=True,
    )

    page.add(layout)
    page.update()