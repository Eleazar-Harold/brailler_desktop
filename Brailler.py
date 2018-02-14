from tkinter import Tk, Frame, Label, Text, Button, Menu, END

from src import TextToBraille, BrailleToText


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Menu
        MainMenu(self)

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (TextBraillePage, BrailleTextPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TextBraillePage)

    def show_frame(self, context):
        if context == TextBraillePage:
            self.title("Text to Braille")
        elif context == BrailleTextPage:
            self.title("Braille to Text")
        frame = self.frames[context]
        frame.tkraise()


class TextBraillePage(Frame):
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.frame = Frame.__init__(self, self.parent)

        self.label = Label(self, text='Enter text: ')
        self.label.pack(padx=2, pady=10)
        #
        self.user_input = Text(self, background='white', width=80, height=10)
        self.user_input.pack(padx=10, pady=10, anchor='center')

        self.label_2 = Label(self, text='Braille')
        self.label_2.pack(padx=2, pady=10)

        self.converted_input = Text(self, background='lightgray', width=80, height=10)
        self.converted_input.pack(padx=10, pady=10, anchor='center')
        #
        self.cur_frame = Frame(self).pack(padx=15, pady=(0, 15), anchor='e')
        #
        self.button = Button(self, text='OK', default='active', command=self.click_ok)
        self.button.pack(side='right', padx=15, pady=15)
        self.button2 = Button(self, text='Cancel', command=self.click_cancel)
        self.button2.pack(side='right', padx=15, pady=15)
        self.button3 = Button(self, text='Braille-to-text', command=lambda: controller.show_frame(BrailleTextPage))
        self.button3.pack(side='left', padx=15, pady=15)

    def click_ok(self):
        self.converted_input.insert(END, TextToBraille.t2b_translate(str(self.user_input.get(1.0, END))))
        # self.converted_input.config(state=DISABLED)

    def click_cancel(self):
        self.user_input.delete('1.0', END)
        # self.converted_input.config(state=NORMAL)
        self.converted_input.delete('1.0', END)
        # self.converted_input.config(state=DISABLED)


class BrailleTextPage(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.frame = Frame.__init__(self, self.parent)

        self.label = Label(self, text='Enter braille: ')
        self.label.pack(padx=2, pady=10)
        #
        self.user_input = Text(self, background='white', width=80, height=10)
        self.user_input.pack(padx=10, pady=10, anchor='center')

        self.label_2 = Label(self, text='Text')
        self.label_2.pack(padx=2, pady=10)

        self.converted_input = Text(self, background='lightgray', width=80, height=10)
        self.converted_input.pack(padx=10, pady=10, anchor='center')
        #
        self.cur_frame = Frame(self).pack(padx=15, pady=(0, 15), anchor='e')
        #
        self.button = Button(self, text='OK', default='active', command=self.click_ok)
        self.button.pack(side='right', padx=15, pady=15)
        self.button2 = Button(self, text='Cancel', command=self.click_cancel)
        self.button2.pack(side='right', padx=15, pady=15)
        self.button3 = Button(self, text='Text-to-braille', command=lambda: controller.show_frame(TextBraillePage))
        self.button3.pack(side='left', padx=15, pady=15)

    def click_ok(self):
        self.converted_input.insert(END, BrailleToText.translate(str(self.user_input.get(1.0, END))))
        # self.converted_input.config(state=DISABLED)

    def click_cancel(self):
        self.user_input.delete('1.0', END)
        # self.converted_input.config(state=NORMAL)
        self.converted_input.delete('1.0', END)
        # self.converted_input.config(state=DISABLED)


class MainMenu:
    def __init__(self, master):
        self.master = master
        self.menu_bar = Menu(self.master)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.menu_bar)

