import json
import os

class Config:
    CONFIG_FILE = os.path.expanduser('~/.nocturne_config.json')
    
    _defaults = {
        'LANGUAGE': 'english',
        'EMOJIS': False,
        'MAX_WORKERS': 200,
        'USE_TOR': True,
        'TOR_ROTATION_INTERVAL': 30
    }
    
    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                for key, value in config.items():
                    if key in cls._defaults:
                        setattr(cls, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
                for key, value in cls._defaults.items():
                    setattr(cls, key, value)
        else:
            for key, value in cls._defaults.items():
                setattr(cls, key, value)
    
    @classmethod
    def save_config(cls):
        try:
            config = {}
            for key in cls._defaults:
                config[key] = getattr(cls, key, cls._defaults[key])
            
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

Config.load_config()

class Translator:
    def __init__(self):
        self.messages = {
            "spanish": {
                "settings_title": "CONFIGURACIÓN",
                "current_language": "Idioma actual",
                "use_tor": "Usar Tor",
                "yes": "Sí",
                "no": "No",
                "back_to_menu": "Volver al menú principal",
                "select_option": "Seleccione una opción",
                "enabled": "activado",
                "disabled": "desactivado",
                "banner": "HERRAMIENTA DE PRUEBAS DDOS, DOS, HTTP, TCP, SLOWLORIS, PORT SCANNER",
                "warning": "ADVERTENCIA: Usa solo en sistemas con autorización explícita",
                "warning_legal": "El mal uso de esta herramienta puede ser ilegal",
                "enter_target": "Ingresa URL o IP del objetivo",
                "select_attack": "SELECCIONA EL TIPO DE ATAQUE",
                "port_scan": "Escaneo de Puertos",
                "http_flood": "HTTP Flood",
                "tcp_flood": "TCP Flood",
                "slowloris": "Slowloris Attack",
                "ddos_sim": "DDoS",
                "option": "Opción (1-5)",
                "start_port": "Puerto inicial (default 1)",
                "end_port": "Puerto final (default 1000)",
                "num_requests": "Número de requests",
                "delay": "Delay entre requests (default 0.1)",
                "target_port": "Puerto objetivo",
                "num_connections": "Número de conexiones",
                "message": "Mensaje a enviar (opcional)",
                "num_sockets": "Número de sockets (default 150)",
                "duration": "Duración en segundos (default 60)",
                "restart": "¿Ejecutar otra prueba? (s/n)",
                "exiting": "Saliendo...",
                "error_no_target": "Error: Debes especificar un objetivo",
                "error_invalid_option": "Opción no válida",
                "error_general": "Error",
                "operation_cancelled": "Operación cancelada por el usuario",
                "scanning_ports": "Escaneando puertos {}-{} en {}",
                "port_open": "Puerto {} ABIERTO ({})",
                "scan_complete": "Escaneo completado. Puertos abiertos: {}",
                "starting_http_flood": "Iniciando HTTP Flood a {}",
                "sending_requests": "Enviando {} requests...",
                "request_success": "Request {}/{} - Status: {}",
                "request_warning": "Request {}/{} - Status: {}",
                "request_error": "Request {}/{} - Error: {}",
                "http_summary": "RESUMEN HTTP FLOOD",
                "successful_requests": "Requests exitosos",
                "failed_requests": "Requests fallidos",
                "main_menu": "MENÚ PRINCIPAL",
                "exit": "Salir",
                "port_scan_title": "ESCANEO DE PUERTOS",
                "http_flood_title": "INUNDACIÓN HTTP",
                "tcp_flood_title": "INUNDACIÓN TCP",
                "slowloris_title": "ATAQUE SLOWLORIS",
                "ddos_title": "ATAQUE DDoS",
                "enter_ip_or_domain": "Introduzca la dirección IP o el dominio:",
                "start_port_prompt": "Puerto de inicio (por defecto 1):",
                "end_port_prompt": "Puerto final (por defecto 1000):",
                "enter_url": "Introduzca la URL de destino (por ejemplo, http://example.com):",
                "num_requests_prompt": "Número de solicitudes:",
                "delay_prompt": "Tiempo entre peticiones en segundos (por defecto 0.1):",
                "enter_ip": "Introduzca la dirección IP de destino:",
                "port_prompt": "Puerto de destino:",
                "num_connections_prompt": "Número de conexiones:",
                "message_prompt": "Mensaje a enviar (opcional):",
                "num_sockets_prompt": "Número de sockets (por defecto 150):",
                "duration_prompt": "Duración en segundos (por defecto 60):",
                "scan_completed": "Escaneo completado. Puertos abiertos: {}",
                "starting_attack": "Iniciando ataque a {}",
                "app_terminated": "Aplicación terminada por el usuario",
                "critical_error": "Error crítico",
                "total_time": "Tiempo total",
                "requests_second": "Requests/segundo",
                "starting_tcp_flood": "Iniciando TCP Flood a {}:{}",
                "establishing_connections": "Estableciendo {} conexiones...",
                "connection_established": "Conexión {}: Establecida (Activas: {})",
                "connection_error_send": "Conexión {}: Error enviando - {}",
                "connection_failed": "Conexión {}: Falló - {}",
                "tcp_summary": "RESUMEN TCP FLOOD",
                "successful_connections": "Conexiones exitosas",
                "starting_slowloris": "Iniciando Slowloris a {}",
                "configuring_sockets": "Configurando {} sockets...",
                "sockets_connected": "{}/{} sockets conectados",
                "sockets_active": "{} sockets conectados y manteniendo conexiones...",
                "press_stop": "Presiona Ctrl+C para detener el ataque",
                "sockets_active_count": "Sockets activos: {}/{}",
                "all_sockets_closed": "Todos los sockets se han cerrado",
                "attack_stopped": "Ataque detenido por el usuario",
                "sockets_closed": "{} sockets cerrados",
                "socket_error": "Error en socket {}: {}",
                "starting_ddos": "Iniciando ataque DDoS a {} por {} segundos",
                "starting_workers": "Iniciando ataque con múltiples workers...",
                "worker_progress": "Worker {}: {} requests enviados",
                "time_elapsed": "Tiempo transcurrido: {}s, Requests: {} (~{}/s)",
                "attack_interrupted": "Ataque interrumpido",
                "ddos_summary": "RESUMEN DDoS",
                "total_requests": "Total requests",
                "result": "RESULTADO: {} puertos abiertos: {}"
            },
            "english": {
                "settings_title": "SETTINGS",
                "current_language": "Current language",
                "use_tor": "Use Tor",
                "yes": "Yes",
                "no": "No",
                "back_to_menu": "Back to main menu",
                "select_option": "Select an option",
                "enabled": "enabled",
                "disabled": "disabled",
                "banner": "LOAD TESTING DDOS, DOS, HTTP, TCP, SLOWLORIS, PORT SCANNER",
                "warning": "WARNING: Use only on systems with explicit authorization",
                "warning_legal": "Misuse of this tool may be illegal",
                "enter_target": "Enter target URL or IP",
                "select_attack": "SELECT ATTACK TYPE",
                "port_scan": "Port Scan",
                "http_flood": "HTTP Flood",
                "tcp_flood": "TCP Flood",
                "slowloris": "Slowloris Attack",
                "ddos_sim": "DDoS (Multiple techniques)",
                "option": "Option (1-5)",
                "start_port": "Start port (default 1)",
                "end_port": "End port (default 1000)",
                "num_requests": "Number of requests",
                "delay": "Delay between requests (default 0.1)",
                "target_port": "Target port",
                "num_connections": "Number of connections",
                "message": "Message to send (optional)",
                "num_sockets": "Number of sockets (default 150)",
                "duration": "Duration in seconds (default 60)",
                "restart": "Run another test? (y/n)",
                "exiting": "Exiting...",
                "error_no_target": "Error: You must specify a target",
                "error_invalid_option": "Invalid option",
                "error_general": "Error",
                "operation_cancelled": "Operation cancelled by user",
                "scanning_ports": "Scanning ports {}-{} on {}",
                "port_open": "Port {} OPEN ({})",
                "scan_complete": "Scan completed. Open ports: {}",
                "starting_http_flood": "Starting HTTP Flood to {}",
                "sending_requests": "Sending {} requests...",
                "request_success": "Request {}/{} - Status: {}",
                "request_warning": "Request {}/{} - Status: {}",
                "request_error": "Request {}/{} - Error: {}",
                "http_summary": "HTTP FLOOD SUMMARY",
                "successful_requests": "Successful requests",
                "failed_requests": "Failed requests",
                "main_menu": "MAIN MENU",
                "exit": "Exit",
                "port_scan_title": "PORT SCAN",
                "http_flood_title": "HTTP FLOOD",
                "tcp_flood_title": "TCP FLOOD",
                "slowloris_title": "SLOWLORIS",
                "ddos_title": "DDoS ATTACK",
                "enter_ip_or_domain": "Enter IP address or domain:",
                "start_port_prompt": "Start port (default 1):",
                "end_port_prompt": "End port (default 1000):",
                "enter_url": "Enter target URL (e.g., http://example.com):",
                "num_requests_prompt": "Number of requests:",
                "delay_prompt": "Time between requests in seconds (default 0.1):",
                "enter_ip": "Enter target IP address:",
                "port_prompt": "Target port:",
                "num_connections_prompt": "Number of connections:",
                "message_prompt": "Message to send (optional):",
                "num_sockets_prompt": "Number of sockets (default 150):",
                "duration_prompt": "Duration in seconds (default 60):",
                "scan_completed": "Scan completed. Open ports: {}",
                "starting_attack": "Starting attack to {}",
                "app_terminated": "Application terminated by user",
                "critical_error": "Critical error",
                "total_time": "Total time",
                "requests_second": "Requests/second",
                "starting_tcp_flood": "Starting TCP Flood to {}:{}",
                "establishing_connections": "Establishing {} connections...",
                "connection_established": "Connection {}: Established (Active: {})",
                "connection_error_send": "Connection {}: Send error - {}",
                "connection_failed": "Connection {}: Failed - {}",
                "tcp_summary": "TCP FLOOD SUMMARY",
                "successful_connections": "Successful connections",
                "starting_slowloris": "Starting Slowloris to {}",
                "configuring_sockets": "Configuring {} sockets...",
                "sockets_connected": "{}/{} sockets connected",
                "sockets_active": "{} sockets connected and maintaining connections...",
                "press_stop": "Press Ctrl+C to stop attack",
                "sockets_active_count": "Active sockets: {}/{}",
                "all_sockets_closed": "All sockets have been closed",
                "attack_stopped": "Attack stopped by user",
                "sockets_closed": "{} sockets closed",
                "socket_error": "Socket {} error: {}",
                "starting_ddos": "Starting DDoS attack to {} for {} seconds",
                "starting_workers": "Starting attack with multiple workers...",
                "worker_progress": "Worker {}: {} requests sent",
                "time_elapsed": "Time elapsed: {}s, Requests: {} (~{}/s)",
                "attack_interrupted": "Attack interrupted",
                "ddos_summary": "DDoS SUMMARY",
                "total_requests": "Total requests",
                "result": "RESULT: {} open ports: {}"
            }
        }

    def get(self, key):
        lang = getattr(Config, 'LANGUAGE', 'english')
        print(f"Language used: {lang}")
        return self.messages.get(lang, {}).get(key, self.messages['english'].get(key, key))

t = Translator()