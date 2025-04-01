import flet as ft
import requests
import webbrowser
from utils.constants import BASE_URL

def add_book_page_admin(page: ft.Page, body_column: ft.Column, user_email: str):
    body_column.controls.clear()
    
    title_field = ft.TextField(label="Título", autofocus=True, width=400)
    message_label = ft.Text(value="", size=20, color=ft.colors.GREEN)
    author_field = ft.TextField(label="Autor", width=400)
    year_field = ft.TextField(label="Año", width=400)
    link_field = ft.TextField(label="Enlace", width=400)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def submit_book(e):
        if not title_field.value:
            title_field.error_text = "El título es obligatorio"
            title_field.update()
            return
        
        response = requests.post(
            f"{BASE_URL}/books",
            json={
                "title": title_field.value,
                "author": author_field.value,
                "year": year_field.value,
                "link": link_field.value
            }
        )

        if response.status_code == 201:
            message_label.value = "Libro agregado correctamente"
        else:
            message_label.value = "Error al agregar el libro"
        
        title_field.value = ""
        author_field.value = ""
        year_field.value = ""
        link_field.value = ""
        page.update()
    
    text_fields = body_column.controls.extend([
        ft.Text("Agregar Nuevo Libro", size=24, weight=ft.FontWeight.BOLD),
        title_field,
        message_label,
        author_field,
        year_field,
        link_field,
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Guardar",
                    icon=ft.icons.SAVE,
                    on_click=submit_book
                ),
            ],
            spacing=10
            )    
        ]
    )
    body_column.update()