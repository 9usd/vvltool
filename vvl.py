import os
import time
import urllib.parse
import requests
import sqlite3
import socket
from concurrent.futures import ThreadPoolExecutor

API_KEY = "e871f5f9e8eb784652acc579cbf7e912"  # vvl32

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    MAGENTA = '\033[95m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"""{Colors.BLUE}
    
               ╔════════════════════════════════════════════════╗
               ║      vvltool v 1.0 credits: @shootmamont       ║
               ╚════════════════════════════════════════════════╝
               
 {Colors.RESET}""")

def print_menu():
    print(f"""{Colors.BLUE}
        ╔══════════════════════════════╗╔══════════════════════════════╗
        ║            Choose            ║║            Choose            ║
        ╠══════════════════════════════╣╠══════════════════════════════╣
        ║ {Colors.GREEN}1{Colors.BLUE} — UserName Search          ║║ {Colors.GREEN}7{Colors.BLUE} — WHOIS Domain/IP Analisys ║
        ║ {Colors.GREEN}2{Colors.BLUE} — IP Address Info          ║║ {Colors.GREEN}8{Colors.BLUE} — IP Ports Scanner         ║
        ║ {Colors.GREEN}3{Colors.BLUE} — Phone Number Lookup      ║║ {Colors.GREEN}9{Colors.BLUE} — Soon                     ║
        ║ {Colors.GREEN}4{Colors.BLUE} — Discord Acc Info         ║║ {Colors.GREEN}10{Colors.BLUE} — Soon                    ║
        ║ {Colors.GREEN}5{Colors.BLUE} — Search by DataBase       ║║ {Colors.GREEN}11{Colors.BLUE} — Soon                    ║
        ║ {Colors.GREEN}6{Colors.BLUE} — Email Checker for Leaks  ║║ {Colors.GREEN}12{Colors.BLUE} — Soon                    ║
        ╠══════════════════════════════╣╠══════════════════════════════╣
        ║ {Colors.CYAN}0{Colors.BLUE} — {Colors.RED}Exit{Colors.CYAN}                     ║║ {Colors.CYAN}by{Colors.BLUE} — {Colors.CYAN}@vvl32                  ║
        ╚══════════════════════════════╝╚══════════════════════════════╝
        
