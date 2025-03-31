import flet as ft
from auth.login import login_page
from auth.register import register_page
from views.main_view import main_page
from views.admin_view import admin_page

def main(page: ft.Page):
    page.window_size = (1280, 720)
    page.window.always_on_top = True
    page.bgcolor = "#212121"
    # Manejo de rutas
    def route_change(route):
        if route.route == "/login":
            login_page(page)
        elif route.route == "/register":
            register_page(page)
        elif route.route == "/main":
            main_page(page)
        elif route.route == "/admin":
            admin_page(page)

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main)