import pygame
from pynput import keyboard
from spike import PrimeHub, Motor
from spike.control import wait_for_seconds

# Inicializar o Pygame e o controlador PS4
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Inicializar o Hub e motores do LEGO SPIKE Prime
hub = PrimeHub()
motor_left = Motor('A')
motor_right = Motor('B')

# Função para controlar o carrinho com base nas entradas do teclado
def on_press(key):
    try:
        if key == keyboard.Key.up:
            motor_left.start(100)
            motor_right.start(100)
        elif key == keyboard.Key.down:
            motor_left.start(-100)
            motor_right.start(-100)
        elif key == keyboard.Key.left:
            motor_left.start(-100)
            motor_right.start(100)
        elif key == keyboard.Key.right:
            motor_left.start(100)
            motor_right.start(-100)
    except AttributeError:
        pass

def on_release(key):
    if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
        motor_left.stop()
        motor_right.stop()

# Configurar o controle do PS4
def handle_ps4_input():
    while True:
        pygame.event.pump()
        left_y = joystick.get_axis(1)
        left_x = joystick.get_axis(0)

        if left_y > 0.1:
            motor_left.start(100)
            motor_right.start(100)
        elif left_y < -0.1:
            motor_left.start(-100)
            motor_right.start(-100)
        elif left_x < -0.1:
            motor_left.start(-100)
            motor_right.start(100)
        elif left_x > 0.1:
            motor_left.start(100)
            motor_right.start(-100)
        else:
            motor_left.stop()
            motor_right.stop()

# Configurar o listener do teclado
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Iniciar o loop de controle do PS4
handle_ps4_input()
