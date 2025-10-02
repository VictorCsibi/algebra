from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
from fractions import Fraction
import random

# Color constants
BG_COLOR = "#f5f5f5"
PRIMARY_COLOR = "#2196F3"
SECONDARY_COLOR = "#FF9800"
SUCCESS_COLOR = "#4CAF50"
ERROR_COLOR = "#8b1515"
ALT_BG_COLOR = "#146b31"
DARK_TEXT_COLOR = "#333"
DISABLED_BG_COLOR = "#e0e0e0"

class FractionHelperApp:
    def __init__(self, master):
        self.master = master
        master.title("Fraction Helper")
        master.configure(bg=BG_COLOR)
        self.mode = StringVar(value='main')  # 'main', 'calc', or 'practice'
        self.points = 0
        self.practice_widgets = []
        self.main_widgets = []
        # Initialize calculator variables
        self.whole1_var = StringVar()
        self.num1_var = StringVar()
        self.den1_var = StringVar()
        self.whole2_var = StringVar()
        self.num2_var = StringVar()
        self.den2_var = StringVar()
        self.res_num_var = StringVar()
        self.res_den_var = StringVar()
        self.res_integer_var = StringVar()
        self.operation = StringVar(value='*')
        self.frame = None
        self.show_main_screen()

    def show_main_screen(self):
        self.clear_all_widgets()
        # Title at the top of the window
        title_label = Label(self.master, text="Fraction Helper", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        title_label.pack(pady=(20, 10))
        self.main_widgets.append(title_label)
        
        main_frame = Frame(self.master, bg=BG_COLOR)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.main_widgets.append(main_frame)
        
        Label(main_frame, text="Welcome to Fraction Helper!", font=("Arial", 18), bg=BG_COLOR, fg=DARK_TEXT_COLOR).pack(pady=(0, 30))
        start_btn = Button(main_frame, text="Start", font=("Arial", 18, "bold"), bg=SUCCESS_COLOR, fg="white", padx=30, pady=10, command=self.show_mode_selection)
        start_btn.pack(pady=(0, 10))
        self.main_widgets.append(start_btn)

    def show_mode_selection(self):
        self.clear_all_widgets()
        # Title at the top of the window
        title_label = Label(self.master, text="Mode Selection", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        title_label.pack(pady=(20, 10))
        self.main_widgets.append(title_label)
        
        mode_frame = Frame(self.master, bg=BG_COLOR)
        mode_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.main_widgets.append(mode_frame)
        
        Label(mode_frame, text="Choose your mode:", font=("Arial", 16), bg=BG_COLOR, fg=DARK_TEXT_COLOR).pack(pady=(0, 20))
        calc_btn = Button(mode_frame, text="Calculator", font=("Arial", 16), bg=PRIMARY_COLOR, fg="white", width=15, command=self.enter_calc_mode)
        calc_btn.pack(pady=10)
        practice_btn = Button(mode_frame, text="Practice Mode", font=("Arial", 16), bg=SECONDARY_COLOR, fg="white", width=15, command=self.enter_practice_mode)
        practice_btn.pack(pady=10)
        nav_frame = Frame(mode_frame, bg=BG_COLOR)
        nav_frame.pack(pady=(20,0))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_main_screen)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.main_widgets.extend([calc_btn, practice_btn, back_btn, home_btn])

    def enter_calc_mode(self):
        self.mode.set('calc')
        self.clear_all_widgets()
        
        # Title at the top of the window
        title_label = Label(self.master, text="Fraction Calculator", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        title_label.grid(row=0, column=0, pady=(20, 5), columnspan=2)
        self.main_widgets.append(title_label)
        
        # Instructions
        instructions_label = Label(self.master, text="Enter mixed fractions (whole number + numerator/denominator)", font=("Arial", 12), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        instructions_label.grid(row=1, column=0, pady=(0, 10), columnspan=2)
        self.main_widgets.append(instructions_label)
        
        # Create a bordered frame for the calculator
        calc_container = Frame(self.master, bg=BG_COLOR, relief='raised', bd=2)
        calc_container.grid(row=2, column=0, padx=30, pady=20, columnspan=2)
        self.main_widgets.append(calc_container)
        
        if not hasattr(self, 'frame') or self.frame is None:
            self.frame = Frame(calc_container, bg=BG_COLOR, padx=20, pady=20)
        else:
            self.frame = Frame(calc_container, bg=BG_COLOR, padx=20, pady=20)
        self.frame.pack()
        
        self.build_fraction_ui()
        
        # Calculate button
        calc_btn = Button(self.master, text="Calculate", command=self.calculate, font=("Arial", 14, "bold"), bg=SUCCESS_COLOR, fg="white", padx=20)
        calc_btn.grid(row=3, column=0, pady=(10,5))
        self.main_widgets.append(calc_btn)
        
        self.toggle_btn = Button(self.master, text="Switch to Divide", command=self.toggle_operation, font=("Arial", 12))
        self.toggle_btn.grid(row=4, column=0, pady=(0,5))
        self.practice_btn = Button(self.master, text="Practice Mode", command=self.enter_practice_mode, font=("Arial", 12))
        self.practice_btn.grid(row=5, column=0, pady=(0,5))
        nav_frame = Frame(self.master, bg=BG_COLOR)
        nav_frame.grid(row=6, column=0, pady=(10,5))
        back_btn = Button(nav_frame, text="Back", font=("Arial", 12), command=self.show_mode_selection)
        back_btn.pack(side='left', padx=5)
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        self.main_widgets.extend([self.toggle_btn, self.practice_btn, nav_frame, back_btn, home_btn])

    def build_fraction_ui(self):
        # Clear frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create boxes for each fraction
        # Fraction 1 box
        frac1_container = Frame(self.frame, bg=BG_COLOR)
        frac1_container.grid(row=0, column=0, padx=10, pady=10)
        
        frac1_frame = Frame(frac1_container, bg="white", relief='solid', bd=1, padx=10, pady=10)
        frac1_frame.pack()
        
        Label(frac1_frame, text="First Fraction", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0,5))
        Entry(frac1_frame, width=3, textvariable=self.whole1_var, justify='center', font=("Arial", 16)).grid(row=2, column=0, padx=5)
        Entry(frac1_frame, width=4, textvariable=self.num1_var, justify='center', font=("Arial", 16)).grid(row=1, column=1, padx=5)
        Label(frac1_frame, text="\u2014", font=("Arial", 18), bg="white").grid(row=2, column=1)
        Entry(frac1_frame, width=4, textvariable=self.den1_var, justify='center', font=("Arial", 16)).grid(row=3, column=1, padx=5)
        
        # Buttons for fraction 1
        btn_frame1 = Frame(frac1_container, bg=BG_COLOR)
        btn_frame1.pack(pady=(5,0))
        
        simplify_btn1 = Button(btn_frame1, text="⚡", font=("Arial", 12), width=2, command=lambda: self.simplify_fraction(1))
        simplify_btn1.pack(side='left', padx=1)
        self.create_tooltip(simplify_btn1, "Simplify fraction (6/4 → 3/2)")
        
        extract_btn1 = Button(btn_frame1, text="↗", font=("Arial", 12), width=2, command=lambda: self.extract_integer(1))
        extract_btn1.pack(side='left', padx=1)
        self.create_tooltip(extract_btn1, "Extract integer (3/2 → 1 1/2)")
        
        combine_btn1 = Button(btn_frame1, text="↙", font=("Arial", 12), width=2, command=lambda: self.combine_to_improper(1))
        combine_btn1.pack(side='left', padx=1)
        self.create_tooltip(combine_btn1, "Convert to improper (1 1/2 → 3/2)")
        
        # Operator (centered)
        op_symbol = "  ×  " if self.operation.get() == '*' else "  ÷  "
        self.operator_label = Label(self.frame, text=op_symbol, font=("Arial", 24, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR)
        self.operator_label.grid(row=0, column=1, padx=20)
        
        # Fraction 2 box
        frac2_container = Frame(self.frame, bg=BG_COLOR)
        frac2_container.grid(row=0, column=2, padx=10, pady=10)
        
        frac2_frame = Frame(frac2_container, bg="white", relief='solid', bd=1, padx=10, pady=10)
        frac2_frame.pack()
        
        Label(frac2_frame, text="Second Fraction", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0,5))
        Entry(frac2_frame, width=3, textvariable=self.whole2_var, justify='center', font=("Arial", 16)).grid(row=2, column=0, padx=5)
        Entry(frac2_frame, width=4, textvariable=self.num2_var, justify='center', font=("Arial", 16)).grid(row=1, column=1, padx=5)
        Label(frac2_frame, text="\u2014", font=("Arial", 18), bg="white").grid(row=2, column=1)
        Entry(frac2_frame, width=4, textvariable=self.den2_var, justify='center', font=("Arial", 16)).grid(row=3, column=1, padx=5)
        
        # Buttons for fraction 2
        btn_frame2 = Frame(frac2_container, bg=BG_COLOR)
        btn_frame2.pack(pady=(5,0))
        
        simplify_btn2 = Button(btn_frame2, text="⚡", font=("Arial", 12), width=2, command=lambda: self.simplify_fraction(2))
        simplify_btn2.pack(side='left', padx=1)
        self.create_tooltip(simplify_btn2, "Simplify fraction (6/4 → 3/2)")
        
        extract_btn2 = Button(btn_frame2, text="↗", font=("Arial", 12), width=2, command=lambda: self.extract_integer(2))
        extract_btn2.pack(side='left', padx=1)
        self.create_tooltip(extract_btn2, "Extract integer (3/2 → 1 1/2)")
        
        combine_btn2 = Button(btn_frame2, text="↙", font=("Arial", 12), width=2, command=lambda: self.combine_to_improper(2))
        combine_btn2.pack(side='left', padx=1)
        self.create_tooltip(combine_btn2, "Convert to improper (1 1/2 → 3/2)")
        
        # Equals sign (centered)
        Label(self.frame, text="  =  ", font=("Arial", 24, "bold"), bg=BG_COLOR).grid(row=0, column=3, padx=20)
        
        # Result integer box (readonly)
        result_int_frame = Frame(self.frame, bg=DISABLED_BG_COLOR, relief='solid', bd=1, padx=10, pady=10)
        result_int_frame.grid(row=0, column=4, padx=5, pady=10)
        
        Label(result_int_frame, text="Integer Part", font=("Arial", 12, "bold"), bg=DISABLED_BG_COLOR).grid(row=0, column=0, pady=(0,5))
        Entry(result_int_frame, width=6, textvariable=self.res_integer_var, justify='center', state='readonly', font=("Arial", 16), disabledbackground=DISABLED_BG_COLOR).grid(row=1, column=0, padx=5)
        
        # Result fraction box (readonly)
        result_frame = Frame(self.frame, bg=DISABLED_BG_COLOR, relief='solid', bd=1, padx=10, pady=10)
        result_frame.grid(row=0, column=5, padx=5, pady=10)
        
        Label(result_frame, text="Fraction Part", font=("Arial", 12, "bold"), bg=DISABLED_BG_COLOR).grid(row=0, column=0, columnspan=2, pady=(0,5))
        Entry(result_frame, width=4, textvariable=self.res_num_var, justify='center', state='readonly', font=("Arial", 16), disabledbackground=DISABLED_BG_COLOR).grid(row=1, column=0, padx=5)
        Label(result_frame, text="\u2014", font=("Arial", 18), bg=DISABLED_BG_COLOR).grid(row=2, column=0)
        Entry(result_frame, width=4, textvariable=self.res_den_var, justify='center', state='readonly', font=("Arial", 16), disabledbackground=DISABLED_BG_COLOR).grid(row=3, column=0, padx=5)

    def toggle_operation(self):
        if self.operation.get() == '*':
            self.operation.set('/')
            self.toggle_btn.config(text="Switch to Multiply")
        else:
            self.operation.set('*')
            self.toggle_btn.config(text="Switch to Divide")
        self.clear_result()
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
    
    def clear_result(self):
        """Clear all result fields"""
        self.res_integer_var.set("")
        self.res_num_var.set("")
        self.res_den_var.set("")
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = Label(self.master, text=text, font=("Arial", 10), 
                          bg="lightyellow", relief="solid", bd=1, padx=5, pady=2)
            tooltip.place(x=event.x_root - self.master.winfo_rootx() + 10, 
                         y=event.y_root - self.master.winfo_rooty() - 30)
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def simplify_fraction(self, fraction_num):
        """Simplify the specified fraction"""
        try:
            if fraction_num == 1:
                whole_var, num_var, den_var = self.whole1_var, self.num1_var, self.den1_var
            else:
                whole_var, num_var, den_var = self.whole2_var, self.num2_var, self.den2_var
            
            # Get current fraction
            frac = self.get_fraction(whole_var, num_var, den_var)
            
            # Update with simplified improper fraction (no whole part)
            whole_var.set("0")
            num_var.set(str(frac.numerator))
            den_var.set(str(frac.denominator))
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot simplify: {e}")
    
    def extract_integer(self, fraction_num):
        """Extract integer part from improper fraction"""
        try:
            if fraction_num == 1:
                whole_var, num_var, den_var = self.whole1_var, self.num1_var, self.den1_var
            else:
                whole_var, num_var, den_var = self.whole2_var, self.num2_var, self.den2_var
            
            # Get current values
            num = int(num_var.get()) if num_var.get() else 0
            den = int(den_var.get()) if den_var.get() else 1
            current_whole = int(whole_var.get()) if whole_var.get() else 0
            
            if den == 0:
                raise ValueError("Denominator cannot be zero")
            
            # Extract integer from the fraction part
            if abs(num) >= den:
                extracted_integer = num // den
                remainder = num % den
                
                # Update fields
                whole_var.set(str(current_whole + extracted_integer))
                num_var.set(str(remainder))
                den_var.set(str(den))
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot extract integer: {e}")
    
    def combine_to_improper(self, fraction_num):
        """Convert mixed number to improper fraction"""
        try:
            if fraction_num == 1:
                whole_var, num_var, den_var = self.whole1_var, self.num1_var, self.den1_var
            else:
                whole_var, num_var, den_var = self.whole2_var, self.num2_var, self.den2_var
            
            # Get current values
            whole = int(whole_var.get()) if whole_var.get() else 0
            num = int(num_var.get()) if num_var.get() else 0
            den = int(den_var.get()) if den_var.get() else 1
            
            if den == 0:
                raise ValueError("Denominator cannot be zero")
            
            # Convert to improper fraction
            if whole != 0:
                improper_num = whole * den + num
                
                # Update fields
                whole_var.set("0")
                num_var.set(str(improper_num))
                den_var.set(str(den))
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot convert to improper: {e}")

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
            
            # Simplify and convert to mixed number format
            if result.denominator == 1:
                # Pure integer result
                self.res_integer_var.set(str(result.numerator))
                self.res_num_var.set("0")
                self.res_den_var.set("1")
            elif abs(result.numerator) >= result.denominator:
                # Mixed number result
                integer_part = result.numerator // result.denominator
                remainder = abs(result.numerator) % result.denominator
                
                if remainder == 0:
                    # Actually a whole number
                    self.res_integer_var.set(str(integer_part))
                    self.res_num_var.set("0")
                    self.res_den_var.set("1")
                else:
                    # True mixed number
                    self.res_integer_var.set(str(integer_part))
                    self.res_num_var.set(str(remainder))
                    self.res_den_var.set(str(result.denominator))
            else:
                # Proper fraction (numerator < denominator)
                self.res_integer_var.set("0")
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
        
        # Title at the top of the window
        title_label = Label(self.master, text="Practice Mode - Difficulty Selection", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        title_label.pack(pady=(20, 10))
        self.practice_widgets = [title_label]
        
        diff_frame = Frame(self.master, bg=BG_COLOR)
        diff_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.practice_widgets.append(diff_frame)
        
        Label(diff_frame, text="Select Difficulty Level:", font=("Arial", 16), bg=BG_COLOR).grid(row=0, column=0, columnspan=3, pady=(0,20))
        Button(diff_frame, text="Easy", font=("Arial", 14), bg=SUCCESS_COLOR, fg="white", width=10, command=lambda: self.start_practice('easy')).grid(row=1, column=0, padx=10)
        Button(diff_frame, text="Medium", font=("Arial", 14), bg=SECONDARY_COLOR, fg="white", width=10, command=lambda: self.start_practice('medium')).grid(row=1, column=1, padx=10)
        Button(diff_frame, text="Hard", font=("Arial", 14), bg=ERROR_COLOR, fg="white", width=10, command=lambda: self.start_practice('hard')).grid(row=1, column=2, padx=10)
        nav_frame = Frame(diff_frame, bg=BG_COLOR)
        nav_frame.grid(row=2, column=0, columnspan=3, pady=(30,0))
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
        
        # Title at the top of the window
        difficulty_name = self.difficulty.capitalize() if hasattr(self, 'difficulty') else 'Easy'
        title_label = Label(self.master, text=f"Practice Mode - {difficulty_name} Level", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        title_label.pack(pady=(20, 10))
        self.practice_widgets.append(title_label)
        
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
        
        # Create a bordered frame for the question
        question_container = Frame(self.master, bg=BG_COLOR, relief='raised', bd=2, padx=20, pady=15)
        question_container.pack(padx=30, pady=20)
        self.practice_widgets.append(question_container)
        
        # Title for the question
        Label(question_container, text="Solve:", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR).pack(pady=(0, 10))
        
        # Display question using fraction boxes like calculator mode
        q_frame = Frame(question_container, bg=BG_COLOR)
        q_frame.pack()
        
        # First fraction box
        frac1_frame = Frame(q_frame, bg="lightblue", relief='solid', bd=1, padx=8, pady=8)
        frac1_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Display first fraction in box format
        if w1 > 0:
            Label(frac1_frame, text=str(w1), font=("Arial", 14, "bold"), bg="lightblue").grid(row=1, column=0, padx=3)
        Label(frac1_frame, text=str(n1), font=("Arial", 14, "bold"), bg="lightblue").grid(row=0, column=1, padx=3)
        Label(frac1_frame, text="\u2014", font=("Arial", 16), bg="lightblue").grid(row=1, column=1)
        Label(frac1_frame, text=str(d1), font=("Arial", 14, "bold"), bg="lightblue").grid(row=2, column=1, padx=3)
        
        # Operator
        op_symbol = "  ×  " if op == '*' else "  ÷  "
        Label(q_frame, text=op_symbol, font=("Arial", 20, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR).grid(row=0, column=1, padx=15)
        
        # Second fraction box
        frac2_frame = Frame(q_frame, bg="lightblue", relief='solid', bd=1, padx=8, pady=8)
        frac2_frame.grid(row=0, column=2, padx=5, pady=5)
        
        # Display second fraction in box format
        if w2 > 0:
            Label(frac2_frame, text=str(w2), font=("Arial", 14, "bold"), bg="lightblue").grid(row=1, column=0, padx=3)
        Label(frac2_frame, text=str(n2), font=("Arial", 14, "bold"), bg="lightblue").grid(row=0, column=1, padx=3)
        Label(frac2_frame, text="\u2014", font=("Arial", 16), bg="lightblue").grid(row=1, column=1)
        Label(frac2_frame, text=str(d2), font=("Arial", 14, "bold"), bg="lightblue").grid(row=2, column=1, padx=3)
        
        # Equals sign
        Label(q_frame, text="  =  ", font=("Arial", 20, "bold"), bg=BG_COLOR).grid(row=0, column=3, padx=15)
        
        # Answer input box
        answer_frame = Frame(q_frame, bg="white", relief='solid', bd=1, padx=10, pady=10)
        answer_frame.grid(row=0, column=4, padx=5, pady=5)
        
        Label(answer_frame, text="Your Answer", font=("Arial", 12, "bold"), bg="white").pack(pady=(0,5))
        self.ans_var = StringVar()
        Entry(answer_frame, width=12, textvariable=self.ans_var, justify='center', font=("Arial", 14)).pack()
        
        # Points label
        self.points_var = StringVar(value=f"Points: {self.points}")
        points_label = Label(self.master, textvariable=self.points_var, font=("Arial", 16, "bold"), bg=BG_COLOR, fg=DARK_TEXT_COLOR)
        points_label.pack(pady=(10,0))
        self.practice_widgets.append(points_label)
        
        # Buttons
        button_frame = Frame(self.master, bg=BG_COLOR)
        button_frame.pack(pady=(20,10))
        self.practice_widgets.append(button_frame)
        
        submit_btn = Button(button_frame, text="Submit Answer", command=self.check_practice_answer, font=("Arial", 14, "bold"), bg=SUCCESS_COLOR, fg="white", padx=20)
        submit_btn.pack(side='left', padx=10)
        
        change_btn = Button(button_frame, text="New Problem", command=self.change_practice_problem, font=("Arial", 12), bg=PRIMARY_COLOR, fg="white", padx=15)
        change_btn.pack(side='left', padx=10)
        
        # Navigation buttons
        nav_frame = Frame(self.master, bg=BG_COLOR)
        nav_frame.pack(pady=(10,20))
        self.practice_widgets.append(nav_frame)
        
        back_btn = Button(nav_frame, text="Back to Difficulty", font=("Arial", 12), bg=SECONDARY_COLOR, fg="white", command=self.show_difficulty_selection)
        back_btn.pack(side='left', padx=5)
        
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), command=self.show_main_screen)
        home_btn.pack(side='left', padx=5)
        
        self.practice_widgets.extend([submit_btn, change_btn, back_btn, home_btn])
        self.back_btn = back_btn

    def change_practice_problem(self):
        self.clear_practice_widgets()
        self.show_practice_ui()

    def exit_practice_mode(self):
        self.mode.set('main')
        self.clear_practice_widgets()
        self.show_mode_selection()

    def clear_all_widgets(self):
        # Clear all widgets from the master window
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Reset widget lists
        self.main_widgets = []
        self.practice_widgets = []
        
        # Reset references
        for attr in ['frame', 'toggle_btn', 'practice_btn', 'back_btn']:
            if hasattr(self, attr):
                setattr(self, attr, None)

    def clear_main_widgets(self):
        self.frame.grid_remove()
        self.toggle_btn.grid_remove()
        self.practice_btn.grid_remove()

    def clear_practice_widgets(self):
        for w in self.practice_widgets:
            try:
                w.destroy()
            except:
                pass
        self.practice_widgets = []
        if hasattr(self, 'back_btn') and self.back_btn:
            try:
                self.back_btn.destroy()
            except:
                pass
            self.back_btn = None

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
            
            # Format the correct answer nicely
            if correct.denominator == 1:
                correct_str = str(correct.numerator)
            elif abs(correct.numerator) >= correct.denominator:
                # Mixed number
                integer_part = correct.numerator // correct.denominator
                remainder = abs(correct.numerator) % correct.denominator
                if remainder == 0:
                    correct_str = str(integer_part)
                else:
                    correct_str = f"{integer_part} {remainder}/{correct.denominator}"
            else:
                correct_str = f"{correct.numerator}/{correct.denominator}"
            
            if user_frac == correct:
                self.points += 1
                messagebox.showinfo("Correct!", "Correct answer! +1 point.")
            else:
                self.points -= 1
                messagebox.showerror("Incorrect", f"Wrong answer. The correct answer is {correct_str}. -1 point.")
            
            # Generate new problem
            self.clear_practice_widgets()
            self.show_practice_ui()
        except Exception as e:
            messagebox.showerror("Invalid input", f"Please enter a valid answer as a fraction (e.g., 3/4 or 2).\n{e}")

if __name__ == "__main__":
    root = Tk()
    root.geometry("900x600")  # Set window size to accommodate fraction calculator layout with separate result boxes
    app = FractionHelperApp(root)
    root.mainloop()