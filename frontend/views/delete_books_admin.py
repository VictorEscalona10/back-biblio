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
    
    # Función para confirmar y ejecutar la eliminación
    def confirm_delete(e):
        title = title_field.value.strip()
        if not title:
            title_field.error_text = "Debes ingresar un título"
            title_field.update()
            return
        
        # Diálogo de confirmación
        def execute_delete(e):
            # Aquí iría tu llamada a DELETE /books con el título
            # Ejemplo:
            # response = requests.delete(f"{API_URL}/books", json={"title": title})
            
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Libro '{title}' eliminado correctamente"),
                duration=3000
            )
            page.snack_bar.open = True
            title_field.value = ""
            title_field.focus()
            page.update()
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar el libro '{title}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, "open", False)),
                ft.TextButton("Eliminar", on_click=execute_delete, style=ft.ButtonStyle(color=ft.colors.RED))
            ],
            open=True
        )
        page.update()
    
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
                    on_click=confirm_delete,
                    color=ft.colors.RED
                ),
            ],
            spacing=20
        )
    ])
    body_column.update()