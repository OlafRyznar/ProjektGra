import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import ImageTk, Image
import random
import time

class MemoryGameMenu:
    def __init__(self, root):
        self.root = root
        self.frame_color = '#ADD8E6'  # Domyślny kolor tła dla current_frame
        self.root.configure(bg=self.frame_color)
        self.root.title("Memory Game")
        self.root.geometry("600x600")
        self.current_frame = None
        self.start_time = None
        self.timer_label = None
        self.elapsed_time = None
        self.end = None

        self.show_main_menu()

    def show_main_menu(self): #Przyciski w menu głównym
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.frame_color)
        self.current_frame.pack(pady=50)

        self.title_label = tk.Label(self.current_frame, text="Memory Game", bg=self.frame_color, font=("Arial", 24))
        self.title_label.pack(pady=20)

        create_board_button = tk.Button(self.current_frame, text="Stwórz plansze", command=self.show_create_board_menu,
                                        font=("Arial", 16), width=20, background="green")
        create_board_button.pack(pady=10)

        start_button = tk.Button(self.current_frame, text="Wybierz poziom trudności", command=self.show_difficulty_menu,
                                 font=("Arial", 16), width=20, background="red")
        start_button.pack(pady=10)

        last_games_button = tk.Button(self.current_frame, text="Ostatnie gry", command=self.show_last_games,
                                      font=("Arial", 16), width=20, background="yellow")
        last_games_button.pack(pady=10)

        rules_button = tk.Button(self.current_frame, text="Zasady", command=self.show_game_rules,
                                 font=("Arial", 16), width=20, background="grey")
        rules_button.pack(pady=10)

        ##color_button = tk.Button(self.current_frame, text="Change Frame Color", command=self.change_background_color, font=("Arial", 16), width=20, background="white", foreground="black")
        ##color_button.pack(pady=10)
        ##Nie do konca to dziala, nie zmieniaja sie kolory wszedzie, gdzie chce


        exit_button = tk.Button(self.current_frame, text="Wyjdź", command=self.exit_game,
                                font=("Arial", 16), width=20, background="black", foreground="white")
        exit_button.pack(pady=10)



    def show_create_board_menu(self): #Przyciski w tworzeniu własnej planszy
        self.clear_frame()

        self.current_frame = tk.Frame(self.root,bg=self.frame_color )
        self.current_frame.pack(pady=50)

        title_label = tk.Label(self.current_frame,bg=self.frame_color, text="Utwórz plansze", font=("Arial", 24))
        title_label.pack(pady=20)

        size_label = tk.Label(self.current_frame,bg=self.frame_color, text="Wpisz rozmiar planszy podając jedną liczbe parzystą")
        size_label.pack()

        size_entry = tk.Entry(self.current_frame, width=10)
        size_entry.pack(pady=10)

        create_button = tk.Button(self.current_frame, text="Utwórz", command=lambda: self.create_board(size_entry.get()))
        create_button.pack(pady=10)

        back_button = tk.Button(self.current_frame, text="Wróć", command=self.show_main_menu)
        back_button.pack(pady=10)

    def create_board(self, size):
        try:
            size = int(size)
            if size <= 1 or size % 2 != 0:
                messagebox.showerror("Złe dane","Zły rozmiar, liczba musi być parzysta i większa od 1")
            else:
                self.start_game(size)
        except ValueError:
            messagebox.showerror("Podaj liczbe")

    def show_difficulty_menu(self): #Przyciski w wyborze trudności
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.frame_color)
        self.current_frame.pack(pady=50)

        title_label = tk.Label(self.current_frame, text="Wybierz poziom trudności",bg=self.frame_color, font=("Arial", 24))
        title_label.pack(pady=20)

        easy_button = tk.Button(self.current_frame, text="Łatwy (4x4)", command=lambda: self.start_game(4), font=("Arial", 16), width=20, background="green")
        easy_button.pack(pady=10)

        medium_button = tk.Button(self.current_frame, text="Średni (6x6)", command=lambda: self.start_game(6), font=("Arial", 16), width=20, background="yellow")
        medium_button.pack(pady=10)

        hard_button = tk.Button(self.current_frame, text="Trudny (8x8)", command=lambda: self.start_game(8), font=("Arial", 16), width=20, background="red")
        hard_button.pack(pady=10)

        back_button = tk.Button(self.current_frame, text="Wróć", command=self.show_main_menu,)
        back_button.pack(pady=10)

    def start_game(self, size):
  
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg= self.frame_color)
        self.current_frame.pack(pady=50)

        self.start_time = time.time()

        # Lista dostępnych obrazków
        image_filenames = [f"{i}.png" for i in range(1, (size * size) // 2 + 1)] * 2
        random.shuffle(image_filenames)

        # Funkcja obsługująca kliknięcie przycisku
        def button_click(row, col):
            button = buttons[row][col]
            if button["state"] == tk.DISABLED:
                return

            image = Image.open(image_filenames[row * size + col])
            image = image.resize((90, 90), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button.configure(image=photo)
            button.image = photo
            button["state"] = tk.DISABLED

            # Sprawdzanie, czy wybrane karty są takie same
            if len(guessed_cards) == 1:
                prev_row, prev_col = guessed_cards[0]
                if image_filenames[row * size + col] == image_filenames[prev_row * size + prev_col]:
                    buttons[prev_row][prev_col]["state"] = tk.DISABLED
                    guessed_cards.clear()
                    check_game_over()
                else:
                    root.after(1000, reset_cards, row, col, prev_row, prev_col)
            else:
                guessed_cards.append((row, col))
                
            # Zwiększanie licznika ruchów
            if self.end != 1:
                self.moves += 1
            self.update_moves_label()
            self.update_timer_label()

        # Funkcja resetująca nieodgadnięte karty
        def reset_cards(row1, col1, row2, col2):
            buttons[row1][col1].configure(image=cover_image)
            buttons[row2][col2].configure(image=cover_image)
            buttons[row1][col1]["state"] = tk.NORMAL
            buttons[row2][col2]["state"] = tk.NORMAL
            guessed_cards.clear()

        # Funkcja sprawdzająca, czy gra została ukończona
        def check_game_over():
            for row in buttons:
                for button in row:
                    if button["state"] == tk.NORMAL:
                        return
            elapsed_time = int(time.time() - self.start_time)
            self.save_game_result(size, elapsed_time, self.moves)  # Zapis wyniku gry
            self.end = 1
            messagebox.showinfo("Wygrana", f"Gratulacje! Wygrałeś grę. Twój czas: {elapsed_time} sekund. Ruchy: {self.moves}")
            #self.moves = 0  # Resetowanie licznika ruchów
            #self.update_moves_label()
            self.update_timer_label()

        # Tworzenie przycisków
        buttons = []
        guessed_cards = []

        cover_image = ImageTk.PhotoImage(Image.open("cover.png").resize((90, 90), Image.LANCZOS))

        for row in range(size):
            button_row = []
            for col in range(size):
                button = tk.Button(self.current_frame, image=cover_image, command=lambda row=row, col=col: button_click(row, col),bg="green")
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            buttons.append(button_row)

        self.moves = 0  # Licznik ruchów

        self.moves_label = tk.Label(self.root, text="Ruchy: 0", font=("Arial", 16),bg=self.frame_color)
        self.moves_label.pack()

        self.timer_label = tk.Label(self.root, text=f"Czas: 0 sekund", font=("Arial", 16),bg=self.frame_color)
        self.timer_label.pack()

        back_button = tk.Button(self.current_frame, text="Wróć", command=self.go_back)
        back_button.grid(row=size, column=0, columnspan=size, pady=10)

    def go_back(self): #Powrót
        self.moves_label.destroy()
        self.timer_label.destroy()
        self.end = None
        self.show_main_menu()

    def start_timer(self): #Timer
        self.update_timer_label()

    def update_timer_label(self):
        if self.timer_label is not None:
            if self.end != 1:
                self.elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Czas: {self.elapsed_time} sekund")
            self.timer_label.after(1000, self.update_timer_label)

    def update_moves_label(self):
        if self.moves_label is not None:
            self.moves_label.config(text=f"Ruchy: {self.moves}")

    def show_last_games(self):
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.frame_color)
        self.current_frame.pack(pady=50)

        title_label = tk.Label(self.current_frame, text="Ostatnie gry", font=("Arial", 24), bg=self.frame_color)
        title_label.pack(pady=20)

        # Odczytanie ostatnich gier z pliku wyniki.txt
        try:
            with open("wyniki.txt", "r") as file:
                results = file.readlines()
        except FileNotFoundError:
            results = []

        if results:
            for i, result in enumerate(results[-5:], start=1):
                result_label = tk.Label(self.current_frame, text=result.strip(), font=("Arial", 16), bg=self.frame_color)
                result_label.pack()
        else:
            no_results_label = tk.Label(self.current_frame, text="Brak ostatnich gier", font=("Arial", 16))
            no_results_label.pack()

        back_button = tk.Button(self.current_frame, text="Wróć", command=self.show_main_menu)
        back_button.pack(pady=10)

    def save_game_result(self, size, elapsed_time, moves):
        # Zapis wyniku gry do pliku wyniki.txt
        with open("wyniki.txt", "a") as file:
            file.write(f"Rozmiar planszy: {size} | Czas: {elapsed_time} sekund | Ruchy: {moves}\n")

    def show_game_rules(self):
        messagebox.showinfo("Zasady gry", "Zasady gry memory:\n1. Na planszy są rozmieszczone zakryte kafelki.\n2. Klikając na kafelki, odsłaniasz ich zawartość.\n3. Jeśli kafelki są takie same, zostaną one odkryte na stałe. \n4. Jeśli kafelki się różnią, zostaną ponownie zakryte po chwili. \n5. Celem gry jest odnalezienie wszystkich par kafelków przy jak najmniejszej liczbie ruchów. ")
    def exit_game(self):
        self.root.destroy()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()

    # def change_background_color(self):
    #     color = colorchooser.askcolor(title="Choose Background Color")[1]
    #     if color:
    #         self.root.configure(bg=color)
    #         self.current_frame.configure(bg=color)
    #         self.title_label.configure(bg=color)

root = tk.Tk()
memory_game_menu = MemoryGameMenu(root)
root.mainloop()