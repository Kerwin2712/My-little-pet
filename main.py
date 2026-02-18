import arcade
from mascota import Mascota

# Constantes de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mi Pequeña Mascota"

# Colores para las barras
COLOR_HAMBRE = arcade.color.RED
COLOR_ENERGIA = arcade.color.YELLOW
COLOR_FELICIDAD = arcade.color.GREEN
COLOR_SUCIEDAD = arcade.color.BROWN

class MyGame(arcade.Window):
    """
    Clase principal del juego.
    """

    def __init__(self):
        """ Inicializador """
        # Llamar al inicializador de la clase padre
        # Habilitar redimensionado de ventana
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Fondo
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Instancia de la mascota
        self.mascota = None

    def setup(self):
        """ Configuración del juego y variables """
        self.mascota = Mascota("Bolita")

    def on_draw(self):
        """ Renderizado """
        # Limpiar la pantalla
        self.clear()

        # Dimensiones actuales de la ventana
        screen_w = self.width
        screen_h = self.height

        # --- Dibujar barras de estado (Esquina inferior izquierda) ---
        # Margen desde abajo izquierda
        margin_x = 20
        margin_y = 20
        bar_height = 20
        bar_width = 200
        spacing = 30

        # Calculamos la base Y para las 4 barras para que crezcan hacia arriba
        # Orden de abajo hacia arriba: Hambre, Energía, Felicidad, Suciedad (o al revés, como prefieras)
        # Vamos a dibujarlas de arriba hacia abajo empezando desde una posición base calculada
        # O mejor, apilarlas desde abajo:
        
        current_y = margin_y

        # Hambre
        arcade.draw_text("Hambre:", margin_x, current_y, arcade.color.BLACK, 14)
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, bar_width, bar_height, arcade.color.GRAY)
        width_hambre = (self.mascota.hambre / 100) * bar_width
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, width_hambre, bar_height, COLOR_HAMBRE)
        current_y += spacing

        # Energía
        arcade.draw_text("Energía:", margin_x, current_y, arcade.color.BLACK, 14)
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, bar_width, bar_height, arcade.color.GRAY)
        width_energia = (self.mascota.energia / 100) * bar_width
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, width_energia, bar_height, COLOR_ENERGIA)
        current_y += spacing

        # Felicidad
        arcade.draw_text("Felicidad:", margin_x, current_y, arcade.color.BLACK, 14)
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, bar_width, bar_height, arcade.color.GRAY)
        width_felicidad = (self.mascota.felicidad / 100) * bar_width
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, width_felicidad, bar_height, COLOR_FELICIDAD)
        current_y += spacing

        # Suciedad
        arcade.draw_text("Suciedad:", margin_x, current_y, arcade.color.BLACK, 14)
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, bar_width, bar_height, arcade.color.GRAY)
        width_suciedad = (self.mascota.suciedad / 100) * bar_width
        arcade.draw_lbwh_rectangle_filled(margin_x + 80, current_y, width_suciedad, bar_height, COLOR_SUCIEDAD)

        # --- Dibujar estado general (Esquina superior izquierda) ---
        estado_texto = f"Estado: {self.mascota.obtener_estado()}"
        arcade.draw_text(estado_texto, 20, screen_h - 40, arcade.color.BLACK, 20, anchor_x="left")

        # --- Dibujar instrucciones (Parte superior central) ---
        instrucciones = "F: Alimentar | J: Jugar | L: Limpiar | D: Dormir"
        arcade.draw_text(instrucciones, screen_w / 2, screen_h - 80, arcade.color.DARK_BLUE, 16, anchor_x="center")

        # --- Dibujar Mascota (Centro de la pantalla) ---
        center_x = screen_w / 2
        center_y = screen_h / 2
        
        # Cuerpo
        arcade.draw_circle_filled(center_x, center_y, 50, arcade.color.WHITE)
        arcade.draw_circle_outline(center_x, center_y, 50, arcade.color.BLACK, 2)
        # Ojos
        arcade.draw_circle_filled(center_x - 15, center_y + 10, 5, arcade.color.BLACK)
        arcade.draw_circle_filled(center_x + 15, center_y + 10, 5, arcade.color.BLACK)
        # Boca (cambia según felicidad)
        if self.mascota.felicidad > 50:
             # Sonrisa
             arcade.draw_arc_outline(center_x, center_y - 5, 20, 10, arcade.color.BLACK, 180, 360, 2)
        else:
             # Triste / Serio
             arcade.draw_arc_outline(center_x, center_y - 15, 20, 10, arcade.color.BLACK, 0, 180, 2)


    def on_update(self, delta_time):
        """ Movimiento y lógica de juego """
        self.mascota.update(delta_time)

    def on_key_press(self, key, modifiers):
        """ Llamado cuando se presiona una tecla """
        if key == arcade.key.F:
            self.mascota.alimentar()
        elif key == arcade.key.J:
            self.mascota.jugar()
        elif key == arcade.key.L:
            self.mascota.limpiar()
        elif key == arcade.key.D:
            self.mascota.dormir()

def main():
    """ Función principal """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
