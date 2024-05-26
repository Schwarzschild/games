from tkinter import Tk, Button
from dice.rolling_dice import make_dice


tk = Tk()
tk.title('Rolling Dice')


def red(*args):
    die = dice[0]
    print('red', die.n)
    die.set_legend("HOLD")


def blue(*args):
    print('blue', dice[1].n)


def green(*args):
    print('green', dice[2].n)


def purple(*args):
    print('purple', dice[3].n)


def orange(*args):
    print('orange', dice[4].n)


callbacks = [red, blue, green, purple, orange]
fills = [c.__name__ for c in callbacks]

dice_canvas, dice, roll_em = (
    make_dice(tk, fills=fills, callbacks=callbacks))
dice_canvas.pack()

button = Button(tk, text='Roll', command=roll_em)
button.pack(side='left')
button2 = Button(tk, text='Exit', command=tk.destroy)
button2.pack(side='left')
tk.mainloop()