{Colors.RESET}""")  

def generate_ip_link(user_input):
    base_url = "https://whatismyipaddress.com/ip/"
    return f"{base_url}{user_input}"

def generate_social_links(nickname):
    encoded_query = urllib.parse.quote(nickname)
    links = {
        "Twitter": f"https://twitter.com/search?q={encoded_query}",
        "Reddit": f"https://www.reddit.com/search/?q={encoded_query}",
        "YouTube": f"https://www.youtube.com/results?search_query={encoded_query}",
        "TikTok": f"https://www.google.com/search?q=site%3Atiktok.com+{encoded_query}",
        "Instagram": f"https://www.google.com/search?q=site%3Ainstagram.com+{encoded_query}",
        "Facebook": f"https://www.google.com/search?q=site%3Afacebook.com+{encoded_query}",
        "VK": f"https://www.google.com/search?q=site%3Avk.com+{encoded_query}",
        "Telegram": f"https://www.google.com/search?q=site%3At.me+{encoded_query}",
    }
    return links

def hlr_lookup(phone_number):
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}&format=1"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("valid"):
            print(f"\n{Colors.BLUE}Номер валиден:{Colors.RESET}")
            print(f"{Colors.BLUE} Страна: {Colors.RESET}{data.get('country_name')}")
            print(f"{Colors.BLUE} Оператор: {Colors.RESET}{data.get('carrier')}")
            print(f"{Colors.BLUE} Код страны: {Colors.RESET}+{data.get('country_code')}")
            print(f"{Colors.BLUE}Локальный формат: {Colors.RESET}{data.get('local_format')}")
        else:
            print(f"{Colors.RED} Номер недействителен или недоступен.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED} Ошибка при запросе HLR: {e}{Colors.RESET}")

API_KEY = "your api key"

def discord_osint(discord_input):
    def is_discord_id(value):
        return value.isdigit() and len(value) >= 17

    if not is_discord_id(discord_input):
        print(f"{Colors.RED} Ошибка: Введите корректный Discord User ID (только цифры).{Colors.RESET}")
        return

    url = f"https://discord.com/api/v10/users/{discord_input}"
    headers = {
        "Authorization": f"Bot {API_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        print(f"\n{Colors.GREEN}Информация о пользователе:{Colors.RESET}")
        print(f"Username: {user_data.get('username')}#{user_data.get('discriminator')}")
        print(f"ID: {user_data.get('id')}")
        avatar_hash = user_data.get('avatar')
        if avatar_hash:
            print(f"Avatar URL: https://cdn.discordapp.com/avatars/{user_data.get('id')}/{avatar_hash}.png")
        else:
            print("Avatar: отсутствует")
        print(f"Bot: {user_data.get('bot', False)}")
        print(f"Public Flags: {user_data.get('public_flags')}")
        print(f"Accent Color: {user_data.get('accent_color')}")
    else:
        print(f"{Colors.BLUE}Ошибка запроса: {response.status_code} {response.text}{Colors.RESET}")

def search_all_databases(folder_path, search_term):
    valid_extensions = (".db", ".txt", ".sql")
    found_results = []

    try:
        db_files = [f for f in os.listdir(folder_path) if f.endswith(valid_extensions)]
    except FileNotFoundError:
        print(f"Папка не найдена: {folder_path}")
        return []

    for db_file in db_files:
        full_path = os.path.join(folder_path, db_file)

        if db_file.endswith(".db"):
            try:
                conn = sqlite3.connect(full_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                for table_name in tables:
                    table = table_name[0]
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = cursor.fetchall()
                    text_columns = [col[1] for col in columns if col[2] in ("TEXT", "VARCHAR")]

                    for col in text_columns:
                        query = f"SELECT * FROM {table} WHERE {col} LIKE ?"
                        cursor.execute(query, (f"%{search_term}%",))
                        rows = cursor.fetchall()
                        if rows:
                            found_results.append((full_path, table, col, rows))

                conn.close()
            except Exception as e:
                print(f"Ошибка при работе с базой {full_path}: {e}")

        else:
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if search_term in line:
                            found_results.append((full_path, i + 1, line.strip()))
            except Exception as e:
                print(f"Ошибка при чтении файла {full_path}: {e}")
    return found_results

def check_breaches_google_dork(email_or_username):
    print(f"\n{Colors.BLUE}Поиск утечек данных по: {email_or_username}{Colors.RESET}")
    print(f"{Colors.CYAN}Используются открытые источники{Colors.RESET}")

    queries = [
        f'site:pastebin.com "{email_or_username}"',
        f'site:throwbin.io "{email_or_username}"',
        f'site:anonfiles.com "{email_or_username}"',
        f'site:pasteio.com "{email_or_username}"',
        f'"{email_or_username}" filetype:txt',
        f'"{email_or_username}" inurl:breach',
    ]

    print(f"{Colors.GREEN}Ссылки с результатами: {Colors.RESET}")
    for q in queries:
        print(f"https://www.google.com/search?q={urllib.parse.quote(q)}")

def whois_lookup(query):
    try:
        # Преобразуем домен в IP, если нужно
        ip = socket.gethostbyname(query)
    except socket.gaierror:
        print(f"{Colors.RED} Не удалось разрешить домен: {query}{Colors.RESET}")
        return

    url = f"https://ipwho.is/{ip}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("success"):
            print(f"\n{Colors.GREEN} WHOIS-информация для {query}:{Colors.RESET}")
            print(f"{Colors.RED} IP:{Colors.RESET} {data.get('ip')}")
            print(f"{Colors.RED} Страна:{Colors.RESET} {data.get('country')} ({data.get('country_code')})")
            print(f"{Colors.RED} Регион:{Colors.RESET} {data.get('region')}")
            print(f"{Colors.RED} Город:{Colors.RESET} {data.get('city')}")
            print(f"{Colors.RED} Провайдер (ISP):{Colors.RESET} {data.get('connection', {}).get('isp')}")
            print(f"{Colors.RED} Организация:{Colors.RESET} {data.get('connection', {}).get('org')}")
            print(f"{Colors.RED} ASN:{Colors.RESET} {data.get('connection', {}).get('asn')}")
            print(f"{Colors.RED} Таймзона:{Colors.RESET} {data.get('timezone', {}).get('id')}")
        else:
            print(f"{Colors.RED} WHOIS-запрос не удался: {data.get('message', 'неизвестная ошибка')}{Colors.RESET}")

    except Exception as e:
        print(f"{Colors.RED} Ошибка при выполнении запроса: {e}{Colors.RESET}")

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return port
    except:
        pass
    return None

def scan_ports(ip, ports_range=(1, 1024)):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(ports_range[0], ports_range[1]+1)]
        for f in futures:
            port = f.result()
            if port:
                open_ports.append(port)
    return open_ports

while True:
    clear_screen()
    print_banner()
    print_menu()

    choice = input(f"{Colors.BLUE}        ┌──[Choose]{Colors.CYAN}\n        └─> ").strip()

    if choice == "0":
        print(f"\n{Colors.CYAN} Выход из программы{Colors.RESET}")
        time.sleep(3)
        break

    elif choice == "1":
        nickname = input(f"{Colors.BLUE}Введите никнейм: {Colors.RESET}").strip()
        results = generate_social_links(nickname)
        print(f"\n{Colors.GREEN} Найдены результаты:{Colors.RESET}\n")
        for platform, url in results.items():
            print(f"{Colors.BLUE}{platform}:{Colors.RESET} {url}")
        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения{Colors.RESET}")

    elif choice == "2":
        user_input = input(f"{Colors.BLUE}Введите IP-адрес: {Colors.RESET}").strip()
        link = generate_ip_link(user_input)
        print(f"\n{Colors.GREEN} Ссылка на инфу об IP:{Colors.RESET} {link}")
        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения{Colors.RESET}")

    elif choice == "3":
        user_input = input(f"{Colors.BLUE}Введите номер (+79001234567): {Colors.RESET}").strip()
        print(f"{Colors.BLUE}\n Отправка HLR-запроса...{Colors.RESET}")
        hlr_lookup(user_input)
        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения{Colors.RESET}")

    elif choice == "4":
        discord_input = input(f"{Colors.BLUE}Введите Discord ID (12345678912345678): {Colors.RESET}").strip()
        print(f"{Colors.BLUE}\n Discord OSINT...{Colors.RESET}")
        discord_osint(discord_input)
        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения{Colors.RESET}")

    elif choice == "5":
        folder = input(f"{Colors.BLUE}Введите путь к папке с базами данных: {Colors.RESET}").strip()
        term = input(f"{Colors.BLUE}Введите строку для поиска: {Colors.RESET}").strip()
        print(f"{Colors.BLUE}\nИдет поиск...{Colors.RESET}")
        results = search_all_databases(folder, term)

        if results:
            print(f"\n{Colors.GREEN}Найдено результатов: {len(results)}{Colors.RESET}")
            for res in results:
                if len(res) == 4:
                    path, table, column, rows = res
                    print(f"\n{Colors.BLUE}База:{Colors.RESET} {path}")
                    print(f"{Colors.BLUE}Таблица:{Colors.RESET} {table}")
                    print(f"{Colors.V}Колонка:{Colors.RESET} {column}")
                    print(f"{Colors.BLUE}Строки:{Colors.RESET} {rows}")
                else:
                    path, line_num, line_text = res
                    print(f"\n{Colors.BLUE}Файл:{Colors.RESET} {path}")
                    print(f"{Colors.BLUE}Строка {line_num}:{Colors.RESET} {line_text}")
        else:
            print(f"{Colors.RED}Ничего не найдено.{Colors.RESET}")

        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения{Colors.RESET}")

    elif choice == "6":
        login = input(f"{Colors.BLUE}Введите email или username для поиска утечек: {Colors.RESET}").strip()
        check_breaches_google_dork(login)
        input(f"\n{Colors.BOLD}Нажмите Enter, чтобы продолжить...{Colors.RESET}")

    elif choice == "7":
        query = input(f"{Colors.BLUE}Введите IP или домен: {Colors.RESET}").strip()
        print(f"{Colors.CYAN}\n Выполняется WHOIS-анализ{Colors.RESET}")
        whois_lookup(query)
        input(f"\n{Colors.BOLD}Нажмите Enter для возврата в меню{Colors.RESET}")


    elif choice == "8":

        ip = input("Введите IP для сканирования портов: ").strip()

        print(f"\n{Colors.BLUE}Сканирование портов {ip}...{Colors.RESET}\n")


        def scan_port(ip, port):

            try:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                    sock.settimeout(0.5)

                    result = sock.connect_ex((ip, port))

                    if result == 0:
                        return port

            except:

                pass

            return None


        def scan_ports(ip, ports_range=(1, 1024)):

            open_ports = []

            with ThreadPoolExecutor(max_workers=100) as executor:

                futures = [executor.submit(scan_port, ip, port) for port in range(ports_range[0], ports_range[1] + 1)]

                for f in futures:

                    port = f.result()

                    if port:
                        open_ports.append(port)

            return open_ports


        open_ports = scan_ports(ip)

        if open_ports:

            print(f"\n{Colors.GREEN}Открытые порты для {ip}:{Colors.RESET} {', '.join(map(str, open_ports))}")

        else:

            print(f"\n{Colors.RED}Открытых портов не найдено для {ip}.{Colors.RESET}")
            input("\nНажмите Enter, чтобы выйти...")
