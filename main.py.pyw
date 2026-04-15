import flet as ft
import urllib.parse
import os

def main(page: ft.Page):
    # --- RUTA DE ASSETS ---
    current_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = os.path.join(current_dir, "assets")
    
    if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
        page.assets_dir = assets_dir
    
    # --- ESTILO GENERAL ---
    page.title = "La Caserita de las camisetas"
    page.bgcolor = "#FDFCFB" 
    page.padding = 10 

    ROSA_PALO = "#F48FB1"
    ORO_ROSADO = "#C5A059"
    COLOR_TEXTO = "#4A4A4A"
    COLOR_FONDO_RESUMEN = "#FFFFFFFF"

    carrito = {} 

    def actualizar_lista():
        detalle.controls.clear()
        total = 0
        for nombre, datos in carrito.items():
            if datos["cantidad"] > 0:
                sub = datos["precio"] * datos["cantidad"]
                total += sub
                precio_f = f"${sub:,.0f}".replace(",", ".")
                
                detalle.controls.append(
                    ft.Text(f"{int(datos['cantidad'])}x {nombre} = {precio_f}", 
                            color=COLOR_TEXTO, size=16, weight="bold")
                )
        
        lbl_total.value = f"Total: ${total:,.0f}".replace(",", ".")
        page.update()

    def sumar(nombre, precio):
        if nombre not in carrito:
            carrito[nombre] = {"precio": float(precio), "cantidad": 0}
        carrito[nombre]["cantidad"] += 1
        actualizar_lista()

    def restar(nombre, precio):
        if nombre in carrito and carrito[nombre]["cantidad"] > 0:
            carrito[nombre]["cantidad"] -= 1
        actualizar_lista()

    def borrar_todo(e):
        carrito.clear()
        actualizar_lista()

    def enviar_wa(e):
        msg = "*Pedido La Caserita de las camisetas*\n--------------------------\n"
        hay_algo = False
        for n, d in carrito.items():
            if d["cantidad"] > 0:
                msg += f"- {n} (x{int(d['cantidad'])})\n"
                hay_algo = True
        
        if not hay_algo: return
        
        msg += f"--------------------------\n*TOTAL: {lbl_total.value}*"
        page.launch_url(f"https://wa.me/?text={urllib.parse.quote(msg)}")

    def crear_item(nombre, precio, imagen):
        return ft.Container(
            content=ft.Column([
                ft.Image(src=f"/{imagen}", width=70, height=70, fit="contain"),
                ft.Text(nombre, weight="bold", size=12, text_align="center", color=ROSA_PALO),
                ft.Text(f"${precio:,.0f}".replace(",", "."), color=ORO_ROSADO, weight="bold"),
                ft.Row([
                    ft.Container(
                        content=ft.Text("-", color="white", weight="bold", size=20, text_align="center"),
                        bgcolor="#EF9A9A", padding=10, border_radius=5, width=45,
                        on_click=lambda _: restar(nombre, precio),
                    ),
                    ft.Container(width=10),
                    ft.Container(
                        content=ft.Text("+", color="white", weight="bold", size=20, text_align="center"),
                        bgcolor="#81C784", padding=10, border_radius=5, width=45,
                        on_click=lambda _: sumar(nombre, precio),
                    ),
                ], alignment="center")
            ], horizontal_alignment="center", spacing=5),
            bgcolor="white", padding=15, border_radius=15, border=ft.border.all(1, "#E1BEE7"), width=150
        )

    lbl_total = ft.Text("Total: $0", size=28, weight="bold", color=ORO_ROSADO)
    
    # --- DETALLE CON SCROLL ACTIVO ---
    detalle = ft.Column(scroll="auto")

    grid = ft.Row(
        wrap=True, alignment="center", spacing=10,
        controls=[
            crear_item("Camiseta 2 a 12", 3000, "camiseta.png"),
            crear_item("Camiseta Adulto", 3000, "camiseta.png"),
            crear_item("Calzoncillo 2 a 12", 3000, "calzoncillo.png"),
            crear_item("Calzoncillo Adulto", 3000, "calzoncillo.png"),
        ]
    )

    page.add(
        ft.Stack([
            ft.Image(src="/fondo.jpg", width=page.width, height=page.height, fit="cover", opacity=0.4),

            ft.Column([
                ft.Container(height=20),
                ft.Image(src="/logo.png", width=100),
                ft.Text("LA CASERITA DE LAS CAMISETAS", size=26, weight="bold", color=ROSA_PALO),
                
                ft.Container(height=9),
                grid,
                
                ft.Container(height=9),
                ft.Text("RESUMEN DE TU SELECCIÓN", weight="bold", color=COLOR_TEXTO),
                
                # --- CONTENEDOR CON ALTURA FIJA ---
                ft.Container(
                    content=detalle,
                    bgcolor=COLOR_FONDO_RESUMEN,
                    padding=15,
                    border_radius=30,
                    height=100, # Altura fija para que no empuje los botones
                    width=300,
                    border=ft.border.all(1, "#F7F0E0"),
                ),
                
                lbl_total,
                
                ft.Row([
                    ft.ElevatedButton("LIMPIAR TODO", on_click=borrar_todo, bgcolor="#E1BEE7", color="#7B1FA2", icon="DELETE"),
                    ft.ElevatedButton("ENVIAR PEDIDO", on_click=enviar_wa, bgcolor="#A5D6A7", color="#2E7D32", icon="SEND"),
                ], alignment="center", spacing=25),
                
                ft.Container(height=30)
            ], horizontal_alignment="center", scroll="adaptive")
        ])
    )

ft.app(target=main)