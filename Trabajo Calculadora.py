import tkinter as tk
from tkinter import messagebox
import re
from fractions import Fraction

# Clase para manejar la logica 
class Logica:
    def __init__(self):
        pass

    def evaluate(self, expression):
        # Reemplazar el operador de porcentaje 
        expression = expression.replace("%", "/100")

        # Evaluar la expresion de forma segura
        result = eval(expression, {"__builtins__": None}, {"Fraction": Fraction, "float": float})

        # Convertir fracciones a decimales 
        if isinstance(result, Fraction):
            return float(result)
        else:
            return result

# Clase para manejar el historial 
class Historial:
    def __init__(self):
        self.history = []

    def add_entry(self, entry):
        self.history.append(entry)

    def get_history(self):
        return "\n".join(self.history)

    def clear_history(self):
        self.history.clear()

# Clase para la interfaz grafica 
class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora 2.0")
        self.geometry("400x500")
        self.config(bg="sky blue")

        self.logic = Logica() 
        self.history = Historial()  

        # Pantalla para mostrar ecuaciones y resultados
        self.display = tk.Entry(self, font=("Boolean", 24), borderwidth=2, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

       
        self.create_buttons()
        # Asignar eventos de teclado
        self.bind("<Return>", lambda event: self.calculate())
        self.bind("<BackSpace>", lambda event: self.backspace())
        self.bind("<KeyPress>", self.on_keypress)

        # Configuracion de filas y columnas 
        for i in range(6):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i % 4, weight=1)

    def create_buttons(self):
        # Botones para las operaciones basicas
        buttons = [
            '7', '8', '9', '/',  
            '4', '5', '6', '*',  
            '1', '2', '3', '-',  
            '0', '.', '=', '+',  
            'CE', '⌫', '%', 'Historial' 
        ]

        # Crear botones y asignar acciones
        for i, button in enumerate(buttons):
            if button == 'CE':
                command = self.clear_display
            elif button == '⌫':
                command = self.backspace
            elif button == '=':
                command = self.calculate
            elif button == 'Historial':
                command = self.show_history
            else:
                command = lambda b=button: self.append_to_expression(b)

            tk.Button(self, text=button, font=("Arial", 18), command=command).grid(
                row=(i // 4) + 1, column=(i % 4), sticky="nsew", padx=10, pady=10
            )

    def append_to_expression(self, char):
        # Agregar un caracter a la ecuacion
        self.display.insert(tk.END, char)

    def clear_display(self):
        # Limpiar todo el campo de texto
        self.display.delete(0, tk.END)

    def backspace(self):
        # Borrar el ultimo caracter
        current_text = self.display.get()
        if current_text:
            self.display.delete(len(current_text) - 1, tk.END)

    def calculate(self):
        # Obtener la expresion y validarla
        expression = self.display.get()

        # Validar para caracteres 
        if not re.match(r'^[0-9+\-*/%.]+$', expression):
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            return

        try:
            # Evaluar la expresion y obtener el resultado
            result = self.logic.evaluate(expression)

            # Guardar la ecuacion y resultado en el historial
            self.history.add_entry(f"{expression} = {result}")

            # Mostrar el resultado
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

    def show_history(self):
        # Mostrar el historial en un cuadro de dialogo
        history_str = self.history.get_history()
        messagebox.showinfo("Historial", history_str)

    def on_keypress(self, event):
        # Validar caracteres permitidos
        char = event.char
        if not char.isdigit() and char not in {'.', '/', '*', '-', '+', '%'}:
            messagebox.showwarning("Entrada inválida", "Solo se permiten números y operadores.")

# Iniciar la calculadora
if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()