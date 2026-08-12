import os
import sys
import time
import json
import hashlib
import subprocess
import threading
import requests
from datetime import datetime
from cryptography.fernet import Fernet

# ===== КОНФИГ =====
CONFIG = {
    "watch_dirs": ["/sdcard/Download", "/sdcard/Android", "/sdcard/DCIM"],
    "scan_extensions": [".apk", ".dex", ".jar", ".sh", ".bin", ".exe"],
    "suspicious_hashes": [
        "37d4c5a0ea070fe0a1a2703914bf442b4285658b31d220f974adcf953b041e11",
        "184356d900a545a2d545ab96fa6dd7b46f881a1a80ed134db1c65225e8fa902b",
        "0fdfbf20e59b28181801274ad23b951106c6f7a516eb914efd427b6617630f30"
    ],
    "suspicious_perms": ["777", "755"],
    "suspicious_apps": ["com.teamviewer", "com.anydesk"],
    "suspicious_ports": [22, 23, 3389, 5900],
    "log_file": "/sdcard/last_chance.log",
    "hash_file": "/sdcard/.last_chance_hashes.json",
    "quarantine_file": "/sdcard/last_chance_quarantine.json",
    "key_file": "/sdcard/.last_chance_key",
    "version": "2.0",
    "github_repo": "p79850330/lastchance"
}

