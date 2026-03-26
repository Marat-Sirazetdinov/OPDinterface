import customtkinter as ctk
from tkinter import filedialog
import os
import random


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Seismic Data Suite")
        self.geometry("1100x800")

        # --- ЛОГИКА УМНОЙ НАВИГАЦИИ ---
        self.current_state = {
            "tab": "Файл",
            "theme": "System",
            "scale": "100%"
        }
        self.history = [self.current_state.copy()]
        self.history_index = 0
        self.is_navigating = False

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ ---
        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(fill="x", padx=15, pady=(10, 0))

        # Логотип
        self.logo_label = ctk.CTkLabel(self.top_container, text="SEIS",
                                       font=("Arial", 24, "bold"), text_color="#3b8ed0")
        self.logo_label.pack(side="left", padx=(0, 15))

        # Навигация (стрелки)
        self.nav_frame = ctk.CTkFrame(self.top_container, fg_color="transparent")
        self.nav_frame.pack(side="left")

        self.btn_back = ctk.CTkButton(self.nav_frame, text="←", width=35, height=35, fg_color="gray30",
                                      command=self.go_back)
        self.btn_back.pack(side="left", padx=1)
        self.btn_forward = ctk.CTkButton(self.nav_frame, text="→", width=35, height=35, fg_color="gray30",
                                         command=self.go_forward)
        self.btn_forward.pack(side="left", padx=1)

        # Вкладки
        self.tab_buttons = {}
        self.tabs_list = ["Файл", "Главная", "Данные", "Анализ", "Вид"]
        for name in self.tabs_list:
            btn = ctk.CTkButton(self.top_container, text=name, width=85, height=35,
                                fg_color="transparent", text_color=("gray10", "gray80"),
                                command=lambda n=name: self.save_state(tab=n))
            btn.pack(side="left", padx=1)
            self.tab_buttons[name] = btn

        # --- 2. ПАНЕЛЬ ИНСТРУМЕНТОВ ---
        self.ribbon = ctk.CTkFrame(self, height=105, corner_radius=0, border_width=1, border_color=("gray70", "gray30"))
        self.ribbon.pack(fill="x", padx=0, pady=(5, 0))
        self.ribbon.pack_propagate(False)

        # --- 3. КОНТЕЙНЕР ДЛЯ КОНТЕНТА ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for name in self.tabs_list:
            frame = ctk.CTkFrame(self.container, fg_color="transparent")
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.setup_file_page()
        self.setup_ribbon_tools()
        self.setup_view_settings()

        # Заглушки
        ctk.CTkLabel(self.frames["Главная"], text="Рабочая область: ГЛАВНАЯ", font=("Arial", 16, "italic")).pack(
            pady=50)
        ctk.CTkLabel(self.frames["Данные"], text="Когда-нибудь тут будут данные", font=("Arial", 24)).pack(pady=100)
        ctk.CTkLabel(self.frames["Анализ"], text="Когда-нибудь тут будет происходить анализ", font=("Arial", 24)).pack(
            pady=100)

        # Инициализация
        self.apply_state(self.current_state)

    def setup_ribbon_tools(self):
        self.home_tools = ctk.CTkFrame(self.ribbon, fg_color="transparent")

        def add_tool(icon, text, cmd):
            btn = ctk.CTkButton(self.home_tools,
                                text=f"{icon}\n{text}",
                                fg_color=("#eeeeee", "#333333"),
                                text_color=("#1a1a1a", "#ffffff"),
                                hover_color=("#dddddd", "#444444"),
                                border_width=1,
                                border_color=("#cccccc", "#444444"),
                                corner_radius=8,
                                width=100,
                                height=80,
                                font=("Arial", 12, "bold"),
                                command=cmd)
            btn.pack(side="left", padx=4, pady=10)  # Сократили padx до 4

        add_tool("⚙️", "Настройки", lambda: print("Настройки"))
        add_tool("⏳", "Фильтр", lambda: print("Фильтр"))
        add_tool("📈", "Амплитуда", lambda: print("Амплитуда"))

    def setup_file_page(self):
        """Стабильная большая область загрузки"""
        self.upload_box = ctk.CTkFrame(self.frames["Файл"], border_width=2, width=700, height=450)
        self.upload_box.place(relx=0.5, rely=0.5, anchor="center")
        self.upload_box.pack_propagate(False)

        ctk.CTkLabel(self.upload_box, text="Область загрузки", font=("Arial", 26, "bold")).pack(pady=(80, 10))
        ctk.CTkLabel(self.upload_box, text="Доступные форматы: .sgy, .segy",
                     font=("Arial", 14), text_color="#3b8ed0").pack(pady=(0, 30))

        self.btn_select = ctk.CTkButton(self.upload_box, text="Выбрать файл",
                                        width=200, height=50, font=("Arial", 16),
                                        command=self.open_file_dialog)
        self.btn_select.pack(pady=10)

        self.file_status = ctk.CTkLabel(self.upload_box, text="Файл не выбран", font=("Arial", 14), text_color="gray")
        self.file_status.pack(pady=40)

    def open_file_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Seismic data", "*.sgy *.segy")])
        if path:
            name = os.path.basename(path)
            self.file_status.configure(text=f"Успешно загружен: {name}", text_color="#2ecc71")

    def setup_view_settings(self):
        f = self.frames["Вид"]
        ctk.CTkLabel(f, text="Настройки интерфейса", font=("Arial", 24, "bold")).pack(pady=40)
        container = ctk.CTkFrame(f, fg_color="transparent")
        container.pack()
        # Тема и Масштаб (как в прошлом коде)
        for lbl, vals, opt in [("Тема приложения:", ["System", "Dark", "Light"], "theme"),
                               ("Масштаб:", ["80%", "100%", "120%"], "scale")]:
            r = ctk.CTkFrame(container, fg_color="transparent")
            r.pack(pady=10)
            ctk.CTkLabel(r, text=lbl, width=150, anchor="w", font=("Arial", 14)).pack(side="left")
            menu = ctk.CTkOptionMenu(r, values=vals, command=lambda v, o=opt: self.save_state(**{o: v}))
            menu.pack(side="left")
            if opt == "theme":
                self.theme_menu = menu
            else:
                self.scale_menu = menu

    # --- УМНАЯ НАВИГАЦИЯ ---
    def save_state(self, tab=None, theme=None, scale=None):
        if self.is_navigating: return
        if tab: self.current_state["tab"] = tab
        if theme: self.current_state["theme"] = theme
        if scale: self.current_state["scale"] = scale
        if self.current_state == self.history[self.history_index]: return
        self.history = self.history[:self.history_index + 1]
        self.history.append(self.current_state.copy())
        self.history_index += 1
        self.apply_state(self.current_state)

    def apply_state(self, state):
        self.is_navigating = True
        name = state["tab"]
        self.frames[name].tkraise()
        for t_name, btn in self.tab_buttons.items():
            btn.configure(fg_color="#3b8ed0" if t_name == name else "transparent",
                          text_color="white" if t_name == name else ("gray10", "gray80"))
        if name == "Главная":
            self.home_tools.pack(side="left", padx=15)
            self.ribbon.configure(fg_color=("#f9f9f9", "#2b2b2b"))
        else:
            self.home_tools.pack_forget()
            self.ribbon.configure(fg_color="transparent")
        ctk.set_appearance_mode(state["theme"])
        self.theme_menu.set(state["theme"])
        ctk.set_widget_scaling(int(state["scale"].replace("%", "")) / 100)
        self.scale_menu.set(state["scale"])
        self.btn_back.configure(state="normal" if self.history_index > 0 else "disabled",
                                fg_color="#3b8ed0" if self.history_index > 0 else "gray30")
        self.btn_forward.configure(state="normal" if self.history_index < len(self.history) - 1 else "disabled",
                                   fg_color="#3b8ed0" if self.history_index < len(self.history) - 1 else "gray30")
        self.is_navigating = False

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.current_state = self.history[self.history_index].copy()
            self.apply_state(self.current_state)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_state = self.history[self.history_index].copy()
            self.apply_state(self.current_state)


if __name__ == "__main__":
    app = App()
    app.mainloop()