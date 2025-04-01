import flet as ft
from utils.jwt_utils import decode_jwt
from views.books_view import load_books, add_book_page
from views.profile_view import load_profile

def main_page(page: ft.Page):
    page.clean()
    page.bgcolor = '#212121'

    jwt_token = page.client_storage.get("jwt")
    if not jwt_token:
        page.go("/login")
        return

    user_info = decode_jwt(jwt_token)
    user_name = user_info.get("name", "Usuario") if user_info else "Usuario"
    user_email = user_info.get("email", None) if user_info else None

    page.title = f"Biblioteca - {user_name}"

    body_column = ft.Column(
        [],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    def show_view(view_name):
        body_column.controls.clear()
        if view_name == "Inicio":
            body_column.controls.append(
                ft.Text("Bienvenido a la Biblioteca", 
                       size=20, 
                       color=ft.colors.WHITE)
            )
        elif view_name == "Libros":
            load_books(page, body_column)
        elif view_name == "Agregar Libro":
            add_book_page(page, body_column, user_email)
        elif view_name == "Perfil":
            load_profile(page, body_column, user_name, user_email)
        elif view_name == "Configuración":
            body_column.controls.append(ft.Text("Vista de Configuración", size=20))
        body_column.update()

    def logout(e):
        page.client_storage.remove("jwt")
        page.go("/login")

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=56,
        min_extended_width=2160,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME,
                label="Inicio",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.BOOK_OUTLINED,
                selected_icon=ft.icons.BOOK,
                label="Libros",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD,
                selected_icon=ft.icons.ADD,
                label="Agregar Libro",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON_OUTLINED,
                selected_icon=ft.icons.PERSON,
                label="Perfil",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="Configuración",
            ),
        ],
        on_change=lambda e: show_view(e.control.destinations[e.control.selected_index].label),
    )

    fab = ft.FloatingActionButton(
        text="Logout",
        icon=ft.icons.LOGOUT,
        tooltip="Cerrar sesión",
        on_click=logout,
        bgcolor=ft.colors.RED_400,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Stack(
                    [
                        body_column,
                        ft.Row(
                            [fab],
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            expand=True,
                        )
                    ],
                    expand=True,
                )
            ],
            expand=True,
        )
    )
    
    show_view("Inicio")
    page.update()