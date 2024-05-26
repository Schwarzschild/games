# Games

Games are a great way to learn programming. They are fun and can be very 
challenging. They are also a great way to learn how to think logically and 
solve problems. 

I started this repo to use with students in a computing concepts 
with python course.

The first project was to create a Die object to render a collection of dice 
with tkinter. The second project uses those dice for the game Yahtzee.

## Dice

Example with five colored dice.  This is in the `five_dice.py` file.

    ```python
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

    ```

## Yahtzee

You can play Yahtzee with the `yahtzee.py` script like this: `$ python 
yahtzee.py` 
The rules for Yahtzee are [here](https://en.wikipedia.org/wiki/Yahtzee).  In 
my version of the game you can click on a given die to hold it while you 
roll the second or third rolls of each turn.  You can choose where to apply 
the dice by clicking on the dice on the score card in the relevant row.  Try it.

