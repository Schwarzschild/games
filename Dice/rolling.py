from tkinter import Tk, Button
from rolling_dice import make_dice

tk = Tk()
tk.title('Roll the Dice')

roll_em = make_dice(tk, fills=['red', 'blue', 'green', 'purple', 'orange'])
button = Button(tk, text='Roll', command=roll_em)
button.pack()
tk.mainloop()
