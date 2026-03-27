import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
import random
import sys
import os
import platform

# Определяем операционную систему
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

# ============================================
# КРОССПЛАТФОРМЕННЫЙ МОДУЛЬ ЗВУКА
# ============================================
class AudioModule:
    @staticmethod
    def play_sound(sound_type="order"):
        try:
            frequencies = {
                "order": 800, "assign": 1000, "start": 900,
                "complete": 1200, "cancel": 500, "error": 400
            }
            freq = frequencies.get(sound_type, 800)
            duration = 300
            
            if IS_WINDOWS:
                import winsound
                winsound.Beep(freq, duration)
            elif IS_MAC:
                try:
                    sounds = {
                        800: "/System/Library/Sounds/Ping.aiff",
                        1000: "/System/Library/Sounds/Tink.aiff",
                        1200: "/System/Library/Sounds/Glass.aiff",
                        500: "/System/Library/Sounds/Basso.aiff",
                        400: "/System/Library/Sounds/Funk.aiff"
                    }
                    sound_file = sounds.get(freq, "/System/Library/Sounds/Ping.aiff")
                    os.system(f'afplay "{sound_file}"')
                except:
                    pass
            else:
                pass
        except:
            pass


# ============================================
# МОДУЛЬ АНИМАЦИИ
# ============================================
class AnimationModule:
    @staticmethod
    def show_notification(parent, title, message, duration=2000, is_error=False):
        try:
            popup = tk.Toplevel(parent)
            popup.title(title)
            popup.geometry("350x150")
            
            if is_error:
                bg_color = '#e74c3c'
                icon_text = "❌"
            else:
                bg_color = '#2c3e50'
                icon_text = "✅"
            
            popup.configure(bg=bg_color)
            popup.attributes('-topmost', True)
            
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (350 // 2)
            y = (popup.winfo_screenheight() // 2) - (150 // 2)
            popup.geometry(f'+{x}+{y}')
            
            alpha = 0.0
            popup.attributes('-alpha', alpha)
            
            def fade_in():
                nonlocal alpha
                if alpha < 1.0:
                    alpha += 0.1
                    popup.attributes('-alpha', alpha)
                    popup.after(50, fade_in)
            
            icon_label = tk.Label(popup, text=icon_text, font=('Arial', 28),
                                  bg=bg_color, fg='white')
            icon_label.pack(pady=(20, 5))
            
            label = tk.Label(popup, text=message, font=('Arial', 11, 'bold'),
                            bg=bg_color, fg='white', wraplength=300)
            label.pack(expand=True, fill='both', padx=20, pady=5)
            
            fade_in()
            popup.after(duration, popup.destroy)
        except:
            if is_error:
                messagebox.showerror(title, message)
            else:
                messagebox.showinfo(title, message)


class QuestionDialog:
    @staticmethod
    def askyesno(title, message):
        return messagebox.askyesno(title, message)


class Documentation:
    @staticmethod
    def show_help(parent):
        win = tk.Toplevel(parent)
        win.title("Справка")
        win.geometry("600x500")
        
        text_area = tk.Text(win, wrap=tk.WORD, font=('Courier', 10))
        text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        help_text = u"""
ДОКУМЕНТАЦИЯ ПРОГРАММЫ "ТАКСОПАРК - ДИСПЕТЧЕРСКАЯ"
================================================

ОПИСАНИЕ ПРОГРАММЫ
------------------
Программа предназначена для диспетчерской службы таксопарка.
Обеспечивает управление заказами, водителями и отслеживание статусов.

ОСНОВНЫЕ ФУНКЦИИ
----------------
1. Новый заказ - создание заказа (нажмите Enter для быстрого создания)
2. Активные заказы - просмотр и управление заказами
3. Водители - просмотр списка водителей
4. Выполненные - история завершенных заказов (здесь же печать отчетов)

СТАТУСЫ ЗАКАЗОВ
---------------
НОВЫЙ - заказ создан, ожидает водителя
НАЗНАЧЕН - водитель назначен, ожидает начала
В ПУТИ - поездка началась
ВЫПОЛНЕН - заказ завершен
ОТМЕНЕН - заказ отменен

ГОРЯЧИЕ КЛАВИШИ
---------------
Enter - Создать заказ (в полях ввода)

ЗВУКОВЫЕ СИГНАЛЫ
----------------
800 Гц - Новый заказ
1000 Гц - Назначение водителя
900 Гц - Начало поездки
1200 Гц - Завершение заказа
500 Гц - Отмена заказа
400 Гц - Ошибка

МОДУЛИ ПРОГРАММЫ
----------------
- Database - работа с БД MySQL
- AudioModule - воспроизведение звуков
- AnimationModule - анимация уведомлений
- PrintModule - печать отчетов
- ModuleTests - тестирование модулей
"""
        text_area.insert('1.0', help_text)
        text_area.configure(state='disabled')


# ============================================
# МОДУЛЬ ПЕЧАТИ (с проверкой наличия данных)
# ============================================
class PrintModule:
    @staticmethod
    def print_orders_report(orders, parent):
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            if not orders:
                AnimationModule.show_notification(parent, "Нет данных", 
                                                 "Нет выполненных заказов для печати", 2000, True)
                return False
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Сохранить отчет о выполненных заказах"
            )
            if not filename:
                return False
            
            font_paths = []
            if IS_WINDOWS:
                font_paths = [
                    "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/times.ttf",
                    "C:/Windows/Fonts/calibri.ttf",
                ]
            elif IS_MAC:
                font_paths = [
                    "/System/Library/Fonts/Arial.ttf",
                    "/System/Library/Fonts/Times.ttc",
                    "/System/Library/Fonts/Helvetica.ttc",
                ]
            else:
                font_paths = [
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                ]
            
            font_registered = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                        font_registered = True
                        break
                    except:
                        continue
            
            styles = getSampleStyleSheet()
            
            if font_registered:
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Title'],
                    fontName='RussianFont',
                    fontSize=16,
                    alignment=1
                )
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontName='RussianFont',
                    fontSize=10
                )
            else:
                title_style = styles['Title']
                normal_style = styles['Normal']
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            title = Paragraph(u"Отчет по выполненным заказам таксопарка", title_style)
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            data = [[u'ID', u'Клиент', u'Откуда', u'Куда', u'Водитель', u'Дата']]
            for order in orders:
                date_str = order['completed_at'].strftime('%d.%m.%Y %H:%M') if order['completed_at'] else ''
                data.append([
                    str(order.get('id', '')),
                    order.get('client_name', '')[:30] or '',
                    order.get('start_address', '')[:30] or '',
                    order.get('end_address', '')[:30] or '',
                    order.get('driver_name', u'Не указан') or u'Не указан',
                    date_str
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'RussianFont' if font_registered else 'Helvetica'),
                ('FONTNAME', (0, 1), (-1, -1), 'RussianFont' if font_registered else 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(table)
            
            elements.append(Spacer(1, 30))
            date_paragraph = Paragraph(u"Дата формирования: " + datetime.now().strftime('%d.%m.%Y %H:%M'), normal_style)
            elements.append(date_paragraph)
            
            doc.build(elements)
            AnimationModule.show_notification(parent, "Успех", f"Отчет сохранен", 2000)
            return True
            
        except ImportError:
            AnimationModule.show_notification(parent, "Ошибка", 
                                             "Модуль reportlab не установлен\nУстановите: pip install reportlab", 
                                             3000, True)
            return False
        except Exception as e:
            AnimationModule.show_notification(parent, "Ошибка", f"Не удалось создать отчет", 3000, True)
            return False


# ============================================
# МОДУЛЬ ТЕСТИРОВАНИЯ
# ============================================
class ModuleTests:
    @staticmethod
    def test_database_connection(db):
        if not db:
            return False, "База данных не подключена"
        try:
            db.cursor.execute("SELECT 1")
            return True, "Подключение к БД успешно"
        except:
            return False, "Ошибка подключения"
    
    @staticmethod
    def test_audio_module():
        try:
            AudioModule.play_sound("order")
            return True, "Звуковой модуль работает"
        except:
            return False, "Звуковой модуль не доступен"
    
    @staticmethod
    def run_all_tests(db):
        results = []
        results.append(ModuleTests.test_database_connection(db))
        results.append(ModuleTests.test_audio_module())
        return results


# ============================================
# МОДУЛЬ БАЗЫ ДАННЫХ (с возможностью работы без БД)
# ============================================
class Database:
    def __init__(self):
        self.connected = False
        self.conn = None
        self.cursor = None
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="taxi_dispatch"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            self.connected = True
        except Exception as e:
            self.connected = False
            self.error_message = str(e)

    def is_connected(self):
        return self.connected

    def get_drivers(self):
        if not self.connected:
            return []
        self.cursor.execute("SELECT * FROM drivers")
        return self.cursor.fetchall()
    
    def get_free_drivers(self):
        if not self.connected:
            return []
        self.cursor.execute("SELECT * FROM drivers WHERE status = 'available'")
        return self.cursor.fetchall()
    
    def get_tariffs(self):
        if not self.connected:
            return [{"id": 1, "name": "Эконом", "price_per_km": 15.00, "price_per_minute": 5.00},
                    {"id": 2, "name": "Комфорт", "price_per_km": 25.00, "price_per_minute": 8.00}]
        self.cursor.execute("SELECT * FROM tariffs")
        return self.cursor.fetchall()

    def add_client(self, name, phone):
        if not self.connected:
            return 1
        self.cursor.execute("INSERT INTO clients (full_name, phone) VALUES (%s, %s)", (name, phone))
        self.conn.commit()
        return self.cursor.lastrowid

    def create_order(self, client_name, client_phone, start_addr, end_addr, tariff_id, dispatcher_id):
        if not self.connected:
            AnimationModule.show_notification(None, "Ошибка", 
                                             "База данных не подключена\nЗапустите XAMPP и MySQL", 
                                             3000, True)
            return None
        client_id = self.add_client(client_name, client_phone)
        sql = """INSERT INTO rides (client_id, dispatcher_id, tariff_id, start_address, end_address, status) 
                 VALUES (%s, %s, %s, %s, %s, 'new')"""
        self.cursor.execute(sql, (client_id, dispatcher_id, tariff_id, start_addr, end_addr))
        self.conn.commit()
        return self.cursor.lastrowid

    def assign_driver(self, ride_id, driver_id):
        if not self.connected:
            return
        self.cursor.execute("UPDATE rides SET driver_id = %s, status = 'assigned' WHERE id = %s", 
                           (driver_id, ride_id))
        self.cursor.execute("UPDATE drivers SET status = 'busy' WHERE id = %s", (driver_id,))
        self.conn.commit()

    def start_ride(self, ride_id):
        if not self.connected:
            return
        self.cursor.execute("UPDATE rides SET status = 'in_progress' WHERE id = %s", (ride_id,))
        self.conn.commit()

    def complete_ride(self, ride_id):
        if not self.connected:
            return
        self.cursor.execute("SELECT driver_id FROM rides WHERE id = %s", (ride_id,))
        result = self.cursor.fetchone()
        driver_id = result['driver_id'] if result else None
        
        self.cursor.execute("""UPDATE rides 
                               SET status = 'completed', completed_at = NOW() 
                               WHERE id = %s""", (ride_id,))
        
        if driver_id:
            self.cursor.execute("UPDATE drivers SET status = 'available' WHERE id = %s", (driver_id,))
        
        self.conn.commit()

    def cancel_ride(self, ride_id):
        if not self.connected:
            return
        self.cursor.execute("SELECT driver_id FROM rides WHERE id = %s", (ride_id,))
        result = self.cursor.fetchone()
        driver_id = result['driver_id'] if result else None
        
        self.cursor.execute("UPDATE rides SET status = 'cancelled' WHERE id = %s", (ride_id,))
        
        if driver_id:
            self.cursor.execute("UPDATE drivers SET status = 'available' WHERE id = %s", (driver_id,))
        
        self.conn.commit()

    def get_active_orders(self):
        if not self.connected:
            return []
        self.cursor.execute("""SELECT r.*, c.full_name as client_name, c.phone as client_phone,
                                      d.full_name as driver_name
                               FROM rides r 
                               JOIN clients c ON r.client_id = c.id 
                               LEFT JOIN drivers d ON r.driver_id = d.id 
                               WHERE r.status IN ('new', 'assigned', 'in_progress')
                               ORDER BY 
                                   CASE r.status 
                                       WHEN 'new' THEN 1 
                                       WHEN 'assigned' THEN 2 
                                       WHEN 'in_progress' THEN 3 
                                   END, r.id DESC""")
        return self.cursor.fetchall()

    def get_completed_orders(self):
        if not self.connected:
            return []
        self.cursor.execute("""SELECT r.*, d.full_name as driver_name, c.full_name as client_name
                               FROM rides r 
                               LEFT JOIN drivers d ON r.driver_id = d.id
                               JOIN clients c ON r.client_id = c.id
                               WHERE r.status = 'completed'
                               ORDER BY r.completed_at DESC LIMIT 20""")
        return self.cursor.fetchall()

    def get_stats(self):
        if not self.connected:
            return 0, 0, 0, 0
        self.cursor.execute("SELECT COUNT(*) as total FROM rides WHERE status = 'new'")
        new = self.cursor.fetchone()
        self.cursor.execute("SELECT COUNT(*) as total FROM rides WHERE status = 'assigned'")
        assigned = self.cursor.fetchone()
        self.cursor.execute("SELECT COUNT(*) as total FROM rides WHERE status = 'in_progress'")
        in_progress = self.cursor.fetchone()
        self.cursor.execute("SELECT COUNT(*) as total FROM drivers WHERE status = 'available'")
        available = self.cursor.fetchone()
        return new['total'], assigned['total'], in_progress['total'], available['total']


# ============================================
# ОСНОВНОЕ ПРИЛОЖЕНИЕ
# ============================================
class DispatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Таксопарк - Диспетчерская")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f5f5f5')
        
        self.db = Database()
        self.audio = AudioModule()
        self.print_module = PrintModule()
        self.dispatcher_id = 1
        
        # Показываем предупреждение, если БД не подключена
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Предупреждение", 
                                             "База данных не подключена\nРаботает демонстрационный режим\nЗапустите XAMPP и MySQL для полной функциональности", 
                                             4000, True)
        
        self.create_menu()
        self.create_notebook()
        self.create_statusbar()
        self.update_stats()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Печать отчета (выполненные заказы)", command=self.print_report)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        test_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Тестирование", menu=test_menu)
        test_menu.add_command(label="Запустить тесты", command=self.run_tests)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Справка", command=lambda: Documentation.show_help(self.root))
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def print_report(self):
        orders = self.db.get_completed_orders()
        if not orders and not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "Нет данных для печати\nБаза данных не подключена", 
                                             3000, True)
            return
        self.print_module.print_orders_report(orders, self.root)
    
    def show_large_notification(self, message, is_error=False):
        try:
            popup = tk.Toplevel(self.root)
            popup.title("Результаты тестирования")
            popup.geometry("500x300")
            
            if is_error:
                bg_color = '#e74c3c'
                icon_text = "⚠️"
            else:
                bg_color = '#2c3e50'
                icon_text = "✅"
            
            popup.configure(bg=bg_color)
            popup.attributes('-topmost', True)
            
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (500 // 2)
            y = (popup.winfo_screenheight() // 2) - (300 // 2)
            popup.geometry(f'+{x}+{y}')
            
            icon_label = tk.Label(popup, text=icon_text, font=('Arial', 32),
                                  bg=bg_color, fg='white')
            icon_label.pack(pady=(20, 10))
            
            text_frame = tk.Frame(popup, bg=bg_color)
            text_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            text_area = tk.Text(text_frame, font=('Courier', 10), 
                               bg=bg_color, fg='white', wrap=tk.WORD,
                               height=8, width=50)
            text_area.insert('1.0', message)
            text_area.configure(state='disabled')
            text_area.pack(side='left', fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_area.yview)
            scrollbar.pack(side='right', fill='y')
            text_area.configure(yscrollcommand=scrollbar.set)
            
            btn = tk.Button(popup, text="Закрыть", command=popup.destroy,
                           bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                           padx=20, pady=5, cursor='hand2')
            btn.pack(pady=15)
            
        except Exception as e:
            messagebox.showinfo("Результаты тестирования", message)
    
    def run_tests(self):
        self.audio.play_sound("assign")
        results = ModuleTests.run_all_tests(self.db)
        
        result_text = "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:\n\n"
        has_error = False
        for test_name, (success, message) in zip(
            ["Подключение к БД", "Звуковой модуль"],
            results
        ):
            status = "ПРОЙДЕН" if success else "НЕ ПРОЙДЕН"
            result_text += f"{test_name}: {status}\n   {message}\n\n"
            if not success:
                has_error = True
        
        self.show_large_notification(result_text, has_error)
    
    def create_notebook(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[15, 5])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_order = tk.Frame(self.notebook, bg='#f5f5f5')
        self.tab_active = tk.Frame(self.notebook, bg='#f5f5f5')
        self.tab_drivers = tk.Frame(self.notebook, bg='#f5f5f5')
        self.tab_completed = tk.Frame(self.notebook, bg='#f5f5f5')
        
        self.notebook.add(self.tab_order, text="Новый заказ")
        self.notebook.add(self.tab_active, text="Активные заказы")
        self.notebook.add(self.tab_drivers, text="Водители")
        self.notebook.add(self.tab_completed, text="Выполненные")
        
        self.setup_order_tab()
        self.setup_active_tab()
        self.setup_drivers_tab()
        self.setup_completed_tab()
    
    def setup_order_tab(self):
        title_frame = tk.Frame(self.tab_order, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="Создание нового заказа", 
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(expand=True)
        
        hotkey_frame = tk.Frame(self.tab_order, bg='#ecf0f1', height=30)
        hotkey_frame.pack(fill='x')
        hotkey_frame.pack_propagate(False)
        tk.Label(hotkey_frame, text="Нажмите Enter для быстрого создания заказа",
                font=('Arial', 10), bg='#ecf0f1', fg='#7f8c8d').pack(pady=5)
        
        form_frame = tk.Frame(self.tab_order, bg='white', relief='groove', bd=2)
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        fields = [("ФИО клиента:", "client_name"), ("Телефон:", "client_phone"),
                  ("Откуда:", "start_address"), ("Куда:", "end_address"), ("Тариф:", "tariff")]
        
        self.entries = {}
        tariffs = self.db.get_tariffs()
        tariff_names = [f"{t['name']} - {t['price_per_km']} руб/км" for t in tariffs]
        
        for i, (label, key) in enumerate(fields):
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=12, padx=20)
            tk.Label(frame, text=label, width=12, anchor='w', 
                    font=('Arial', 12, 'bold'), bg='white').pack(side='left')
            if key == "tariff":
                self.entries[key] = ttk.Combobox(frame, values=tariff_names, font=('Arial', 12), width=50)
                self.entries[key].current(0)
            else:
                self.entries[key] = tk.Entry(frame, font=('Arial', 12), width=50)
                self.entries[key].bind('<Return>', lambda e: self.create_order())
            self.entries[key].pack(side='left', padx=(10, 0), fill='x', expand=True)
        
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(pady=25)
        
        self.create_btn = tk.Button(btn_frame, text="СОЗДАТЬ ЗАКАЗ (Enter)", command=self.create_order,
                 bg='#27ae60', fg='white', font=('Arial', 14, 'bold'), padx=40, pady=12,
                 cursor='hand2', relief='raised', bd=2)
        self.create_btn.pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Случайный бонус", command=self.show_random_bonus,
                 bg='#f39c12', fg='white', font=('Arial', 11), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=10)
    
    def create_order(self):
        client_name = self.entries["client_name"].get().strip()
        client_phone = self.entries["client_phone"].get().strip()
        start_addr = self.entries["start_address"].get().strip()
        end_addr = self.entries["end_address"].get().strip()
        
        if not all([client_name, client_phone, start_addr, end_addr]):
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Заполните все поля", 2000, True)
            return
        
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "База данных не подключена\nЗапустите XAMPP и MySQL", 
                                             3000, True)
            return
        
        tariffs = self.db.get_tariffs()
        tariff_id = self.entries["tariff"].current() + 1
        
        ride_id = self.db.create_order(client_name, client_phone, start_addr, end_addr, tariff_id, self.dispatcher_id)
        
        if ride_id:
            self.audio.play_sound("order")
            AnimationModule.show_notification(self.root, "Успех", f"Заказ #{ride_id} создан!\nСтатус: НОВЫЙ", 2500)
        
        for key in self.entries:
            if key != "tariff":
                self.entries[key].delete(0, tk.END)
        
        self.refresh_active()
        self.update_stats()
    
    def show_random_bonus(self):
        bonuses = [
            "Скидка 10% на следующую поездку",
            "Бесплатная подача автомобиля",
            "Кофе в подарок",
            "Накопительная скидка 5%",
            "Бонус 100 рублей на счет",
            "Бесплатные 5 минут ожидания"
        ]
        bonus = random.choice(bonuses)
        self.audio.play_sound("complete")
        AnimationModule.show_notification(self.root, "Случайный бонус", f"Клиент получает:\n{bonus}", 2500)
    
    def setup_active_tab(self):
        title_frame = tk.Frame(self.tab_active, bg='#34495e', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Активные заказы", 
                font=('Arial', 16, 'bold'), bg='#34495e', fg='white').pack(side='left', padx=20, pady=15)
        
        status_info = tk.Label(title_frame, text="Новые | Назначены | В процессе", 
                               font=('Arial', 10), bg='#34495e', fg='#ecf0f1')
        status_info.pack(side='right', padx=20)
        
        table_frame = tk.Frame(self.tab_active, bg='#f5f5f5')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Статус', 'Клиент', 'Телефон', 'Откуда', 'Куда', 'Водитель')
        self.active_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=18)
        
        col_widths = [50, 100, 150, 120, 200, 200, 150]
        for col, width in zip(columns, col_widths):
            self.active_tree.heading(col, text=col)
            self.active_tree.column(col, width=width, anchor='center')
        
        self.active_tree.tag_configure('new', background='#e8f5e9')
        self.active_tree.tag_configure('assigned', background='#fff3e0')
        self.active_tree.tag_configure('in_progress', background='#ffe0b2')
        
        self.active_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.active_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.active_tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.tab_active, bg='#f5f5f5')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(btn_frame, text="Обновить", command=self.refresh_active,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Назначить водителя", command=self.assign_driver,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Начать поездку", command=self.start_ride,
                 bg='#f39c12', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Завершить заказ", command=self.complete_ride,
                 bg='#16a085', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Отменить заказ", command=self.cancel_ride,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        self.refresh_active()
    
    def refresh_active(self):
        for i in self.active_tree.get_children():
            self.active_tree.delete(i)
        
        orders = self.db.get_active_orders()
        if not orders and not self.db.is_connected():
            self.active_tree.insert('', 'end', values=("—", "—", "—", "—", "—", "—", "БД не подключена"), tags=())
            return
        
        status_icons = {'new': 'НОВЫЙ', 'assigned': 'НАЗНАЧЕН', 'in_progress': 'В ПУТИ'}
        
        for order in orders:
            status = order['status']
            tag = status if status in ['new', 'assigned', 'in_progress'] else ''
            self.active_tree.insert('', 'end', values=(
                order['id'],
                status_icons.get(status, status),
                order['client_name'],
                order['client_phone'],
                order['start_address'][:30],
                order['end_address'][:30],
                order.get('driver_name', 'Не назначен')
            ), tags=(tag,))
    
    def assign_driver(self):
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "База данных не подключена", 2000, True)
            return
        
        selected = self.active_tree.selection()
        if not selected:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Выберите заказ", 2000, True)
            return
        
        item = self.active_tree.item(selected[0])
        ride_id = item['values'][0]
        current_status = item['values'][1]
        
        if 'НАЗНАЧЕН' in current_status or 'В ПУТИ' in current_status:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", 
                                             f"Нельзя назначить водителя на заказ со статусом: {current_status}", 
                                             2500, True)
            return
        
        drivers = self.db.get_free_drivers()
        if not drivers:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Нет свободных водителей", 2000, True)
            return
        
        win = tk.Toplevel(self.root)
        win.title("Назначение водителя")
        win.geometry("450x250")
        win.configure(bg='white')
        
        tk.Label(win, text=f"Заказ #{ride_id}", font=('Arial', 14, 'bold'), bg='white').pack(pady=15)
        tk.Label(win, text="Выберите водителя:", font=('Arial', 12), bg='white').pack()
        
        combo = ttk.Combobox(win, values=[f"{d['id']} - {d['full_name']} ({d['car_number']})" for d in drivers],
                            font=('Arial', 11), width=35)
        combo.pack(pady=15)
        
        def assign():
            if not combo.get():
                return
            driver_id = combo.get().split(" - ")[0]
            self.db.assign_driver(ride_id, driver_id)
            self.audio.play_sound("assign")
            AnimationModule.show_notification(self.root, "Успех", "Водитель назначен", 2000)
            win.destroy()
            self.refresh_active()
            self.refresh_drivers()
            self.update_stats()
        
        tk.Button(win, text="Назначить", command=assign,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=8,
                 cursor='hand2').pack(pady=10)
    
    def start_ride(self):
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "База данных не подключена", 2000, True)
            return
        
        selected = self.active_tree.selection()
        if not selected:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Выберите заказ", 2000, True)
            return
        
        item = self.active_tree.item(selected[0])
        ride_id = item['values'][0]
        current_status = item['values'][1]
        
        if 'НАЗНАЧЕН' not in current_status:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", 
                                             "Начать поездку можно только для заказа со статусом 'НАЗНАЧЕН'", 
                                             2500, True)
            return
        
        if QuestionDialog.askyesno("Подтверждение", f"Начать поездку по заказу #{ride_id}?"):
            self.db.start_ride(ride_id)
            self.audio.play_sound("start")
            AnimationModule.show_notification(self.root, "Успех", "Поездка начата", 2000)
            self.refresh_active()
            self.update_stats()
    
    def complete_ride(self):
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "База данных не подключена", 2000, True)
            return
        
        selected = self.active_tree.selection()
        if not selected:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Выберите заказ", 2000, True)
            return
        
        item = self.active_tree.item(selected[0])
        ride_id = item['values'][0]
        current_status = item['values'][1]
        
        if 'В ПУТИ' not in current_status:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", 
                                             "Завершить можно только заказ со статусом 'В ПУТИ'", 
                                             2500, True)
            return
        
        if QuestionDialog.askyesno("Подтверждение", f"Завершить заказ #{ride_id}?"):
            self.db.complete_ride(ride_id)
            self.audio.play_sound("complete")
            AnimationModule.show_notification(self.root, "Успех", f"Заказ #{ride_id} завершен", 2000)
            self.refresh_active()
            self.refresh_completed()
            self.refresh_drivers()
            self.update_stats()
    
    def cancel_ride(self):
        if not self.db.is_connected():
            AnimationModule.show_notification(self.root, "Ошибка", 
                                             "База данных не подключена", 2000, True)
            return
        
        selected = self.active_tree.selection()
        if not selected:
            self.audio.play_sound("error")
            AnimationModule.show_notification(self.root, "Внимание", "Выберите заказ", 2000, True)
            return
        
        item = self.active_tree.item(selected[0])
        ride_id = item['values'][0]
        
        if QuestionDialog.askyesno("Подтверждение", f"Отменить заказ #{ride_id}?"):
            self.db.cancel_ride(ride_id)
            self.audio.play_sound("cancel")
            AnimationModule.show_notification(self.root, "Успех", f"Заказ #{ride_id} отменен", 2000)
            self.refresh_active()
            self.refresh_drivers()
            self.update_stats()
    
    def setup_drivers_tab(self):
        title_frame = tk.Frame(self.tab_drivers, bg='#34495e', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="Список водителей", 
                font=('Arial', 16, 'bold'), bg='#34495e', fg='white').pack(expand=True)
        
        table_frame = tk.Frame(self.tab_drivers, bg='#f5f5f5')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'ФИО', 'Телефон', 'Автомобиль', 'Номер', 'Статус')
        self.driver_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [50, 150, 120, 120, 100, 100]
        for col, width in zip(columns, col_widths):
            self.driver_tree.heading(col, text=col)
            self.driver_tree.column(col, width=width, anchor='center')
        
        self.driver_tree.tag_configure('available', background='#e8f5e9')
        self.driver_tree.tag_configure('on_shift', background='#fff3e0')
        self.driver_tree.tag_configure('busy', background='#ffebee')
        
        self.driver_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.driver_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.driver_tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.tab_drivers, bg='#f5f5f5')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(btn_frame, text="Обновить", command=self.refresh_drivers,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8,
                 cursor='hand2').pack()
        
        self.refresh_drivers()
    
    def refresh_drivers(self):
        for i in self.driver_tree.get_children():
            self.driver_tree.delete(i)
        
        drivers = self.db.get_drivers()
        if not drivers and not self.db.is_connected():
            self.driver_tree.insert('', 'end', values=("—", "—", "—", "—", "—", "БД не подключена"), tags=())
            return
        
        status_icons = {'available': 'Свободен', 'on_shift': 'На смене', 'busy': 'Занят'}
        
        for d in drivers:
            tag = d['status'] if d['status'] in ['available', 'on_shift', 'busy'] else ''
            self.driver_tree.insert('', 'end', values=(
                d['id'], d['full_name'], d['phone'], d['car_model'],
                d['car_number'], status_icons.get(d['status'], d['status'])
            ), tags=(tag,))
    
    def setup_completed_tab(self):
        title_frame = tk.Frame(self.tab_completed, bg='#34495e', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="Выполненные заказы", 
                font=('Arial', 16, 'bold'), bg='#34495e', fg='white').pack(expand=True)
        
        table_frame = tk.Frame(self.tab_completed, bg='#f5f5f5')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Клиент', 'Откуда', 'Куда', 'Водитель', 'Дата')
        self.completed_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        col_widths = [50, 150, 200, 200, 150, 150]
        for col, width in zip(columns, col_widths):
            self.completed_tree.heading(col, text=col)
            self.completed_tree.column(col, width=width, anchor='center')
        
        self.completed_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.completed_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.completed_tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.tab_completed, bg='#f5f5f5')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(btn_frame, text="Обновить", command=self.refresh_completed,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Печать отчета (PDF)", command=self.print_report,
                 bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8,
                 cursor='hand2').pack(side='left', padx=5)
        
        self.refresh_completed()
    
    def refresh_completed(self):
        for i in self.completed_tree.get_children():
            self.completed_tree.delete(i)
        
        orders = self.db.get_completed_orders()
        if not orders and not self.db.is_connected():
            self.completed_tree.insert('', 'end', values=("—", "—", "—", "—", "—", "БД не подключена"), tags=())
            return
        
        for order in orders:
            date_str = order['completed_at'].strftime('%d.%m.%Y %H:%M') if order['completed_at'] else ''
            self.completed_tree.insert('', 'end', values=(
                order['id'], order['client_name'], order['start_address'][:30],
                order['end_address'][:30], order.get('driver_name', 'Не указан'), date_str
            ))
    
    def create_statusbar(self):
        self.statusbar = tk.Frame(self.root, bg='#2c3e50', height=35)
        self.statusbar.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(self.statusbar, text="Готов к работе", 
                                     bg='#2c3e50', fg='white', font=('Arial', 9))
        self.status_label.pack(side='left', padx=15)
        
        self.stats_label = tk.Label(self.statusbar, text="", 
                                    bg='#2c3e50', fg='white', font=('Arial', 10))
        self.stats_label.pack(side='right', padx=15)
    
    def update_stats(self):
        if not self.db.is_connected():
            self.stats_label.config(text="БД не подключена")
            return
        new, assigned, in_progress, available = self.db.get_stats()
        self.stats_label.config(text=f"Новых: {new} | Назначено: {assigned} | В пути: {in_progress} | Свободных: {available}")
    
    def show_about(self):
        about_text = ("Таксопарк - Диспетчерская\n\n"
                      "Версия: 2.0\n\n"
                      "Функции:\n"
                      "- Создание заказов (Enter)\n"
                      "- Назначение водителей\n"
                      "- Начало/завершение поездок\n"
                      "- Отмена заказов\n"
                      "- Статусы заказов\n"
                      "- Звуковые уведомления\n"
                      "- Анимированные уведомления\n"
                      "- Печать отчетов (PDF)\n"
                      "- Тестирование модулей\n"
                      "- Случайный бонус")
        
        AnimationModule.show_notification(self.root, "О программе", about_text, 4000)


if __name__ == "__main__":
    root = tk.Tk()
    app = DispatcherApp(root)
    root.mainloop()