import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter.filedialog import askopenfile, asksaveasfilename

from src.analyzer.analyzer import Analyzer


# gui
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main variables
        self.title('COMPILADOR PÁGINA WEB')
        self.rowconfigure(0, minsize=700, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)
        self.text_area = tk.Text(self, wrap=tk.WORD)
        # control files
        self.file = None
        self.open_file = None
        # create components
        self._create_components()
        # tokens
        self.list_tokens = []

    def _create_components(self):
        btns = tk.Frame(self, relief=tk.RAISED, bd=4)
        # FIRST BUTTONS
        tk.Button(btns, text='Nuevo', command=self.new_file).grid(row=0, column=0, sticky='WE', padx=5, pady=5,
                                                                  ipadx=10, ipady=5)
        tk.Button(btns, text='Abrir', command=self.found_file).grid(row=1, column=0, sticky='WE', padx=5, pady=5,
                                                                    ipadx=10, ipady=5)

        tk.Button(btns, text='Guardar', command=self.save_file).grid(row=2, column=0, sticky='WE', padx=5, pady=5,
                                                                     ipadx=10, ipady=5)

        tk.Button(btns, text='Guardar Como', command=self.save_as_file).grid(row=3, column=0, sticky='WE', padx=5,
                                                                             pady=5, ipadx=10, ipady=5)

        tk.Button(btns, text='Analizar', command=self.analyze).grid(row=4, column=0, sticky='WE', padx=5,
                                                                    pady=5, ipadx=10, ipady=5)

        tk.Button(btns, text='Ver Tokens', command=self.see_tokens).grid(row=5, column=0, sticky='WE', padx=5,
                                                                         pady=5, ipadx=10, ipady=5)
        # EXIT
        tk.Button(btns, text='Salir', command=lambda: self.quit()).grid(row=6, column=0, sticky='WE', padx=5,
                                                                        pady=5, ipadx=10, ipady=5)
        # SHOW
        btns.grid(row=0, column=0, sticky='NS')
        self.text_area.grid(row=0, column=1, sticky='NEWS')

    # Functions
    def analyze(self):
        compiler = Analyzer()
        compiler.compile(self.text_area.get(1.0, tk.END))
        self.list_tokens = compiler.token_list


    def see_tokens(self):
        list_window = tk.Toplevel(self)
        list_window.geometry('660x300+200+200')
        list_window.title('Listado de tokens')
        self.withdraw()
        # Table
        columns = ('No.', 'Token', 'Lexema')
        tree = ttk.Treeview(list_window, columns=columns, show='headings')
        # Define headings
        tree.heading('No.', text='Número')
        tree.heading('Token', text='Token')
        tree.heading('Lexema', text='Lexema')
        # Contact the values
        courses = []
        for i in range(len(self.list_tokens)):
            courses.append((
                f'{i+1}',
                f'{self.list_tokens[i].token}',
                f'{self.list_tokens[i].lexema}'
            ))
        # add data to the treeview
        for c in courses:
            tree.insert('', tk.END, values=c)

        tree.grid(row=0, column=0, sticky='nsew', padx=23, pady=10, ipadx=5, ipady=5)

        # button
        def back():
            self.deiconify()
            list_window.destroy()

        btn_back = tk.Button(list_window, text='Regresar', command=back, height=2, width=15)
        btn_back.grid(row=10)

    # Buttons Functions
    def new_file(self):
        new_content = self.text_area.get(1.0, tk.END)
        if new_content != "" and new_content != "\n":
            messagebox.askyesno(message="¿Desea guardar los cambios?", title="AVISO")
            if True:
                new_content = self.text_area.get(1.0, tk.END)
                new_file = filedialog.asksaveasfile(title='Guardar archivo...', defaultextension='.txt', filetypes=(('txt files', '*.gpw'),))
                if self.text_area != None:
                    new_file.write(f"{new_content}")
                    new_file.close()

                    self.text_area.delete(1.0, tk.END)

    def found_file(self):
        # Open the file window
        self.open_file = askopenfile(mode='r+')
        self.text_area.delete(1.0, tk.END)  # remove any line
        # Verified if ins´t a file already opened
        if not self.open_file:
            return
        # Read the selected file
        with open(self.open_file.name, 'r+', encoding="utf-8") as self.file:
            text = self.file.read()  # read content
            self.text_area.insert(1.0, text)  # insert the text into the text area
            self.title(f'* Compilador - {self.file.name}')

    def save_file(self):
        # Verified if a file was already opened
        if self.open_file:
            with open(self.open_file.name, 'w') as self.file:
                text = self.text_area.get(1.0, tk.END)  # read the content
                self.file.write(text)  # write all the text in the textarea
                self.title(f'Compilador - {self.file.name}')  # modified the title

    def save_as_file(self):
        # save file
        self.file = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        # if the file isn't open
        if not self.file:
            return
        with open(self.file, 'w') as file:
            text = self.text_area.get(1.0, tk.END)  # get the content
            file.write(text)  # write the content in the file
            self.title(f'Compilador - {file.name}')
            self.open_file = file  # Indicate that the file was already open


if __name__ == '__main__':
    compilation = GUI()
    compilation.mainloop()
