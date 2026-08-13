# ===== GUI + ЯДРО АНТИВИРУСА (Last Chance 2.0) =====

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

# --- KIVY GUI ---
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.size = (360, 640)

# --- КОНФИГ ---
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
    "github_repo": "p79850330/lastchance-2.0"
}

# --- ОСТАЛЬНАЯ ЛОГИКА (хеши, самопроверка, мониторинг) ---
# (здесь весь код из last_chance_2.0.py — сокращённо, чтобы не дублировать)

# --- GUI ---
class LastChanceApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        title = Label(text='Last Chance 2.0', font_size=24, size_hint=(1, 0.1))
        layout.add_widget(title)
        
        self.status = Label(text='Статус: Защита включена', font_size=16, color=(0,1,0,1))
        layout.add_widget(self.status)
        
        btn_scan = Button(text='Сканировать', size_hint=(1, 0.15))
        btn_scan.bind(on_press=self.scan)
        layout.add_widget(btn_scan)
        
        btn_quarantine = Button(text='Карантин', size_hint=(1, 0.15))
        btn_quarantine.bind(on_press=self.quarantine)
        layout.add_widget(btn_quarantine)
        
        btn_settings = Button(text='Настройки', size_hint=(1, 0.15))
        btn_settings.bind(on_press=self.settings)
        layout.add_widget(btn_settings)
        
        self.log_text = Label(text='Готов к работе', font_size=12, size_hint=(1, 0.3))
        layout.add_widget(self.log_text)
        
        return layout
    
    def scan(self, instance):
        self.log_text.text = 'Сканирование запущено...'
    
    def quarantine(self, instance):
        self.log_text.text = 'Карантин: список файлов'
    
    def settings(self, instance):
        self.log_text.text = 'Настройки: модули включены'

if __name__ == '__main__':
    LastChanceApp().run()
