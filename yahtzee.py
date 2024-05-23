"""
Implement a simple version of the game Yahtzee using tkinter.

Marc Schwarzschild 20240515

"""
from tkinter import Tk, Button, Message, Label, Frame, Text
from dice.rolling_dice import make_dice

fills = ['red', 'blue', 'green', 'purple', 'orange']


def score_aces(dice):
    return sum([d.n for d in dice if d.n == 1])


def score_twos(dice):
    return sum([d.n for d in dice if d.n == 2])


def score_threes(dice):
    return sum([d.n for d in dice if d.n == 3])


def score_fours(dice):
    return sum([d.n for d in dice if d.n == 4])


def score_fives(dice):
    return sum([d.n for d in dice if d.n == 5])


def score_sixes(dice):
    return sum([d.n for d in dice if d.n == 6])


def score_3_of_a_kind(dice):
    if len(set(dice)) <= 3:
        return sum(dice)
    return 0


def score_4_of_a_kind(dice):
    if len(set(dice)) <= 2:
        return sum(dice)
    return 0


def score_full_house(dice):
    if len(set(dice)) == 2:
        return 25
    return 0


def score_small_straight(dice):
    if len(set(dice)) >= 4:
        return 30
    return 0


def score_large_straight(dice):
    if len(set(dice)) == 5:
        return 40
    return 0


def score_yahtzee(dice):
    if dice[0].n and (len(set(dice)) == 1):
        return 50
    return 0


def score_chance(dice):
    return sum(dice)


class FiveDice:
    def __init__(self, tk):
        callbacks = [self.red, self.blue, self.green, self.purple, self.orange]

        frame = Frame(tk, width=300, height=50)
        button = Button(frame, text='Roll', command=self.roll_em)
        button.pack(side='left')
        dice_canvas, dice, _ = make_dice(frame, fills=fills,
                                         callbacks=callbacks,
                                         initialize=False)
        dice_canvas.pack()
        frame.pack()
        self._frame = frame

        self.dice = dice

        for die in dice:
            die.clear()
            die.hold = False

        self.n_rolls = 0
        self.game_over = False

    @property
    def frame(self):
        return self._frame

    def roll_em(self, all=True):
        if self.game_over:
            msg['text'] = 'Game Over - Start a new game'
            return

        if self.n_rolls == 3:
            msg['text'] = 'You have reached the maximum number of rolls'
            return

        for die in self.dice:
            if all and not die.hold:
                die.roll()
                die.hold = False

        if self.n_rolls == 2:
            msg['text'] = "That's three rolls - choose a category."

        self.n_rolls += 1

    def reset(self):
        for die in self.dice:
            die.n = 0
            die.hold = False
        self.n_rolls = 0
        msg['text'] = "Roll the dice."

    @staticmethod
    def report(die):
        if die.n == 0:
            return
        if die.hold:
            die.clear_legend()
            die.hold = False
        else:
            die.set_legend("HOLD")
            die.hold = True

    def red(self, *args):
        FiveDice.report(self.dice[0])

    def blue(self, *args):
        FiveDice.report(self.dice[1])

    def green(self, *args):
        FiveDice.report(self.dice[2])

    def purple(self, *args):
        FiveDice.report(self.dice[3])

    def orange(self, *args):
        FiveDice.report(self.dice[4])

    def toggle_game_over(self):
        self.game_over = not self.game_over


class ScoreCard:
    def __init__(self, tk, name='Player', playing_dice=None):
        self.playing_dice = playing_dice
        frame = Frame(tk, width=300, height=650)
        title = Label(frame, text=name, width=20)
        title.pack(expand=True, fill='x')
        card = {'Aces': self.row(frame, 'Aces'),
                'Twos': self.row(frame, 'Twos'),
                'Threes': self.row(frame, 'Threes'),
                'Fours': self.row(frame, 'Fours'),
                'Fives': self.row(frame, 'Fives'),
                'Sixes': self.row(frame, 'Sixes'),
                '3 of a Kind': self.row(frame, '3 of a Kind'),
                '4 of a Kind': self.row(frame, '4 of a Kind'),
                'Full House': self.row(frame, 'Full House'),
                'Small Straight': self.row(frame, 'Small Straight'),
                'Large Straight': self.row(frame, 'Large Straight'),
                'Yahtzee': self.row(frame, 'Yahtzee'),
                'Chance': self.row(frame, 'Chance')
                }
        self.all_dice = card
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    def reset(self):
        playing_dice = self.playing_dice
        if playing_dice and playing_dice.game_over:
            playing_dice.toggle_game_over()

        for row in self.all_dice.values():
            for d in row['dice']:
                d.n = 0
            row['score'] = 0
            row['label']['text'] = f"{row['label']['text'].split(':')[0]}: 0"

    def is_game_over(self):
        for row in self.all_dice.values():
            if sum(row['dice']) == 0:
                return False
        total_score = sum([row['score'] for row in self.all_dice.values()])
        msg['text'] = f"Game Over - Total Score: {total_score}"
        if self.playing_dice:
            self.playing_dice.toggle_game_over()
        return True

    def callback(self, *args):
        if not self.playing_dice:
            return

        if self.is_game_over():
            return

        category = args[0]
        dice = self.all_dice[category]['dice']

        if sum(dice):
            msg['text'] = f"You have already scored {category}"
            return

        for d, pd in zip(self.playing_dice.dice,
                         [d for d in dice]):
            pd.n = d.n

        method = f"score_{category}".replace(' ', '_')
        score = eval(method.lower())(dice)
        self.all_dice[category]['score'] = score
        self.all_dice[category]['label']['text'] = f"{category}: {score}"
        if self.playing_dice:
            self.playing_dice.reset()

        self.is_game_over()

    def make_callback(self, category):
        def callback(*args):
            self.callback(category)
        return callback

    def row(self, tk, category):
        frame = Frame(tk, width=300, height=50)
        dice_canvas, dice, _ = make_dice(frame, fills=fills, initialize=False)
        for die in dice:
            die.n = 0
        label = Label(frame, text=f"{category}: 0", width=20)
        label.pack(side='left')
        dice_canvas.pack(side='right')

        frame.pack()
        dice_canvas.bind('<Button-1>', self.make_callback(category))
        return {'dice': dice, 'label': label, 'score': 0}


def reset_game():
    dice.reset()
    score_card.reset()
    msg['text'] = "Roll the dice."


tk = Tk()
tk.title('Rolling Dice')
tk.geometry('1000x800')
tk.resizable(0, 0)
msg = Message(tk, text="Let's play Yahtzee", width=500)
msg.pack()

dice = FiveDice(tk)
dice.frame.pack(side='top')

frame = Frame(tk)#, width=900, height=790)

card_frame = Frame(frame)# , width=900, height=700)
score_card = ScoreCard(card_frame, name='Player', playing_dice=dice)
score_card.frame.pack(side='left')
score_card_2 = ScoreCard(card_frame, name='Computer')
score_card_2.frame.pack()
card_frame.pack()

frame.pack()


button = Button(tk, text='Restart', command=reset_game)
button.pack(side='left')
button2 = Button(tk, text='Exit', command=tk.destroy)
button2.pack(side='left')


# tk.after(1000, lambda: msg.config(text='Dice rolled - make choices.'))


tk.mainloop()
