from customtkinter import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw
class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("LogiTalk")
        self.avatar_path = None
        self.avatar_img = None
        self.current_font = ("Arial", 16)
        self.chat_frame = CTkScrollableFrame(self, width=500, height=400)
        self.chat_frame.place(x=0, y=0)
        self.e = CTkEntry(self, width=500, height=50, placeholder_text="Введіть повідомлення...", font=("Arial", 20))
        self.e.place(x=0, y=450)
        self.e.bind("<Return>", lambda event: self.s_m())
        self.username = None
        self.b_frame = CTkFrame(self, width=700, height=700, fg_color="transparent")
        self.b_frame.place(x=0, y=0)
        self.e1 = CTkEntry(self.b_frame, width=250, height=60, placeholder_text="Введіть своє ім'я...", font=self.current_font)
        self.e1.place(x=125, y=200)
        self.b1 = CTkButton(self.b_frame, width=100, height=50, text="OK", font=self.current_font, command=self.login)
        self.b1.place(x=200, y=280)
        self.avatar_button = CTkButton(self.b_frame, text="Вибрати аватарку", font=self.current_font, command=self.choose_avatar)
        self.avatar_button.place(x=175, y=360)
        self.font_option = CTkOptionMenu(self.b_frame, values=["Arial", "Times New Roman", "Courier New", "Helvetica"], command=self.change_font)
        self.font_option.set("Arial")
        self.font_option.place(x=180, y=420)
        self.sock = socket(AF_INET, SOCK_STREAM)
        try:
            self.sock.connect(('0.tcp.eu.ngrok.io', 13578))
            Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Не вдалося підключитися: {e}")
    def change_font(self, font_name):
        self.current_font = (font_name, 16)
        self.e.configure(font=self.current_font)
        self.e1.configure(font=self.current_font)
        self.b1.configure(font=self.current_font)
        self.avatar_button.configure(font=self.current_font)
        self.font_option.configure(font=self.current_font)
    def choose_avatar(self):
        path = askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.avatar_path = path
            img = Image.open(self.avatar_path).convert("RGBA").resize((40, 40))
            mask = Image.new('L', (40, 40), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 40, 40), fill=255)
            img.putalpha(mask)
            self.avatar_img = CTkImage(light_image=img, size=(40, 40))
    def login(self):
        self.username = self.e1.get()
        if self.username:
            self.b_frame.destroy()
            self.font_option_main = CTkOptionMenu(self, values=["Arial", "Times New Roman", "Courier New", "Helvetica"], command=self.change_font)
            self.font_option_main.set(self.current_font[0])
            self.font_option_main.place(x=360, y=415)
        else:
            CTkLabel(self.b_frame, text='Ім`я не може бути пустим!', text_color='red', font=self.current_font).place(x=155, y=460)
    def s_m(self):
        message = self.e.get().strip()
        if message:
            full_message = f"{self.username}: {message}"
            self.a_m(full_message, is_own=True)
            try:
                self.sock.send(full_message.encode())
            except:
                self.sock.close()
            self.e.delete(0, END)
    def a_m(self, message, is_own=False):
        msg_frame = CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.pack(anchor="w", pady=5, padx=10)
        if self.avatar_img:
            avatar_label = CTkLabel(msg_frame, image=self.avatar_img, text="")
            avatar_label.pack(side="left", padx=5)
        msg_label = CTkLabel(msg_frame, text=message, font=self.current_font, anchor="w", justify="left", wraplength=350)
        msg_label.pack(side="left")
    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if msg:
                    self.a_m(msg, is_own=False)
            except:
                break
window = MainWindow()
window.mainloop()