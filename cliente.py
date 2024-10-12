import socket
import threading

def enviar_mensajes(cliente_socket):
    while True:
        mensaje = input("")
        cliente_socket.send(mensaje.encode('utf-8'))


def recibir_mensajes(cliente_socket):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            print(mensaje)
        except:
            print("Desconectado del servidor.")
            cliente_socket.close()
            break

def iniciar_cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(('127.0.0.1', 5555))

    nombre_usuario = input("Introduce tu nombre de usuario: ")
    cliente_socket.send(nombre_usuario.encode('utf-8'))

    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente_socket,))
    hilo_enviar = threading.Thread(target=enviar_mensajes, args=(cliente_socket,))

    hilo_recibir.start()
    hilo_enviar.start()

if __name__ == "__main__":
    iniciar_cliente()
