# ui.py

# ui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from encryption import encrypt_directory, decrypt_directory, generate_key, save_key
from settings import KEY_FILE, DEFAULT_LANGUAGE, DEFAULT_THEME  # Импортируем DEFAULT_THEME
import json
import os

try:
    import sv_ttk  # Попробуем использовать sv_ttk для более продвинутых тем
    THEME_LIBRARY = "sv_ttk"
except ImportError:
    THEME_LIBRARY = "tk"  # Если sv_ttk нет, используем встроенные возможности tkinter

from languages import lang_manager

# Файл для хранения пользовательских настроек (включая тему)
SETTINGS_FILE = "app_settings.json"

class USBEncrypterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(lang_manager.get_text('main_title'))

        self.root.minsize(300, 200)

        self.user_settings = self.load_user_settings()
        self.current_theme = self.user_settings.get('theme', DEFAULT_THEME)
        
        # Применяем тему
        self.apply_theme(self.current_theme)
        
        self.update_ui_language()

        self.center_window()

    def center_window(self):
        """Центрирует окно приложения на экране."""
        # Обновляем "idle tasks" чтобы убедиться, что все геометрические параметры актуальны
        self.root.update_idletasks()
        
        # Получаем размеры окна
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Рассчитываем позицию для центрирования
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Устанавливаем позицию окна
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def load_user_settings(self):
        """Загружает пользовательские настройки из файла."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка при загрузке настроек: {e}")
                return {}
        return {}

    def save_user_settings(self):
        """Сохраняет пользовательские настройки в файл."""
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")

    def apply_theme(self, theme_name):
        """Применяет выбранную тему к приложению."""
        self.current_theme = theme_name
        self.user_settings['theme'] = theme_name
        
        if THEME_LIBRARY == "sv_ttk":
            if theme_name == "dark":
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")
        else:
            # Базовая поддержка тем через изменение цветов виджетов
            # Это упрощенная реализация. Для полноценной темной темы
            # рекомендуется использовать специализированные библиотеки.
            if theme_name == "dark":
                self.root.configure(bg='#2d2d2d')
                # Цвета для темной темы можно настроить индивидуально для каждого виджета
                # Но это потребует значительных изменений во всем коде
                pass
            else:
                self.root.configure(bg='#f0f0f0')

    def update_ui_language(self):
        """Обновляет текст в UI в соответствии с текущим языком."""
        self.root.title(lang_manager.get_text('main_title'))
        
        # Очищаем текущие элементы
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Создаем кнопки с переведенным текстом
        self.encrypt_button = tk.Button(self.root, text=lang_manager.get_text('encrypt_button'), 
                                      command=self.show_encrypt_window)
        self.decrypt_button = tk.Button(self.root, text=lang_manager.get_text('decrypt_button'), 
                                      command=self.show_decrypt_window)
        self.settings_button = tk.Button(self.root, text=lang_manager.get_text('settings_button'), 
                                       command=self.show_settings)
        
        # Создаем кнопки с переведенным текстом
        self.encrypt_button = tk.Button(self.root, text=lang_manager.get_text('encrypt_button'), 
                                       command=self.show_encrypt_window)
        self.decrypt_button = tk.Button(self.root, text=lang_manager.get_text('decrypt_button'), 
                                       command=self.show_decrypt_window)
        self.settings_button = tk.Button(self.root, text=lang_manager.get_text('settings_button'), 
                                        command=self.show_settings)
        
        # Размещаем элементы
        self.encrypt_button.pack(pady=10)
        self.decrypt_button.pack(pady=10)
        self.settings_button.pack(pady=10)
    
    def show_encrypt_window(self):
        """Открывает окно шифрования."""
        encrypt_window = tk.Toplevel(self.root)
        encrypt_window.title(lang_manager.get_text('encrypt_title'))

        encrypt_window.minsize(400, 300)

        self.center_toplevel_window(encrypt_window)
        
        # Поле для выбора файлов/папок
        drive_label = tk.Label(encrypt_window, text=lang_manager.get_text('select_files'))
        drive_entry = tk.Entry(encrypt_window, width=50)
        browse_button = tk.Button(encrypt_window, text=lang_manager.get_text('browse_button'),
                                command=lambda: self.browse_files_or_folders(drive_entry, encrypt_window))

        password_label = tk.Label(encrypt_window, text=lang_manager.get_text('enter_password'))
        password_entry = tk.Entry(encrypt_window, show="*", width=50)

        encrypt_start_button = tk.Button(encrypt_window, text=lang_manager.get_text('start_encryption'),
                                       command=lambda: self.start_encryption(
                                           drive_entry.get().split(";"),
                                           password_entry.get()))
        
        # Размещаем элементы
        drive_label.pack(pady=10)
        drive_entry.pack(pady=5)
        browse_button.pack(pady=5)
        password_label.pack(pady=15)
        password_entry.pack(pady=5)
        encrypt_start_button.pack(pady=20)

    def center_toplevel_window(self, window):
        """Центрирует дочернее окно (Toplevel) относительно главного окна."""
        # Обновляем "idle tasks" чтобы убедиться, что все геометрические параметры актуальны
        window.update_idletasks()
        
        # Получаем размеры дочернего окна
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        
        # Получаем позицию и размеры главного окна
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        # Рассчитываем позицию для центрирования дочернего окна
        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)
        
        # Устанавливаем позицию окна
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def browse_files_or_folders(self, entry_widget):
        """Открывает диалоговое окно для выбора файлов/папок."""
        # Сначала пробуем выбрать файлы
        files = filedialog.askopenfilenames()
        if files:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, ";".join(files))
        else:
            # Если файлы не выбраны, пробуем выбрать папку
            folder = filedialog.askdirectory()
            if folder:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, folder)
    
    def start_encryption(self, paths, password):
        """Запускает процесс шифрования."""
        if not paths or (len(paths) == 1 and not paths[0]):
            messagebox.showerror("Ошибка", lang_manager.get_text('error_select_files'))
            return
        
        if not password:
            messagebox.showerror("Ошибка", lang_manager.get_text('error_enter_password'))
            return
        
        try:
            key = generate_key(password.encode())
            save_key(key, KEY_FILE)
            
            for path in paths:
                if path:  # Проверяем, что путь не пустой
                    encrypt_directory(path, key)
            messagebox.showinfo("Успех", lang_manager.get_text('success_encryption'))
        except Exception as e:
            messagebox.showerror("Ошибка", f"{lang_manager.get_text('error_encryption')} {str(e)}")
    
    def show_decrypt_window(self):
        """Открывает окно дешифрования."""
        decrypt_window = tk.Toplevel(self.root)
        decrypt_window.title(lang_manager.get_text('decrypt_title'))

        decrypt_window.minsize(400, 300)

        self.center_toplevel_window(decrypt_window)
        
        # Поле для выбора зашифрованных файлов/папок
        decrypt_label = tk.Label(decrypt_window, text=lang_manager.get_text('select_encrypted_files'))
        decrypt_entry = tk.Entry(decrypt_window, width=50)
        browse_decrypt_button = tk.Button(decrypt_window, text=lang_manager.get_text('browse_button'),
                                        command=lambda: self.browse_files_or_folders(decrypt_entry, decrypt_window))

        decrypt_password_label = tk.Label(decrypt_window, text=lang_manager.get_text('enter_password'))
        decrypt_password_entry = tk.Entry(decrypt_window, show="*", width=50)

        decrypt_start_button = tk.Button(decrypt_window, text=lang_manager.get_text('start_decryption'),
                                       command=lambda: self.start_decryption(
                                           decrypt_entry.get().split(";"),
                                           decrypt_password_entry.get()))
        
        # Размещаем элементы
        decrypt_label.pack(pady=10)
        decrypt_entry.pack(pady=5)
        browse_decrypt_button.pack(pady=5)
        decrypt_password_label.pack(pady=15)
        decrypt_password_entry.pack(pady=5)
        decrypt_start_button.pack(pady=20)
    
    def browse_files_or_folders(self, entry_widget, parent_window):
        """Открывает диалоговое окно для выбора файлов/папок с управлением видимостью родительского окна."""
        # Скрываем родительское окно
        parent_window.withdraw()
        
        # Обновляем root, чтобы диалог появился корректно
        self.root.update()
        
        # Сначала пробуем выбрать файлы
        files = filedialog.askopenfilenames(parent=self.root) # Указываем parent
        selected_paths = []
        if files:
            selected_paths = list(files)
        else:
            # Если файлы не выбраны, пробуем выбрать папку
            folder = filedialog.askdirectory(parent=self.root) # Указываем parent
            if folder:
                selected_paths = [folder]
        
        # Показываем родительское окно после закрытия диалога
        parent_window.deiconify()
        parent_window.lift() # Поднимаем окно на передний план
        
        # Обновляем поле ввода, если что-то было выбрано
        if selected_paths:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, ";".join(selected_paths))
    
    def start_decryption(self, paths, password):
        """Запускает процесс дешифрования."""
        if not paths or (len(paths) == 1 and not paths[0]):
            messagebox.showerror("Ошибка", lang_manager.get_text('error_select_encrypted_files'))
            return
        
        if not password:
            messagebox.showerror("Ошибка", lang_manager.get_text('error_enter_password'))
            return
        
        try:
            key = generate_key(password.encode())
            for path in paths:
                if path:  # Проверяем, что путь не пустой
                    decrypt_directory(path, key)
            messagebox.showinfo("Успех", lang_manager.get_text('success_decryption'))
        except Exception as e:
            messagebox.showerror("Ошибка", f"{lang_manager.get_text('error_decryption')} {str(e)}")
    
    def show_settings(self):
        """Показывает диалоговое окно настроек."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(lang_manager.get_text('settings_title'))

        settings_window.minsize(350, 350)

        self.center_toplevel_window(settings_window)
        
        # Настройки языка
        language_frame = tk.LabelFrame(settings_window, text=lang_manager.get_text('language_settings'))
        language_frame.pack(pady=10, padx=10, fill='x')
        
        # Выбор языка
        language_label = tk.Label(language_frame, text=lang_manager.get_text('current_language'))
        language_label.pack(pady=5)
        
        # Создаем выпадающий список с языками
        language_names = lang_manager.get_language_names()
        language_var = tk.StringVar(value=language_names.get(lang_manager.current_language, 
                                                           lang_manager.current_language))
        
        language_combo = ttk.Combobox(language_frame, textvariable=language_var, 
                                    values=list(language_names.values()), state='readonly')
        language_combo.pack(pady=5)

        # === НОВОЕ: Настройки темы ===
        theme_frame = tk.LabelFrame(settings_window, text="Тема оформления / Theme")
        theme_frame.pack(pady=15, padx=10, fill='x')
        
        theme_label = tk.Label(theme_frame, text="Выберите тему / Select Theme:")
        theme_label.pack(pady=5)

        # Доступные темы
        available_themes = {"Светлая / Light": "light", "Темная / Dark": "dark"}
        current_theme_name = [name for name, code in available_themes.items() if code == self.current_theme][0] if self.current_theme in available_themes.values() else "Светлая / Light"
        
        theme_var = tk.StringVar(value=current_theme_name)
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, 
                                  values=list(available_themes.keys()), state='readonly')
        theme_combo.pack(pady=5)
        
        # Кнопка сохранения настроек
        save_button = tk.Button(settings_window, text=lang_manager.get_text('save_settings'), 
                              command=lambda: self.save_settings(
                                  language_combo, language_names, theme_combo, available_themes, settings_window))
        save_button.pack(pady=20)
        
        # Информация о файле ключа
        key_file_label = tk.Label(settings_window, text=f"{lang_manager.get_text('key_file')} {KEY_FILE}")
        key_file_label.pack(pady=10)

    def save_settings(self, language_combo, language_names, theme_combo, available_themes, settings_window):
        """Сохраняет настройки языка и темы."""
        # Сохранение языка
        selected_language_name = language_combo.get()
        language_code = None
        for code, name in language_names.items():
            if name == selected_language_name:
                language_code = code
                break
        
        if language_code:
            lang_manager.set_language(language_code)
        
        # === НОВОЕ: Сохранение темы ===
        selected_theme_name = theme_combo.get()
        theme_code = available_themes.get(selected_theme_name)
        
        if theme_code and theme_code != self.current_theme:
            self.apply_theme(theme_code)
            # Переприменяем тему ко всем открытым окнам (упрощенно)
            # В реальном приложении нужно было бы обновлять тему для всех окон
        # === КОНЕЦ НОВОГО ===
        
        # Сохраняем все настройки в файл
        self.user_settings['language'] = language_code if language_code else DEFAULT_LANGUAGE
        self.user_settings['theme'] = theme_code if theme_code else DEFAULT_THEME
        self.save_user_settings()
        
        # Обновляем интерфейс главного окна
        self.update_ui_language()
        settings_window.destroy()
        messagebox.showinfo("Успех", "Настройки сохранены!")

    def center_toplevel_window(self, window):
        window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    app = USBEncrypterApp(root)
    
    # Если используем sv_ttk, применяем тему после создания приложения
    if THEME_LIBRARY == "sv_ttk":
        import sv_ttk
        # Тема уже применяется в __init__
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()