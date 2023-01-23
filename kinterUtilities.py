import tkinter as tk


class KinterUtilities:

    # data input - array of data n-ples
    # output - reference to table
    def __init__(self, parent):
        self.parent=parent

    def table(self, rows, columns, data):
        for i in range(rows):
            for j in range(columns):
                self.e = tk.Entry(self.parent, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, data[i][j])
        self.e.pack()
        return self.e
