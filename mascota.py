import math

class Mascota:
    """
    Clase que representa a la mascota virtual.
    Maneja sus estadísticas y cambios de estado a lo largo del tiempo.
    """

    def __init__(self, nombre: str):
        """
        Inicializa una nueva mascota con estadísticas base.
        
        Args:
            nombre (str): El nombre de la mascota.
        """
        self.nombre = nombre
        # Estadísticas iniciales (0.0 a 100.0)
        self._hambre = 50.0      # 0: Sin hambre, 100: Muy hambriento
        self._energia = 100.0    # 0: Agotado, 100: Lleno de energía
        self._felicidad = 100.0  # 0: Triste, 100: Muy feliz
        self._suciedad = 0.0     # 0: Limpio, 100: Muy sucio

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

    def update(self, delta_time: float):
        """
        Actualiza las estadísticas de la mascota basado en el tiempo transcurrido.
        
        Args:
            delta_time (float): Tiempo transcurrido en segundos desde la última actualización.
        """
        # Tasas de cambio por segundo
        tasa_hambre = 2.0      # Aumenta hambre
        tasa_cansancio = 0.5   # Disminuye energía
        tasa_aburrimiento = 1.0 # Disminuye felicidad
        tasa_suciedad = 0.2    # Aumenta suciedad

        self.hambre += tasa_hambre * delta_time
        self.energia -= tasa_cansancio * delta_time
        self.felicidad -= tasa_aburrimiento * delta_time
        self.suciedad += tasa_suciedad * delta_time

        # Penalizaciones adicionales
        if self.hambre > 80 or self.suciedad > 80:
            self.felicidad -= 2.0 * delta_time
        
        if self.energia < 20:
            self.felicidad -= 1.0 * delta_time

    def alimentar(self):
        """Alimenta a la mascota. Reduce hambre, aumenta un poco la suciedad."""
        self.hambre -= 30
        self.suciedad += 5
        self.energia += 5
        print(f"{self.nombre} ha comido.")

    def jugar(self):
        """Juega con la mascota. Aumenta felicidad, reduce energía, aumenta hambre."""
        if self.energia > 10:
            self.felicidad += 20
            self.energia -= 15
            self.hambre += 10
            self.suciedad += 5
            print(f"{self.nombre} ha jugado.")
        else:
            print(f"{self.nombre} está demasiado cansado para jugar.")

    def limpiar(self):
        """Limpia a la mascota. Reduce suciedad, puede reducir un poco felicidad si no le gusta."""
        self.suciedad = 0
        self.felicidad -= 5 # A veces no les gusta bañarse
        print(f"{self.nombre} ha sido bañado.")

    def dormir(self):
        """Pone a dormir a la mascota. Recupera energía, aumenta hambre considerablemente."""
        self.energia += 50
        self.hambre += 10
        print(f"{self.nombre} ha dormido.")

    def obtener_estado(self) -> str:
        """Devuelve una descripción textual del estado general."""
        estados = []
        if self.hambre > 70:
            estados.append("Hambriento")
        if self.energia < 30:
            estados.append("Cansado")
        if self.felicidad < 40:
            estados.append("Triste")
        if self.suciedad > 60:
            estados.append("Sucio")
        
        if not estados:
            return "Feliz y Saludable"
        
        return ", ".join(estados)
