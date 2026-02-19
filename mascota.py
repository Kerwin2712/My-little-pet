import arcade

# Constantes de animación
SCALE = 0.5
TEXTURE_width = 256
TEXTURE_height = 256
COLUMNS = 4
ROWS = 4

class Mascota(arcade.Sprite):
    """
    Clase que representa a la mascota virtual, ahora como un Sprite animado.
    Maneja sus estadísticas y cambios de estado a lo largo del tiempo.
    """

    def __init__(self, nombre: str, center_x: float, center_y: float):
        """
        Inicializa una nueva mascota con estadísticas base y carga de sprites.
        
        Args:
            nombre (str): El nombre de la mascota.
            center_x (float): Posición inicial X.
            center_y (float): Posición inicial Y.
        """
        super().__init__(scale=SCALE)
        
        self.nombre = nombre
        self.center_x = center_x
        self.center_y = center_y

        # Estadísticas iniciales (0.0 a 100.0)
        self._hambre = 50.0
        self._energia = 100.0
        self._felicidad = 100.0
        self._suciedad = 0.0

        # Carga de texturas
        self.idle_textures = []
        self.jump_textures = []
        
        # Cargar hoja de sprites
        # Asumimos que la hoja es de 4x4. Total 16 frames.
        # Row 0: Idle (4 frames)
        # Row 1: Walk (4 frames) - No usaremos Walk por ahora, solo Idle y Salto
        # Row 2: Jump (4 frames) 
        # Row 3: Other
        
        sheet = arcade.load_spritesheet("images/perro.png")
        texture_list = sheet.get_texture_grid(
            size=(TEXTURE_width, TEXTURE_height),
            columns=COLUMNS,
            count=COLUMNS * ROWS
        )

        # Dividir texturas por filas (suponiendo orden lineal: 0-3 fila 1, 4-7 fila 2, etc.)
        # Según feedback corregido: 
        # Idle: Primeras 2 columnas (Indices 0, 1)
        # Jump/Play: Últimas 2 columnas (Indices 2, 3)
        self.idle_textures = texture_list[2:4]
        self.jump_textures = texture_list[0:2] 

        # Estado inicial de animación
        self.cur_texture = 0
        self.texture = self.idle_textures[0]
        self.time_since_last_swap = 0.0
        self.is_jumping = False
        
        # Hit box
        # self.set_hit_box(self.texture.hit_box_points)

    @property
    def hambre(self) -> float:
        return self._hambre

    @hambre.setter
    def hambre(self, valor: float):
        self._hambre = max(0.0, min(100.0, valor))

    @property
    def energia(self) -> float:
        return self._energia

    @energia.setter
    def energia(self, valor: float):
        self._energia = max(0.0, min(100.0, valor))

    @property
    def felicidad(self) -> float:
        return self._felicidad

    @felicidad.setter
    def felicidad(self, valor: float):
        self._felicidad = max(0.0, min(100.0, valor))

    @property
    def suciedad(self) -> float:
        return self._suciedad

    @suciedad.setter
    def suciedad(self, valor: float):
        self._suciedad = max(0.0, min(100.0, valor))

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Actualiza la textura actual para la animación.
        """
        self.time_since_last_swap += delta_time
        
        # Velocidad de animación
        time_per_frame = 0.15
        
        if self.time_since_last_swap > time_per_frame:
            self.time_since_last_swap = 0
            self.cur_texture += 1
            
            if self.is_jumping:
                if self.cur_texture >= len(self.jump_textures):
                    self.cur_texture = 0
                    self.is_jumping = False # Terminar salto al finalizar ciclo (opcional)
                self.texture = self.jump_textures[self.cur_texture]
            else:
                if self.cur_texture >= len(self.idle_textures):
                    self.cur_texture = 0
                self.texture = self.idle_textures[self.cur_texture]

    def update(self, delta_time: float):
        """
        Actualiza lógica y animación.
        """
        # Actualizar animación
        self.update_animation(delta_time)
        
        # Tasas de cambio por segundo
        tasa_hambre = 2.0
        tasa_cansancio = 0.5
        tasa_aburrimiento = 1.0
        tasa_suciedad = 0.2

        self.hambre += tasa_hambre * delta_time
        self.energia -= tasa_cansancio * delta_time
        self.felicidad -= tasa_aburrimiento * delta_time
        self.suciedad += tasa_suciedad * delta_time

        if self.hambre > 80 or self.suciedad > 80:
            self.felicidad -= 2.0 * delta_time
        
        if self.energia < 20:
            self.felicidad -= 1.0 * delta_time

    def alimentar(self):
        self.hambre -= 30
        self.suciedad += 5
        self.energia += 5
        print(f"{self.nombre} ha comido.")

    def jugar(self):
        if self.energia > 10:
            self.felicidad += 20
            self.energia -= 15
            self.hambre += 10
            self.suciedad += 5
            self.is_jumping = True # Activar animación de salto al jugar
            print(f"{self.nombre} ha jugado.")
        else:
            print(f"{self.nombre} está demasiado cansado para jugar.")

    def limpiar(self):
        self.suciedad = 0
        self.felicidad -= 5
        print(f"{self.nombre} ha sido bañado.")

    def dormir(self):
        self.energia += 50
        self.hambre += 10
        print(f"{self.nombre} ha dormido.")

    def saltar(self):
        """Inicia la animación de salto."""
        if not self.is_jumping:
            self.is_jumping = True
            self.cur_texture = 0

    def obtener_estado(self) -> str:
        estados = []
        if self.hambre > 70: estados.append("Hambriento")
        if self.energia < 30: estados.append("Cansado")
        if self.felicidad < 40: estados.append("Triste")
        if self.suciedad > 60: estados.append("Sucio")
        
        if not estados: return "Feliz y Saludable"
        return ", ".join(estados)
