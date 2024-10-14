import flet as ft
import os

# Palabra que el jugador debe adivinar
word_to_guess = "Hola Mundo"

# Crear una lista con guiones bajos que ocultan la palabra a adivinar
hidden_word = ["_"] * len(word_to_guess)
max_attempts = 7
attempts_left = max_attempts

# Verifica que la ruta de las imágenes sea correcta
base_image_path = "Hangman_game"
hangman_images = [
    os.path.join(base_image_path, f"{i}.png") for i in range(8)
]

# Función para crear botones de letras
def create_letter_button(letter, page, hidden_word_display, hangman_image_display, message_display):
    def on_click(e):
        global attempts_left
        e.control.disabled = True  # Deshabilitar el botón después de ser clickeado
        e.control.update()  # Actualizar la vista del botón

        if letter in word_to_guess:
            # Si la letra está en la palabra, actualizamos la palabra oculta
            for idx, char in enumerate(word_to_guess):
                if char == letter:
                    hidden_word[idx] = letter

            hidden_word_display.value = " ".join(hidden_word)  # Actualizar el texto mostrado
            hidden_word_display.update()

            # Si ya no quedan guiones bajos, el jugador ha ganado
            if "_" not in hidden_word:
                message_display.value = "¡Felicidades, has ganado!"
                message_display.update()
                disable_all_buttons(page)
        else:
            # Si la letra no está en la palabra, disminuimos los intentos restantes
            attempts_left -= 1
            # Actualizamos la imagen del ahorcado
            hangman_image_display.src = hangman_images[max_attempts - attempts_left]
            hangman_image_display.update()

            # Si se quedan sin intentos, el jugador pierde
            if attempts_left == 0:
                message_display.value = "Has perdido"
                message_display.update()
                disable_all_buttons(page)

    return ft.ElevatedButton(letter, on_click=on_click)

# Función para deshabilitar todos los botones cuando el juego termina
def disable_all_buttons(page):
    for control in page.controls[1].controls:  # Acceder a la fila de botones de letras
        control.disabled = True
    page.update()

# Función principal de la aplicación
def main(page: ft.Page):
    # Definir título de la aplicación
    page.title = "Hangman"

    # Mostrar la palabra oculta
    hidden_word_display = ft.Text(" ".join(hidden_word), size=30)

    # Mostrar la imagen inicial del ahorcado
    hangman_image_display = ft.Image(src=hangman_images[0], width=500, height=500)

    # Mostrar mensajes de estado (ganar o perder)
    message_display = ft.Text("", size=20, color="red")

    # Crear los botones de las letras
    alphabet = "abcdefghijklmnñopqrstuvwxyz"
    letter_buttons = [
        create_letter_button(letter, page, hidden_word_display, hangman_image_display, message_display)
        for letter in alphabet
    ]

    # Añadir los elementos a la página
    page.add(
        hidden_word_display,
        ft.Row(controls=letter_buttons, wrap=True, spacing=5),  # Botones en filas con ajuste de línea
        hangman_image_display,
        message_display
    )

# Ejecutar la aplicación
ft.app(target=main)
