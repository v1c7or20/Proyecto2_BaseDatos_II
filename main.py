from inverted_index import *
import tkinter as tk
import tkinter.font as tkFont


class App:
    texts = []
    index = InvertedIndex('index.txt', ['data_mid.json'])
    GMessage_750 = None
    GListBox_947 = None

    def __init__(self, root):
        root.title("Aplicacion Base Datos II")
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_638 = tk.Label(root)
        GLabel_638["anchor"] = "center"
        ft = tkFont.Font(family='Times', size=12)
        GLabel_638["font"] = ft
        GLabel_638["fg"] = "#333333"
        GLabel_638["justify"] = "center"
        GLabel_638["text"] = "Recuperacion de textos"
        GLabel_638["relief"] = "flat"
        GLabel_638.place(x=230, y=10, width=166, height=39)

        GLabel_567 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_567["font"] = ft
        GLabel_567["fg"] = "#333333"
        GLabel_567["justify"] = "center"
        GLabel_567["text"] = "Texto Input"
        GLabel_567.place(x=30, y=60, width=70, height=25)

        self.GMessage_750 = tk.Text(root)
        ft = tkFont.Font(family='Times', size=10)
        self.GMessage_750["font"] = ft
        self.GMessage_750["fg"] = "#333333"
        self.GMessage_750.place(x=180, y=60, width=170, height=25)

        GButton_379 = tk.Button(root)
        GButton_379["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_379["font"] = ft
        GButton_379["fg"] = "#000000"
        GButton_379["justify"] = "center"
        GButton_379["text"] = "Recuperar"
        GButton_379.place(x=480, y=60, width=70, height=25)
        GButton_379["command"] = self.GButton_379_command

        GLabel_918 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_918["font"] = ft
        GLabel_918["fg"] = "#333333"
        GLabel_918["justify"] = "center"
        GLabel_918["text"] = "Textos Recuperados"
        GLabel_918.place(x=20, y=110, width=134, height=30)

        variable = tk.StringVar(root)
        variable.set("Select")  # default value
        self.GListBox_947 = tk.OptionMenu(root, variable, "Select")
        ft = tkFont.Font(family='Times', size=10)
        self.GListBox_947["font"] = ft
        self.GListBox_947["fg"] = "#333333"
        self.GListBox_947["justify"] = "center"
        self.GListBox_947.place(x=190, y=110, width=180, height=25)

        GLineEdit_602 = tk.Entry(root)
        GLineEdit_602["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_602["font"] = ft
        GLineEdit_602["fg"] = "#333333"
        GLineEdit_602["justify"] = "center"
        GLineEdit_602["text"] = "Entry"
        GLineEdit_602.place(x=490, y=240, width=70, height=25)

    def GButton_379_command(self):
        text_to = self.GMessage_750.get('1.0', 'end')
        data = self.index.retrieval(text_to[:-1], 4)
        var = tk.StringVar(root)
        var.set("")
        index_json = []
        self.GListBox_947['menu'].delete(0, 'end')
        for value in data:
            index_json.append(value[0])
        jsons = self.index.get_json_by_ids(index_json)
        choices = []
        for value in jsons:
            choices.append(str(value[0]) + " : " + value[1])
        for choice in choices:
            self.GListBox_947['menu'].add_command(label=choice, command=tk._setit(var, choice))
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# completed