# ===== КЛЮЧ ШИФРОВАНИЯ =====
def load_key():
    if os.path.exists(CONFIG["key_file"]):
        with open(CONFIG["key_file"], "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(CONFIG["key_file"], "wb") as f:
        f.write(key)
    return key

KEY = load_key()
fernet = Fernet(KEY)

def encrypt_log(msg):
    return fernet.encrypt(msg.encode()).decode()

def decrypt_log(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

# ===== ЛОГИРОВАНИЕ =====
def log(msg, encrypted=False):
    full = f"[{datetime.now()}] {msg}"
    print(full)
    try:
        if encrypted:
            with open(CONFIG["log_file"], "a") as f:
                f.write(encrypt_log(full) + "\n")
        else:
            with open(CONFIG["log_file"], "a") as f:
                f.write(full + "\n")
    except:
        pass

def notify(title, msg):
    try:
        subprocess.run(['termux-notification', '-t', title, '-c', msg])
    except:
        pass

# ===== KASPERSKY API =====
def check_with_kaspersky(sha256):
    try:
        url = "https://opentip.kaspersky.com/api/v1/search/hash"
        headers = {"Content-Type": "application/json"}
        payload = {"hash": sha256}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("detected", False):
                return True, data.get("threat_name", "Unknown")
        return False, None
    except:
        return False, None

# ===== САМОПРОВЕРКА =====
def save_hashes():
    hashes = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(script_dir):
        for f in files:
            full = os.path.join(root, f)
            try:
                with open(full, "rb") as fp:
                    hashes[full] = hashlib.md5(fp.read()).hexdigest()
            except:
                pass
    with open(CONFIG["hash_file"], "w") as fp:
        json.dump(hashes, fp)

def self_check():
    if not os.path.exists(CONFIG["hash_file"]):
        return False
    with open(CONFIG["hash_file"], "r") as fp:
        expected = json.load(fp)
    for filepath, expected_hash in expected.items():
        if not os.path.exists(filepath):
            continue
        with open(filepath, "rb") as fp:
            current_hash = hashlib.md5(fp.read()).hexdigest()
        if current_hash != expected_hash:
            log(f"⚠️ Файл изменён: {filepath}")
            return True
    return False

# ===== СИСТЕМЫ САМОУНИЧТОЖЕНИЯ (10 систем) =====
def shatter():
    log("[SHATTER] Уничтожение всех файлов антивируса")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(script_dir):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except:
                pass
    try:
        os.rmdir(script_dir)
    except:
        pass

def purge():
    log("[PURGE] Удаление внешних данных")
    for f in os.listdir("/sdcard"):
        if f.startswith("last_chance") and f.endswith((".log", ".json", ".sig", ".key")):
            try:
                os.remove(os.path.join("/sdcard", f))
            except:
                pass

def erase():
    log("[ERASE] Завершение процессов")
    try:
        os.system("pkill -f last_chance")
    except:
        pass
    for t in threading.enumerate():
        if t != threading.main_thread():
            try:
                t.join(0.1)
            except:
                pass

def oblivion():
    log("[OBLIVION] Затирание остатков")
    trash = []
    for root, _, files in os.walk("/data/data/com.termux/files/home"):
        for f in files:
            if "last_chance" in f.lower():
                trash.append(os.path.join(root, f))
    for path in trash:
        try:
            with open(path, "wb") as fp:
                fp.write(b"\x00" * 1024)
            os.remove(path)
        except:
            pass

def core_destroy():
    log("[CORE_DESTROY] Удаление себя")
    try:
        os.remove(__file__)
    except:
        pass
    sys.exit(0)

def shred():
    log("[SHRED] Перезапись файлов случайными данными")
    for root, _, files in os.walk("/sdcard"):
        for f in files:
            if "last_chance" in f.lower():
                try:
                    with open(os.path.join(root, f), "wb") as fp:
                        fp.write(os.urandom(1024))
                except:
                    pass

def wipe_cache():
    log("[WIPE] Очистка кэша")
    try:
        os.system("rm -rf /data/data/com.termux/cache/*")
    except:
        pass

def kill_parent():
    log("[KILL_PARENT] Завершение родительского процесса")
    try:
        os.kill(os.getppid(), 9)
    except:
        pass

def corrupt_self():
    log("[CORRUPT] Повреждение исполняемого файла")
    try:
        with open(__file__, "wb") as f:
            f.write(os.urandom(1024))
    except:
        pass

def final_blast():
    log("[FINAL_BLAST] Полное уничтожение всех следов")
    try:
        os.system("rm -rf /sdcard/last_chance*")
        os.system("rm -rf ~/.buildozer")
        os.system("rm -rf ~/.termux")
    except:
        pass

def full_destruct():
    log("⚠️ ЗАПУЩЕНО ПОЛНОЕ МНОГОУРОВНЕВОЕ УНИЧТОЖЕНИЕ (10 систем)")
    notify("Last Chance 2.0", "Антивирус уничтожает себя. Безопасность превыше всего.")
    shatter()
    purge()
    erase()
    oblivion()
    shred()
    wipe_cache()
    kill_parent()
    corrupt_self()
    final_blast()
    core_destroy()

# ===== КАРАНТИН =====
def quarantine_file(filepath, reason):
    try:
        q_file = CONFIG["quarantine_file"]
        if os.path.exists(q_file):
            with open(q_file, "r") as f:
                q = json.load(f)
        else:
            q = {}
        q[filepath] = {"reason": reason, "time": str(datetime.now())}
        with open(q_file, "w") as f:
            json.dump(q, f)
        os.chmod(filepath, 0o000)
        notify("Last Chance", f"Файл в карантине: {os.path.basename(filepath)}")
        return True
    except:
        return False

def restore_file(filepath):
    try:
        q_file = CONFIG["quarantine_file"]
        if os.path.exists(q_file):
            with open(q_file, "r") as f:
                q = json.load(f)
            if filepath in q:
                os.chmod(filepath, 0o644)
                del q[filepath]
                with open(q_file, "w") as f:
                    json.dump(q, f)
                notify("Last Chance", f"Файл восстановлен: {os.path.basename(filepath)}")
                return True
    except:
        pass
    return False

# ===== ПОВЕДЕНЧЕСКИЙ АНАЛИЗ =====
def detect_ransomware():
    try:
        result = subprocess.run(['find', '/sdcard', '-name', '*.encrypted'], capture_output=True, text=True)
        if result.stdout:
            notify("Last Chance", "⚠️ Обнаружено массовое переименование! Возможно ransomware.")
            return True
    except:
        pass
    return False

def detect_overlay():
    try:
        result = subprocess.run(['dumpsys', 'window'], capture_output=True, text=True)
        if "TYPE_SYSTEM_ALERT" in result.stdout:
            notify("Last Chance", "⚠️ Обнаружено окно-ловушка!")
            return True
    except:
        pass
    return False

def behavioral_analyzer():
    log("[+] Поведенческий анализатор запущен")
    while True:
        try:
            detect_ransomware()
            detect_overlay()
            time.sleep(10)
        except:
            time.sleep(5)

# ===== МОНИТОРИНГ ФАЙЛОВ =====
def scan_file(filepath):
    if filepath in EXCLUDED_FILES:
        return False, "файл в исключениях, пропущен"
    try:
        perms = oct(os.stat(filepath).st_mode)[-3:]
        if perms in CONFIG["suspicious_perms"]:
            return True, f"права {perms}"
        
        with open(filepath, "rb") as f:
            data = f.read()
            sha256_hash = hashlib.sha256(data).hexdigest()
            if sha256_hash in CONFIG["suspicious_hashes"]:
                return True, f"известный вирус (SHA-256: {sha256_hash[:16]}...)"
            
            detected, name = check_with_kaspersky(sha256_hash)
            if detected:
                return True, f"Kaspersky: {name}"
        
        try:
            text = data.decode('utf-8', errors='ignore')
            for p in ["eval(", "exec(", "wget", "curl", "rm -rf"]:
                if p in text:
                    return True, f"подозрительная строка '{p}'"
        except:
            pass
    except:
        pass
    return False, ""

def monitor_files():
    log("[+] Мониторинг файлов запущен")
    while True:
        try:
            for root, _, files in os.walk("/sdcard"):
                for f in files:
                    full = os.path.join(root, f)
                    if any(full.endswith(ext) for ext in CONFIG["scan_extensions"]):
                        danger, reason = scan_file(full)
                        if danger:
                            log(f"⚠️ {full} — {reason}")
                            quarantine_file(full, reason)
            time.sleep(30)
        except:
            time.sleep(10)

# ===== МОНИТОРИНГ ПРОЦЕССОВ =====
def monitor_processes():
    log("[+] Мониторинг процессов запущен")
    while True:
        try:
            result = subprocess.run(['ps', '-e', '-o', 'comm'], capture_output=True, text=True)
            for p in result.stdout.splitlines():
                if any(x in p for x in ["nc", "netcat", "telnet"]):
                    notify("Last Chance", f"Подозрительный процесс: {p}")
            time.sleep(30)
        except:
            time.sleep(10)

# ===== МОНИТОРИНГ СЕТИ =====
def monitor_network():
    log("[+] Мониторинг сети запущен")
    while True:
        try:
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                for port in CONFIG["suspicious_ports"]:
                    if f":{port}" in line:
                        notify("Last Chance", f"Открыт порт: {port}")
            time.sleep(30)
        except:
            time.sleep(10)

# ===== МОНИТОРИНГ ПРИЛОЖЕНИЙ =====
def monitor_apps():
    log("[+] Мониторинг приложений запущен")
    while True:
        try:
            result = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True)
            installed = result.stdout.splitlines()
            for app in CONFIG["suspicious_apps"]:
                if any(app in pkg for pkg in installed):
                    notify("Last Chance", f"Подозрительное приложение: {app}")
            time.sleep(60)
        except:
            time.sleep(10)

# ===== АВТООБНОВЛЕНИЕ =====
def check_update():
    try:
        url = f"https://api.github.com/repos/{CONFIG['github_repo']}/releases/latest"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("tag_name", "").replace("v", "")
            if latest_version > CONFIG["version"]:
                notify("Last Chance", f"Доступна версия {latest_version}. Скачайте обновление.")
                return True
    except:
        pass
    return False

# ===== ОСНОВНОЙ ЦИКЛ =====
def main():
    log(f"=== Last Chance {CONFIG['version']} запущен ===")
    subprocess.run(['termux-wake-lock'])
    save_hashes()

    if check_update():
        log("[!] Доступно обновление")

    threads = [
        threading.Thread(target=monitor_files, daemon=True),
        threading.Thread(target=monitor_processes, daemon=True),
        threading.Thread(target=monitor_network, daemon=True),
        threading.Thread(target=monitor_apps, daemon=True),
        threading.Thread(target=behavioral_analyzer, daemon=True)
    ]
    for t in threads:
        t.start()

    while True:
        if self_check():
            full_destruct()
        time.sleep(30)

if __name__ == "__main__":
    main()
