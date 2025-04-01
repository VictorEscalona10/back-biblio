import flet as ft
import requests
from utils.constants import BASE_URL


def delete_book_page(page: ft.Page, body_column: ft.Column):
    body_column.controls.clear()
    
    # Campo de entrada para el título
    title_field = ft.TextField(
        label="Título del libro a eliminar",
        autofocus=True,
        hint_text="Ingresa el título exacto del libro",
        width=400
    )
        
    # Diálogo de confirmación
    def execute_delete(e):
        if not title_field.value:
            title_field.error_text = "El título es obligatorio"
            title_field.update()
            return
        
        response = requests.delete(
            f"{BASE_URL}/books",
            json={
                    "title": title_field.value,
            }
            )
            
        if response.status_code == 200:
            title_field.value = ""
            title_field.update()
        else:
            title_field.error_text = "Error al eliminar el libro"
            title_field.update()

        title_field.value = ""
        title_field.update()

            
    
    # Diseño de la vista
    body_column.controls.extend([
        ft.Text("Eliminar Libro", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Ingresa el título exacto del libro que deseas eliminar:", size=16),
        ft.Divider(height=20),
        title_field,
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Eliminar Libro",
                    icon=ft.icons.DELETE,
                    on_click=execute_delete,
                    color=ft.colors.RED
                ),
            ],
            spacing=20
        )
    ])
    body_column.update()