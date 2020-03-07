import tkinter as tk
from decimal import Decimal

WIDTH_P = 5

class CalcMainWindow(tk.Frame):
    def __init__(self, app, **kwargs):
        super(CalcMainWindow, self).__init__(app, **kwargs)
        self.pack()
        self.content = tk.StringVar() # значение поля вычислений
        self.content.set('0')
        self.temp_content = tk.StringVar()
        self.operand = tk.StringVar()
        
        content_field = tk.Label(self, textvariable=self.content, relief=tk.GROOVE, anchor=tk.E, width=WIDTH_P*4)
        row_id = 0
        content_field.grid(row=row_id, columnspan=4)
        row_id += 1
        
        keyboard = [
            ['C','CE','/','*'],
            [7, 8, 9, '-'],
            [6, 5, 4, '+'],
            [3, 2, 1, '='],
            [0]
        ]
        buttons = []
        for ri, row in enumerate(keyboard):
            rlen = len(row)
            for ci, col in enumerate(row):
                ref = int(4 / rlen)
                _btn = tk.Button(self, text=str(col), anchor=tk.CENTER, width=ref*5)
                _btn.grid(row=row_id + ri, column=ci, columnspan=ref)
                _btn.config(command=lambda b=_btn: action(b))
                buttons.append(_btn)

        def action(btn):
            action = btn['text']
            content = self.content.get()
            print(action)
            if action.isdigit():
                if content == '0' or content[-1:] == '!':
                    if action == '0':
                        return
                    else:
                        content = action
                else:
                    content += action
            else:
                if '-' not in content and '*' not in content and '+' not in content and '/' not in content and action not in 'CE':
                    content += action
                elif action == 'C':
                    content = '0'
                elif action == 'CE':
                    print(content)
                    if len(content) == 1:
                        content = '0'
                    else:
                        content = content[:-1]
                else:
                    try:
                        if content[-1:] in '/*-+':
                            content = str(eval(content + content[0:len(content) - 1]))
                        else:
                            content = str(eval(content))
                        if action != '=':
                            content += action
                    except ZeroDivisionError:
                        content = 'Division by zero!'
                  
            self.content.set(content)

        app.bind("c", lambda *ignore: buttons[0].invoke())
        app.bind("e", lambda *ignore: buttons[1].invoke())
        app.bind("/", lambda *ignore: buttons[2].invoke())
        app.bind("*", lambda *ignore: buttons[3].invoke())
        app.bind("7", lambda *ignore: buttons[4].invoke())
        app.bind("8", lambda *ignore: buttons[5].invoke())
        app.bind("9", lambda *ignore: buttons[6].invoke())
        app.bind("-", lambda *ignore: buttons[7].invoke())
        app.bind("6", lambda *ignore: buttons[8].invoke())
        app.bind("5", lambda *ignore: buttons[9].invoke())
        app.bind("4", lambda *ignore: buttons[10].invoke())
        app.bind("+", lambda *ignore: buttons[11].invoke())
        app.bind("3", lambda *ignore: buttons[12].invoke())
        app.bind("2", lambda *ignore: buttons[13].invoke())
        app.bind("1", lambda *ignore: buttons[14].invoke())
        app.bind("=", lambda *ignore: buttons[15].invoke())
        app.bind("0", lambda *ignore: buttons[16].invoke())
        app.bind("<BackSpace>", lambda *ignore: buttons[1].invoke())
        app.bind("<Return>", lambda *ignore: buttons[15].invoke())
        

if __name__ == '__main__':
    import os, sys

    application = tk.Tk()
    path = os.path.join(os.path.dirname(__file__), "images/")
    # if sys.platform.startswith("win"):
    #     icon = path + "interest.ico"
    # else:
    #     icon = "@" + path + "interest.xbm"
    # application.iconbitmap(icon)
    application.title("Calculator")
    window = CalcMainWindow(application)
    application.protocol("WM_DELETE_WINDOW", window.quit)
    application.mainloop()
