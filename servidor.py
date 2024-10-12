import socket
import threading

clientes = {}

def manejar_cliente(cliente_socket, cliente_direccion):
    nombre_usuario = cliente_socket.recv(1024).decode('utf-8')
    clientes[cliente_socket] = nombre_usuario
    print(f"{nombre_usuario} se ha unido desde {cliente_direccion}")
    
    difundir_mensaje(f"{nombre_usuario} se ha unido al chat.", cliente_socket)

    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')

            if mensaje.startswith("!list_users"):
                listar_usuarios(cliente_socket)
            elif mensaje.startswith("!send_to"):
                partes = mensaje.split(' ', 2)
                if len(partes) >= 3:
                    nombre_destinatario = partes[1].replace('"', '') 
                    mensaje_privado = partes[2].replace('"', '')
                    enviar_mensaje_privado(nombre_usuario, nombre_destinatario, mensaje_privado, cliente_socket)
                else:
                    cliente_socket.send("Formato incorrecto. Usa !send_to \"nombre_usuario\" \"mensaje\".\n".encode('utf-8'))
            else:
                mensaje_con_nombre = f"{nombre_usuario}: {mensaje}"
                difundir_mensaje(mensaje_con_nombre, cliente_socket)

        except:
            print(f"{nombre_usuario} se ha desconectado.")
            clientes.pop(cliente_socket)
            cliente_socket.close()
            difundir_mensaje(f"{nombre_usuario} ha salido del chat.", cliente_socket)
            break

def listar_usuarios(cliente_socket):
    usuarios = [nombre for nombre in clientes.values()]
    lista_usuarios = "Usuarios conectados: " + ", ".join(usuarios) + "\n"
    cliente_socket.send(lista_usuarios.encode('utf-8'))

def enviar_mensaje_privado(nombre_emisor, nombre_destinatario, mensaje_privado, cliente_socket):
    encontrado = False
    for cliente, nombre in clientes.items():
        if nombre == nombre_destinatario:
            cliente.send(f"Mensaje privado de {nombre_emisor}: {mensaje_privado}\n".encode('utf-8'))
            cliente_socket.send(f"Mensaje enviado a {nombre_destinatario}.\n".encode('utf-8'))
            encontrado = True
            break
    if not encontrado:
        cliente_socket.send(f"Usuario {nombre_destinatario} no encontrado.\n".encode('utf-8'))
        
def difundir_mensaje(mensaje, cliente_socket):
    for cliente in clientes:
        if cliente != cliente_socket:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                cliente.close()
                clientes.pop(cliente)

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('127.0.0.1', 5555)) 
    servidor.listen()
    print("Servidor escuchando en 127.0.0.1:5555")

    while True:
        cliente_socket, cliente_direccion = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(cliente_socket, cliente_direccion))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
