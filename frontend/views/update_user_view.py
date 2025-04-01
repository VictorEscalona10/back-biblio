# update_user_view.py
import flet as ft
import requests
from utils.constants import BASE_URL
from utils.jwt_utils import decode_jwt
from views.admin_view import admin_page

class UpdateUserView:
    def __init__(self, page, jwt_token, go_back_callback, search_user_callback, update_user_callback):
        self.page = page
        self.jwt_token = jwt_token
        self.go_back_callback = go_back_callback
        self.search_user_callback = search_user_callback
        self.update_user_callback = update_user_callback
        self.server_response = ft.Text("", color=ft.colors.GREEN)
        self.build_view()

    def build_view(self):
        # Campos del formulario (igual que antes)
        self.email_input = ft.TextField(
            label="Email del usuario a actualizar",
            width=400,
            autofocus=True
        )
        
        self.name_input = ft.TextField(
            label="Nuevo nombre (opcional)",
            width=400
        )
        
        self.password_input = ft.TextField(
            label="Nueva contraseña (opcional)",
            width=400,
            password=True,
            can_reveal_password=True
        )

        # Botones (igual que antes)
        search_button = ft.ElevatedButton(
            "Buscar Usuario",
            icon=ft.icons.SEARCH,
            on_click=self.search_user,
            width=200
        )
        
        update_button = ft.ElevatedButton(
            "Actualizar Usuario",
            icon=ft.icons.UPDATE,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
            on_click=self.update_user,
            width=200
        )
        
        back_button = ft.ElevatedButton(
            "Volver",
            icon=ft.icons.ARROW_BACK,
            on_click=lambda e: self.go_back_callback(),
            width=200
        )

        # Diseño de la vista (igual que antes)
        self.view = ft.Column(
            [
                ft.Text("Actualizar Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.email_input,
                ft.Row([search_button], alignment=ft.MainAxisAlignment.CENTER),
                self.name_input,
                self.password_input,
                ft.Row([update_button, back_button], spacing=20),
                self.server_response
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=600
        )

    async def search_user(self, e):
        email = self.email_input.value.strip()
        if not email:
            self.show_response("Por favor ingrese el email del usuario", True)
            return

        # Usamos el callback en lugar de la petición HTTP directa
        result = await self.search_user_callback(email)
        
        if result.get("success"):
            user_data = result.get("data", {})
            self.name_input.value = user_data.get("name", "")
            self.password_input.value = ""
            self.page.update()
            self.show_response("Usuario encontrado")
        else:
            self.show_response(result.get("error", "Error al buscar usuario"), True)

    async def update_user(self, e):
        email = self.email_input.value.strip()
        if not email:
            self.show_response("Por favor ingrese el email del usuario", True)
            return

        update_data = {
            "email": email,
            "name": self.name_input.value if self.name_input.value else None,
            "password": self.password_input.value if self.password_input.value else None
        }

        # Diálogo de confirmación (igual que antes)
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar actualización"),
            content=ft.Text(f"¿Está seguro que desea actualizar el usuario '{email}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.TextButton("Actualizar", 
                            on_click=lambda e: self.confirm_update(update_data),
                            style=ft.ButtonStyle(color=ft.colors.BLUE)),
            ],
        )
        
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    async def confirm_update(self, update_data):
        # Usamos el callback en lugar de la petición HTTP directa
        result = await self.update_user_callback(update_data)
        
        if result.get("success"):
            self.show_response(f"Usuario '{update_data['email']}' actualizado exitosamente")
            self.name_input.value = ""
            self.password_input.value = ""
            self.page.update()
        else:
            self.show_response(result.get("error", "Error al actualizar usuario"), True)
        
        self.close_dialog(None)

    def close_dialog(self, e):
        if self.page.dialog:
            self.page.dialog.open = False
        self.page.update()

    def show_response(self, message, is_error=False):
        self.server_response.value = message
        self.server_response.color = ft.colors.RED if is_error else ft.colors.GREEN
        self.server_response.update()

    def get_view(self):
        return self.view