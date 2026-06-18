🧟 Project Zomshot
¡Bienvenido a Zomshot! Un emocionante juego arcade en 2D desarrollado en Python utilizando la librería Pygame. 
Enfréntate a hordas de zombies dinámicos, destruye barriles explosivos, recolecta Power-Ups y sobrevive lo suficiente para derrotar al temible Jefe Final. 

El juego cuenta con soporte bilingüe (Español/Inglés) y un sistema dinámico de efectos visuales como sacudidas de pantalla (screen shake) y partículas.

🎮 Características Principales
Sistema de Combate Avanzado: 
Disparos normales, ráfagas triples y mecánicas de disparo cargado manteniendo presionado el clic derecho.
Habilidades Especiales: 
Activa un escudo protector temporizado o desata ráfagas de hielo para congelar a los enemigos.
Enemigos Dinámicos: 
Zombies comunes, rápidos con trayectoria sinusoidal y un Jefe Final con patrones de ataque (Dash y proyectiles).
Efectos Jugosos (Juiciness): 
Sistema de partículas de sangre/explosiones y movimientos de cámara al recibir daño o detonar barriles.
Cine de Victoria: 
Al ganar, el juego reproduce un video de fondo dinámico utilizando OpenCV.
Persistencia: 
Guarda automáticamente tu puntuación más alta (highscore.txt).

🛠️ Requisitos e Instalación
Para ejecutar este proyecto, asegúrate de tener instalado Python 3.x y las siguientes librerías:Bashpip install pygame opencv-python
📁 Estructura del Proyecto
Para que el juego funcione correctamente, los recursos deben estar organizados de la siguiente manera:Plaintext├── main.py                # Archivo principal del juego
├── objetos.py             # Lógica de clases (Jugador, Enemigos, Balas, etc.)
├── constantes.py          # Configuraciones y rutas de recursos
├── highscore.txt          # Se genera automáticamente para el récord
├── images/                # Iconos, fondos y sprites obligatorios
│   ├── icon.png, menu_icon.png, menu_background.png, backgroundpatio.jpeg
│   ├── player.png, disparo.png, bone.png, enemigo.png, enemigo2.png, boss1.png
│   ├── botiquin.webp, iceball.png, barrel.png, triple_bullet.png, shield.png
│   └── victory.mp4        # Video reproducido en la pantalla de victoria
└── sounds/                # Efectos de sonido y música ambiental
    ├── disparo.mp3, shouting.mp3, shouting2.mp3, boss_enojado.mp3
    └── background.mp3, boss_music.mp3, victory_sound.mp3, gameover_sound.mp3, menu.mp3

    
🕹️ Controles del Juego

Puedes alternar el idioma entre Español e Inglés directamente desde el menú de Ajustes (Settings).
Acción-Control-Movimiento: W, A, S, D o Flechas Direccionales
Apuntar: Movimiento del Ratón (Mouse)
Disparo Normal: Clic Izquierdo
Disparo Cargado: Mantener Clic Derecho (1 segundo) y soltar
Escudo Protector: Tecla Q (Cooldown: 40s)
Ráfaga de Hielo: Tecla E (Requiere ítem activo)
Triple Disparo: Tecla Shift Izquierdo (Cooldown: 50s)
Reiniciar Juego: Tecla R (Solo en pantalla de Victoria/Game Over)🚀

Cómo Ejecutar el Juego
Simplemente corre el script principal desde tu terminal:Bashpython main.py
👥 Créditos 
Desarrollador Principal: ashlyrgg 🚀Desarrollado con fines educativos y de entretenimiento. ¡Espero que te diviertas jugándolo!
