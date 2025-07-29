# languages.py

import json
import os

class LanguageManager:
    def __init__(self, default_language='ru'):
        self.current_language = default_language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Загружает переводы из JSON файлов."""
        locales_dir = 'locales'
        if not os.path.exists(locales_dir):
            os.makedirs(locales_dir)
            self.create_default_translations()
        
        for filename in os.listdir(locales_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Убираем .json
                with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
    
    def create_default_translations(self):
        """Создает файлы переводов по умолчанию."""
        translations = {
            'ru': {
                'main_title': 'Шифровальщик USB-накопителей',
                'encrypt_button': 'Шифровать',
                'decrypt_button': 'Дешифровать',
                'settings_button': 'Настройки',
                'encrypt_title': 'Шифрование',
                'select_files': 'Выберите файлы/папки:',
                'browse_button': 'Обзор',
                'enter_password': 'Введите пароль:',
                'start_encryption': 'Начать шифрование',
                'decrypt_title': 'Дешифрование',
                'select_encrypted_files': 'Выберите зашифрованные файлы/папки:',
                'start_decryption': 'Начать дешифрование',
                'settings_title': 'Настройки',
                'language_settings': 'Настройки языка',
                'current_language': 'Текущий язык:',
                'save_settings': 'Сохранить настройки',
                'select_language': 'Выберите язык',
                'error_select_files': 'Выберите файлы или папки.',
                'error_enter_password': 'Введите пароль.',
                'success_encryption': 'Файлы/папки успешно зашифрованы.',
                'error_encryption': 'Не удалось зашифровать:',
                'error_select_encrypted_files': 'Выберите зашифрованные файлы или папки.',
                'success_decryption': 'Файлы/папки успешно дешифрованы.',
                'error_decryption': 'Не удалось дешифровать:',
                'key_file': 'Файл ключа:'
            },
            'en': {
                'main_title': 'USB Drive Encrypter',
                'encrypt_button': 'Encrypt',
                'decrypt_button': 'Decrypt',
                'settings_button': 'Settings',
                'encrypt_title': 'Encryption',
                'select_files': 'Select files/folders:',
                'browse_button': 'Browse',
                'enter_password': 'Enter password:',
                'start_encryption': 'Start Encryption',
                'decrypt_title': 'Decryption',
                'select_encrypted_files': 'Select encrypted files/folders:',
                'start_decryption': 'Start Decryption',
                'settings_title': 'Settings',
                'language_settings': 'Language Settings',
                'current_language': 'Current language:',
                'save_settings': 'Save Settings',
                'select_language': 'Select Language',
                'error_select_files': 'Please select files or folders.',
                'error_enter_password': 'Please enter password.',
                'success_encryption': 'Files/folders encrypted successfully.',
                'error_encryption': 'Failed to encrypt:',
                'error_select_encrypted_files': 'Please select encrypted files or folders.',
                'success_decryption': 'Files/folders decrypted successfully.',
                'error_decryption': 'Failed to decrypt:',
                'key_file': 'Key file:'
            },
            'es': {
                'main_title': 'Cifrador de unidades USB',
                'encrypt_button': 'Cifrar',
                'decrypt_button': 'Descifrar',
                'settings_button': 'Configuración',
                'encrypt_title': 'Cifrado',
                'select_files': 'Seleccionar archivos/carpetas:',
                'browse_button': 'Examinar',
                'enter_password': 'Ingrese contraseña:',
                'start_encryption': 'Iniciar cifrado',
                'decrypt_title': 'Descifrado',
                'select_encrypted_files': 'Seleccionar archivos/carpetas cifrados:',
                'start_decryption': 'Iniciar descifrado',
                'settings_title': 'Configuración',
                'language_settings': 'Configuración de idioma',
                'current_language': 'Idioma actual:',
                'save_settings': 'Guardar configuración',
                'select_language': 'Seleccionar idioma',
                'error_select_files': 'Por favor seleccione archivos o carpetas.',
                'error_enter_password': 'Por favor ingrese contraseña.',
                'success_encryption': 'Archivos/carpetas cifrados exitosamente.',
                'error_encryption': 'Error al cifrar:',
                'error_select_encrypted_files': 'Por favor seleccione archivos o carpetas cifrados.',
                'success_decryption': 'Archivos/carpetas descifrados exitosamente.',
                'error_decryption': 'Error al descifrar:',
                'key_file': 'Archivo de clave:'
            }
        }
        
        for lang_code, translations_dict in translations.items():
            filename = f'locales/{lang_code}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(translations_dict, f, ensure_ascii=False, indent=2)
    
    def get_text(self, key):
        """Получает перевод для указанного ключа."""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, key)
        return key
    
    def set_language(self, language_code):
        """Устанавливает текущий язык."""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_available_languages(self):
        """Возвращает список доступных языков."""
        return list(self.translations.keys())
    
    def get_language_names(self):
        """Возвращает словарь с названиями языков."""
        names = {
            'ru': 'Русский',
            'en': 'English',
            'es': 'Español'
        }
        return names

# Создаем глобальный экземпляр менеджера языков
lang_manager = LanguageManager()