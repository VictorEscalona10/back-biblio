import requests
import flet as ft
from decoded import decode_jwt  # Asegúrate de que decode_jwt esté correctamente implementado
import webbrowser  # Para abrir el enlace en el navegador

BASE_URL = "http://localhost:3000"

def main(page: ft.Page):
    def login(e):
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

    def show_register(e):
        page.go("/register")

    def register(e):
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

    def back_to_login(e):
        page.go("/login")

    def logout(e):
        page.client_storage.remove("jwt")  # Eliminar el token almacenado
        page.go("/login")  # Redirigir a la página de inicio de sesión

    def main_page():
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
                load_books()
            elif view_name == "Agregar Libro":
                add_book_page(user_email)
            elif view_name == "Perfil":
                load_profile(user_name, user_email)
            elif view_name == "Configuración":
                content_panel.controls.append(ft.Text("Vista de Configuración", size=20))
            content_panel.update()

        # Función para cargar libros
        def load_books():
            content_panel.controls.clear()
            try:
                response = requests.get(f"{BASE_URL}/books")
                if response.status_code == 200:
                    books = response.json().get("books", [])
                    if not books:
                        content_panel.controls.append(ft.Text("No se encontraron libros.", size=20))
                    else:
                        # Crear una lista scrolleable de libros con enlaces
                        book_list = ft.ListView(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.TextButton(
                                            text=book["title"],
                                            on_click=lambda e, link=book["file_link"]: webbrowser.open(link)
                                        ),
                                        ft.Text(
                                            f"- {book.get('author', 'Autor desconocido')}",
                                            size=18,
                                            color=ft.colors.GREY
                                        ),
                                    ]
                                ) for book in books
                            ],
                            expand=True,  # Asegura que se adapte al espacio disponible
                        )
                        content_panel.controls.append(book_list)
                else:
                    content_panel.controls.append(ft.Text("Error al cargar los libros.", size=20, color=ft.colors.RED))
            except Exception as e:
                content_panel.controls.append(ft.Text(f"Error: {e}", size=20, color=ft.colors.RED))
            content_panel.update()

        # Función para mostrar la página de agregar libros
        def add_book_page(user_email):
            content_panel.controls.clear()

            title_input = ft.TextField(label="Título del libro", width=300)
            message_label = ft.Text(value="", size=20, color=ft.colors.GREEN)

            def submit_book(e):
                title = title_input.value
                try:
                    response = requests.post(
                        f"{BASE_URL}/books/user",
                        json={"email": user_email, "title": title},  # Usamos el email del JWT
                    )
                    if response.status_code == 200:
                        message_label.value = response.json().get("message", "Libro agregado exitosamente.")
                        message_label.color = ft.colors.GREEN
                    else:
                        message_label.value = response.json().get("error", "Error desconocido al agregar el libro.")
                        message_label.color = ft.colors.RED
                except Exception as e:
                    message_label.value = f"Error: {e}"
                    message_label.color = ft.colors.RED
                page.update()

                title_input.value = ""

            content_panel.controls.extend([
                ft.Text("Agregar un nuevo libro al usuario", size=20),
                title_input,
                ft.ElevatedButton(text="Enviar", on_click=submit_book),
                message_label,
            ])
            content_panel.update()

        # Función para mostrar el perfil del usuario
        def load_profile(user_name, user_email):
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
                    logout_button,  # Botón de logout al final
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Espacio entre la parte superior e inferior
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

    def login_page():
        # Limpiar la página antes de agregar elementos
        page.clean()

        page.title = "Biblioteca - login"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Ajusta el alineamiento horizontal global

        message.value = ""
        email_input.value = ""
        password_input.value = ""

        col = ft.Column(
            [
                message, 
                email_input, 
                password_input, 
                ft.Row(
                    [
                        login_button,
                        ft.ElevatedButton("Registrarse", on_click=show_register)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Asegura que la columna esté centrada completamente
        )

        page.add(col)
        page.update()

    def register_page():
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
                register_message,
                register_name_input,
                register_email_input,
                register_password_input,
                register_repeat_password_input,
                ft.Row(
                    [
                        ft.ElevatedButton("Registrarse", on_click=register),
                        ft.ElevatedButton("Volver al Login", on_click=back_to_login)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(col)
        page.update()

    # Configuración inicial
    message = ft.Text(value="", size=20, color=ft.colors.GREEN)
    email_input = ft.TextField(label="Email", width=300)
    password_input = ft.TextField(label="Password", password=True, width=300)
    login_button = ft.ElevatedButton(text="Login", on_click=login)

    # Elementos para el registro
    register_message = ft.Text(value="", size=20)
    register_name_input = ft.TextField(label="Nombre completo", width=300)
    register_email_input = ft.TextField(label="Email", width=300)
    register_password_input = ft.TextField(label="Contraseña", password=True, width=300)
    register_repeat_password_input = ft.TextField(label="Repetir contraseña", password=True, width=300)

    # Manejo de rutas
    def route_change(route):
        if route.route == "/login":
            login_page()
        elif route.route == "/register":
            register_page()
        elif route.route == "/main":
            main_page()

    page.on_route_change = route_change  # Solo ejecuta la función de la página al cambiar de ruta
    page.go("/login")

ft.app(target=main)