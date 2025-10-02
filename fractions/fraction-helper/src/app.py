from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
from fractions import Fraction
import random

class FractionHelperApp:
    def __init__(self, master):
        self.master = master
        master.title("Fraction Helper")
        master.configure(bg="#f5f5f5")
        self.mode = StringVar(value='main')  # 'main', 'calc', or 'practice'
        self.points = 0
        self.practice_widgets = []
        self.main_widgets = []
        self.show_main_screen()

    def show_main_screen(self):
        self.clear_all_widgets()
        main_frame = Frame(self.master, bg="#f5f5f5")
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.main_widgets.append(main_frame)
        Label(main_frame, text="Fraction Helper", font=("Arial", 28, "bold"), bg="#f5f5f5", fg="#333").pack(pady=(0, 30))
        start_btn = Button(main_frame, text="Start", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", padx=30, pady=10, command=self.show_mode_selection)
        start_btn.pack(pady=(0, 10))
        self.main_widgets.append(start_btn)

    def show_mode_selection(self):
        self.clear_all_widgets()
        mode_frame = Frame(self.master, bg="#f5f5f5")
        mode_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.main_widgets.append(mode_frame)
        Label(mode_frame, text="Choose Mode", font=("Arial", 22, "bold"), bg="#f5f5f5", fg="#333").pack(pady=(0, 20))
        calc_btn = Button(mode_frame, text="Calculator", font=("Arial", 16), bg="#2196F3", fg="white", width=15, command=self.enter_calc_mode)
        calc_btn.pack(pady=10)
        practice_btn = Button(mode_frame, text="Practice Mode", font=("Arial", 16), bg="#FF9800", fg="white", width=15, command=self.enter_practice_mode)
        practice_btn.pack(pady=10)
        nav_frame = Frame(mode_frame, bg="#f5f5f5")
        nav_frame.pack(pady=(20,0))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_main_screen)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.main_widgets.extend([calc_btn, practice_btn, back_btn, home_btn])

    def enter_calc_mode(self):
        self.mode.set('calc')
        self.clear_all_widgets()
        if not hasattr(self, 'frame') or self.frame is None:
            self.frame = Frame(self.master, bg="#f5f5f5")
        else:
            self.frame = Frame(self.master, bg="#f5f5f5")
        self.frame.grid(row=0, column=0, padx=30, pady=30)
        self.build_fraction_ui()
        self.toggle_btn = Button(self.master, text="Switch to Divide", command=self.toggle_operation, font=("Arial", 12))
        self.toggle_btn.grid(row=1, column=0, pady=(0,5))
        self.practice_btn = Button(self.master, text="Practice Mode", command=self.enter_practice_mode, font=("Arial", 12))
        self.practice_btn.grid(row=3, column=0, pady=(0,5))
        nav_frame = Frame(self.master, bg="#f5f5f5")
        nav_frame.grid(row=5, column=0, pady=(0,5))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_mode_selection)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.main_widgets.extend([self.toggle_btn, self.practice_btn, nav_frame, back_btn, home_btn])

    def build_fraction_ui(self):
        # Clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.grid(row=0, column=0, padx=30, pady=30)
        # Fraction 1 (Mixed)
        Entry(self.frame, width=3, textvariable=self.whole1_var, justify='center', font=("Arial", 16)).grid(row=1, column=0, padx=5)
        Label(self.frame, text="", bg="#f5f5f5").grid(row=1, column=1)  # spacer
        Entry(self.frame, width=4, textvariable=self.num1_var, justify='center', font=("Arial", 16)).grid(row=0, column=2, padx=5)
        Label(self.frame, text="\u2014", font=("Arial", 18), bg="#f5f5f5").grid(row=1, column=2)
        Entry(self.frame, width=4, textvariable=self.den1_var, justify='center', font=("Arial", 16)).grid(row=2, column=2, padx=5)
        # Operator (recreate every time)
        op_symbol = "  ×  " if self.operation.get() == '*' else "  ÷  "
        self.operator_label = Label(self.frame, text=op_symbol, font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#2196F3")
        self.operator_label.grid(row=1, column=3, padx=10)
        # Fraction 2 (Mixed)
        Entry(self.frame, width=3, textvariable=self.whole2_var, justify='center', font=("Arial", 16)).grid(row=1, column=4, padx=5)
        Label(self.frame, text="", bg="#f5f5f5").grid(row=1, column=5)  # spacer
        Entry(self.frame, width=4, textvariable=self.num2_var, justify='center', font=("Arial", 16)).grid(row=0, column=6, padx=5)
        Label(self.frame, text="\u2014", font=("Arial", 18), bg="#f5f5f5").grid(row=1, column=6)
        Entry(self.frame, width=4, textvariable=self.den2_var, justify='center', font=("Arial", 16)).grid(row=2, column=6, padx=5)
        # Equals sign
        Label(self.frame, text="  =  ", font=("Arial", 20, "bold"), bg="#f5f5f5").grid(row=1, column=7, padx=10)
        # Result fraction (readonly)
        Entry(self.frame, width=4, textvariable=self.res_num_var, justify='center', state='readonly', font=("Arial", 16), disabledbackground="#e0e0e0").grid(row=0, column=8, padx=5)
        Label(self.frame, text="\u2014", font=("Arial", 18), bg="#f5f5f5").grid(row=1, column=8)
        Entry(self.frame, width=4, textvariable=self.res_den_var, justify='center', state='readonly', font=("Arial", 16), disabledbackground="#e0e0e0").grid(row=2, column=8, padx=5)
        # Labels for whole part
        Label(self.frame, text="", bg="#f5f5f5").grid(row=0, column=0)  # empty above whole
        Label(self.frame, text="", bg="#f5f5f5").grid(row=2, column=0)  # empty below whole
        Label(self.frame, text="", bg="#f5f5f5").grid(row=0, column=4)
        Label(self.frame, text="", bg="#f5f5f5").grid(row=2, column=4)

    def toggle_operation(self):
        if self.operation.get() == '*':
            self.operation.set('/')
            self.toggle_btn.config(text="Switch to Multiply")
        else:
            self.operation.set('*')
            self.toggle_btn.config(text="Switch to Divide")
        self.build_fraction_ui()

    def get_fraction(self, whole_var, num_var, den_var):
        try:
            whole = int(whole_var.get()) if whole_var.get() else 0
            num = int(num_var.get()) if num_var.get() else 0
            den = int(den_var.get()) if den_var.get() else 1
            if den == 0:
                raise ValueError("Denominator cannot be zero.")
            frac = Fraction(abs(num), den)
            if whole < 0:
                frac = -frac
            return Fraction(whole) + frac if whole >= 0 else Fraction(whole) - frac
        except Exception as e:
            raise ValueError("Invalid mixed number input.")

    def calculate(self):
        try:
            frac1 = self.get_fraction(self.whole1_var, self.num1_var, self.den1_var)
            frac2 = self.get_fraction(self.whole2_var, self.num2_var, self.den2_var)
            if self.operation.get() == '*':
                result = frac1 * frac2
            else:
                if frac2 == 0:
                    raise ValueError("Cannot divide by zero.")
                result = frac1 / frac2
            self.res_num_var.set(str(result.numerator))
            self.res_den_var.set(str(result.denominator))
        except Exception as e:
            messagebox.showerror("Invalid input", f"Please enter valid mixed numbers.\n{e}")

    def enter_practice_mode(self):
        self.mode.set('practice')
        self.clear_all_widgets()
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        self.difficulty_var = StringVar(value='easy')
        diff_frame = Frame(self.master, bg="#f5f5f5")
        diff_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.practice_widgets = [diff_frame]
        Label(diff_frame, text="Select Difficulty:", font=("Arial", 16, "bold"), bg="#f5f5f5").grid(row=0, column=0, columnspan=3, pady=(0,10))
        Button(diff_frame, text="Easy", font=("Arial", 14), command=lambda: self.start_practice('easy')).grid(row=1, column=0, padx=5)
        Button(diff_frame, text="Medium", font=("Arial", 14), command=lambda: self.start_practice('medium')).grid(row=1, column=1, padx=5)
        Button(diff_frame, text="Hard", font=("Arial", 14), command=lambda: self.start_practice('hard')).grid(row=1, column=2, padx=5)
        nav_frame = Frame(diff_frame, bg="#f5f5f5")
        nav_frame.grid(row=2, column=0, columnspan=3, pady=(20,0))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_mode_selection)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.practice_widgets.extend([back_btn, home_btn])
        self.back_btn = back_btn

    def start_practice(self, difficulty):
        self.difficulty = difficulty
        self.clear_practice_widgets()
        self.show_practice_ui()

    def show_practice_ui(self):
        self.practice_widgets = []
        # Generate random question based on difficulty
        if hasattr(self, 'difficulty'):
            difficulty = self.difficulty
        else:
            difficulty = 'easy'
        def random_mixed(difficulty):
            if difficulty == 'easy':
                whole = random.choice([0, 1])
                num = random.randint(1, 5)
                den = random.randint(1, 5)
            elif difficulty == 'medium':
                whole = random.randint(0, 2)
                num = random.randint(1, 10)
                den = random.randint(2, 10)
            else:
                whole = random.randint(0, 3)
                num = random.randint(1, 20)
                den = random.randint(2, 20)
            return whole, num, den
        # Generate two random fractions, possibly mixed
        w1, n1, d1 = random_mixed(difficulty)
        w2, n2, d2 = random_mixed(difficulty)
        op = random.choice(['*', '/'])
        def mixed_to_str(w, n, d):
            if w > 0:
                return f"{w} {n}/{d}"
            else:
                return f"{n}/{d}"
        def mixed_to_frac(w, n, d):
            return Fraction(w) + Fraction(n, d) if w >= 0 else Fraction(w) - Fraction(n, d)
        self.practice_frac1 = mixed_to_frac(w1, n1, d1)
        self.practice_frac2 = mixed_to_frac(w2, n2, d2)
        self.practice_op = op
        # Display question in a single line
        q_frame = Frame(self.master, bg="#f5f5f5")
        q_frame.grid(row=0, column=0, padx=30, pady=30)
        self.practice_widgets.append(q_frame)
        Label(q_frame, text=mixed_to_str(w1, n1, d1), font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").grid(row=0, column=0, padx=5)
        Label(q_frame, text=" × " if op == '*' else " ÷ ", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#2196F3").grid(row=0, column=1, padx=5)
        Label(q_frame, text=mixed_to_str(w2, n2, d2), font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").grid(row=0, column=2, padx=5)
        Label(q_frame, text=" = ", font=("Arial", 18, "bold"), bg="#f5f5f5").grid(row=0, column=3, padx=5)
        self.ans_var = StringVar()
        Entry(q_frame, width=14, textvariable=self.ans_var, justify='center', font=("Arial", 16)).grid(row=0, column=4, padx=5)
        # Submit button
        submit_btn = Button(self.master, text="Submit Answer", command=self.check_practice_answer, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10)
        submit_btn.grid(row=1, column=0, pady=(0,10))
        self.practice_widgets.append(submit_btn)
        # Change Problem button
        change_btn = Button(self.master, text="Change Problem", command=self.change_practice_problem, font=("Arial", 12), bg="#2196F3", fg="white")
        change_btn.grid(row=1, column=1, pady=(0,10), padx=(5,0))
        self.practice_widgets.append(change_btn)
        # Points label
        self.points_var = StringVar(value=f"Points: {self.points}")
        points_label = Label(self.master, textvariable=self.points_var, font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333")
        points_label.grid(row=2, column=0, pady=(0,10))
        self.practice_widgets.append(points_label)
        # Navigation buttons
        nav_frame = Frame(self.master, bg="#f5f5f5")
        nav_frame.grid(row=3, column=0, pady=(0,10))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_difficulty_selection)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.practice_widgets.extend([nav_frame, back_btn, home_btn])
        self.back_btn = back_btn

    def change_practice_problem(self):
        self.clear_practice_widgets()
        self.show_practice_ui()

    def exit_practice_mode(self):
        self.mode.set('main')
        self.clear_practice_widgets()
        self.show_mode_selection()

    def clear_all_widgets(self):
        for w in getattr(self, 'main_widgets', []):
            try:
                w.destroy()
            except:
                pass
        self.main_widgets = []
        if hasattr(self, 'frame') and self.frame:
            self.frame.grid_remove()
        for w in getattr(self, 'practice_widgets', []):
            try:
                w.destroy()
            except:
                pass
        self.practice_widgets = []
        for btn in ['toggle_btn', 'practice_btn', 'back_btn']:
            if hasattr(self, btn) and getattr(self, btn):
                try:
                    getattr(self, btn).destroy()
                except:
                    pass
                setattr(self, btn, None)

    def clear_main_widgets(self):
        self.frame.grid_remove()
        self.toggle_btn.grid_remove()
        self.practice_btn.grid_remove()

    def clear_practice_widgets(self):
        for w in self.practice_widgets:
            w.destroy()
        self.practice_widgets = []
        if self.back_btn:
            self.back_btn.destroy()
            self.back_btn = None
        self.frame.grid(row=0, column=0, padx=10, pady=10)

    def check_practice_answer(self):
        try:
            user_input = self.ans_var.get().strip()
            user_frac = Fraction(user_input)
            if self.practice_op == '*':
                correct = self.practice_frac1 * self.practice_frac2
            else:
                if self.practice_frac2 == 0:
                    raise ValueError("Cannot divide by zero.")
                correct = self.practice_frac1 / self.practice_frac2
            if user_frac == correct:
                self.points += 1
                messagebox.showinfo("Correct!", "Correct answer! +1 point.")
            else:
                self.points -= 1
                messagebox.showerror("Incorrect", f"Wrong answer. The correct answer is {correct.numerator}/{correct.denominator}. -1 point.")
            self.clear_practice_widgets()
            self.show_practice_ui()
        except Exception as e:
            messagebox.showerror("Invalid input", f"Please enter a valid answer as a fraction (e.g., 3/4 or 2).\n{e}")

if __name__ == "__main__":
    root = Tk()
    root.geometry("500x250")  # Set window size to be larger
    app = FractionHelperApp(root)
    root.mainloop()