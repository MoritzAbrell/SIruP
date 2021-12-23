import threading
import socket
import sys
import ssl
from sirup import var, logger, handler


def deamon(proto, port):
    if proto == "tcp":
        try:
            print("{} {} Starting TCP SIP deamon on Port {}".format(
                var.info, var.ts(), var.tcp_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("0.0.0.0", port))
            s.listen()
        except:
            print("{} {} An error occurred with TCP SIP deamon".format(
                var.error, var.ts()))
            proto = None

    if proto == "udp":
        try:
            print("{} {} Starting UDP SIP deamon on Port {}".format(
                var.info, var.ts(), var.udp_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(("0.0.0.0", port))
        except:
            print("{} {} An error occurred with UDP SIP deamon".format(
                var.error, var.ts()))
            proto = None

    if proto == "tls":
        try:
            print("{} {} Starting TLS SIP deamon on Port {}".format(
                var.info, var.ts(), var.tls_port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLS_SERVER, 
                                keyfile=var.key_path, certfile=var.cert_path)
            s.bind(("0.0.0.0", port))
            s.listen()
        except:
            print("{} {} An error occurred with TLS SIP deamon".format(
                var.error,
                var.ts()))
            proto = None

    while True:
        if proto == "tcp" or proto == "tls":
            connection, client_address = s.accept()
            if connection:
                session = threading.Thread(
                        target=tcp_session,
                        args=(connection, client_address, proto))
                session.deamon = True
                session.start()

        elif proto == "udp":
            connection, client_address = s.recvfrom(1024)
            data = connection
            logger.log(client_address[0])
            payload = handler.handler(client_address, data, proto)
            if payload:
                s.sendto(payload, client_address)

        else:
            print("{} {} Stopping deamon".format(var.error, var.ts()))
            break


def tcp_session(connection, client_address, proto):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            logger.log(client_address[0])
            payload = handler.handler(client_address, data, proto)
            if payload:
                connection.send(payload)
    finally:
        connection.close()


def start_server(proto, port):
    port = int(port)
    t = threading.Thread(target=deamon, args=(proto, port,))
    t.deamon = True
    t.start()


def init():
    print("{} {} Inititalize SIruP".format(var.info, var.ts()))

    print("{} {} Inititalize database".format(var.info, var.ts()))
    try:
        logger.db_init()
    except:
        print("{} {} Database error".format(var.error, var.ts()))
        sys.exit(1)

    if var.udp_enable == "True":
        start_server("udp", var.udp_port)

    if var.tcp_enable == "True":
        start_server("tcp", var.tcp_port)

    if var.tls_enable == "True":
        start_server("tls", var.tls_port)

    print("{} {} Inititalization completed".format(var.info, var.ts()))
