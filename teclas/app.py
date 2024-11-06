from pynput import keyboard, mouse
from win10toast import ToastNotifier
import threading

teclas_pressionadas = 0
cliques_mouse = 0
listener_ativo = True  

def on_key_press(key):
    global teclas_pressionadas
    teclas_pressionadas += 1

    try:
        print(f"Tecla pressionada: {key.char}")
    except AttributeError:
        print(f"Tecla especial pressionada: {key}")

def on_key_release(key):
    global listener_ativo
 
    if key == keyboard.Key.end:
        print("Tecla END pressionada, encerrando...")
        listener_ativo = False  
        return False


def on_click(x, y, button, pressed):
    global cliques_mouse
    if pressed:
        cliques_mouse += 1
        print(f"Botão {button} pressionado em ({x}, {y})")

def on_move(x, y):
    pass 


def mostrar_notificacao():
    toaster = ToastNotifier()
    toaster.show_toast("Contador de teclas e cliques", 
                       f"Teclas pressionadas: {teclas_pressionadas}\nCliques do mouse: {cliques_mouse}", 
                       duration=10)


def iniciar_listener_teclado():
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

def iniciar_listener_mouse():
    global listener_ativo
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        while listener_ativo: 
            pass  
        listener.stop()     

def main():

    teclado_thread = threading.Thread(target=iniciar_listener_teclado)
    mouse_thread = threading.Thread(target=iniciar_listener_mouse)
    
    teclado_thread.start()
    mouse_thread.start()

    print("O programa está rodando. Pressione 'END' para parar.")

    teclado_thread.join()
    mouse_thread.join()

    mostrar_notificacao()

if __name__ == "__main__":
    main()
