import flet as ft
import requests
import webbrowser
from utils.constants import BASE_URL

def load_books(page, content_panel):
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
                    expand=True,
                )
                content_panel.controls.append(book_list)
        else:
            content_panel.controls.append(ft.Text("Error al cargar los libros.", size=20, color=ft.colors.RED))
    except Exception as e:
        content_panel.controls.append(ft.Text(f"Error: {e}", size=20, color=ft.colors.RED))
    content_panel.update()

def add_book_page(page, content_panel, user_email):
    content_panel.controls.clear()

    title_input = ft.TextField(label="Título del libro", width=300)
    message_label = ft.Text(value="", size=20, color=ft.colors.GREEN)

    def submit_book(e):
        title = title_input.value
        try:
            response = requests.post(
                f"{BASE_URL}/books/user",
                json={"email": user_email, "title": title},
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