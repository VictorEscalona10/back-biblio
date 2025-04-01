import flet as ft
import requests
from utils.constants import BASE_URL

def update_user_page(page: ft.Page, body_column: ft.Column, admin_email: str):
    body_column.controls.clear()
    
    email_field = ft.TextField(label="Email del usuario", autofocus=True, width=400)
    name_field = ft.TextField(label="Nombre", width=400)
    password_field = ft.TextField(label="Nueva contraseña", password=True, can_reveal_password=True, width=400)
    message_label = ft.Text(value="", size=20, color=ft.colors.GREEN)
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def submit_update(e):
        if not email_field.value:
            email_field.error_text = "El email es obligatorio"
            email_field.update()
            return
        
        update_data = {
            "email": email_field.value,
            "name": name_field.value if name_field.value else None,
            "password": password_field.value if password_field.value else None
        }

        response = requests.put(
            f"{BASE_URL}/users",
            json=update_data,
            headers={"Authorization": f"Bearer {page.client_storage.get('jwt')}"}
        )

        if response.status_code == 200:
            message_label.value = "Usuario actualizado correctamente"
            message_label.color = ft.colors.GREEN
            page.snack_bar = ft.SnackBar(ft.Text("Usuario actualizado correctamente"))
            page.snack_bar.open = True
        else:
            error_msg = response.json().get("error", "Error al actualizar el usuario")
            message_label.value = error_msg
            message_label.color = ft.colors.RED
        
        # Limpiar solo el campo de contraseña por seguridad
        password_field.value = ""
        page.update()
    
    body_column.controls.extend([
        ft.Text("Actualizar Usuario", size=24, weight=ft.FontWeight.BOLD),
        email_field,
        name_field,
        password_field,
        message_label,
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Actualizar",
                    icon=ft.icons.UPDATE,
                    on_click=submit_update,
                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE)
                ),
            ],
            spacing=10
        )
    ])
    body_column.update()