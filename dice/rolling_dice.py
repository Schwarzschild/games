"""
Create a Die class that can be used to draw a die on a canvas and roll it.

Future improvements:
Make size and margin settable and add as parameters to make_dice.
"""

from tkinter import *
from random import randint


# size of one die
size = 40
# distance from the canvas top edge to the die
margin = 5


def dice_callback(*args):
    print(args)


class Die:
    # dot locations for each number in die coordinates
    dot_locations = {1: [(20, 20)],
                     2: [(10, 10), (30, 30)],
                     3: [(10, 10), (20, 20), (30, 30)],
                     4: [(10, 10), (10, 30), (30, 10), (30, 30)],
                     5: [(10, 10), (10, 30), (30, 10),
                         (30, 30), (20, 20)],
                     6: [(10, 10), (10, 20), (10, 30),
                         (30, 10), (30, 20), (30, 30)]}

    def __init__(self, canvas, x=5, fill='white'):
        """
        :param canvas: TK canvas
        :param x: x location of the top left corner of the die
        :param fill: color of the die
        """
        self.canvas = canvas
        self.x = x
        self.fill = fill

        # Draw a blank 40x40 white rectangle to render one die.
        y = margin + size

        self.rectangle = canvas.create_rectangle(x, margin, x+size, y,
                                                 fill=fill)
        self.dots = self._create_dots()

    def _create_dots(self):
        # storage for the dots drawn on the die
        locations = [xy for i in range(1, 7) for xy in self.dot_locations[i]]
        return {xy: self._draw_dot(*xy) for xy in set(locations)}

    def _draw_dot(self, x, y):
        '''
        Draw a dot at the given location.
        :param x: x location in die coordinates
        :param y: y location in die coordinates
        :return:
        '''
        # x, y are with the die
        x += self.x
        y += margin

        delta = 0.1 * size

        upper_x = x - delta
        upper_y = y - delta
        lower_x = x + delta
        lower_y = y + delta

        canvas = self.canvas
        dot = canvas.create_oval(upper_x, upper_y,
                                 lower_x, lower_y,
                                 fill=self.fill, outline=self.fill)

        return dot

    def _clear(self):
        canvas = self.canvas
        for dot in self.dots.values():
            canvas.itemconfig(dot, fill=self.fill)

    def roll(self):
        self._clear()
        n = randint(1, 6)
        canvas = self.canvas
        for xy in self.dot_locations[n]:
            canvas.itemconfig(self.dots[xy], fill='white')
        return n


# Add a method to the Canvas class to create a Die object.
def create_die(canvas, x=5, fill='white'):
    d = Die(canvas, x, fill)
    return d


Canvas.create_die = create_die


def make_callback(dice, methods):
    def callback(*args):
        x = args[0].x
        for i, die in enumerate(dice):
            if (x >= die.x) and (x <= die.x+size):
                return methods[i](args)
        return None
    return callback


def make_dice(tk, fills=['white', 'white'], callbacks=None):
    """
    :param tk: Tkinter object
    :param fills:
    :return:
    """
    n = len(fills)
    width = n * size + (n + 1) * margin
    canvas = Canvas(tk, width=width, height=size + margin)

    dice = [canvas.create_die(x=margin + i * (size + margin), fill=fills[i])
            for i in range(n)]

    if callbacks:
        cb = make_callback(dice, callbacks)
        canvas.bind('<Button-1>', cb)

    def roll_em():
        for die in dice:
            die.roll()

    roll_em()

    return canvas, dice, roll_em


if __name__ == '__main__':

    tk = Tk()
    tk.title('Rolling Dice')

    def red(*args):
        print('red', args)

    def blue(*args):
        print('blue', args)

    def green(*args):
        print('green', args)

    def purple(*args):
        print('purple', args)

    def orange(*args):
        print('orange', args)

    callbacks = [red, blue, green, purple, orange]

    dice_canvas, dice, roll_em = make_dice(tk, fills=['red', 'blue', 'green',
                                                      'purple', 'orange'],
                                           callbacks=callbacks)
    dice_canvas.pack()

    button = Button(tk, text='Roll', command=roll_em)
    button.pack(side='left')
    button2 = Button(tk, text='Exit', command=tk.destroy)
    button2.pack(side='left')
    tk.mainloop()
