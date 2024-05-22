from time import sleep
from tkinter import Tk, Button, Message, Label, Frame
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
    if len(set(dice)) == 1:
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
                                         callbacks=callbacks)
        dice_canvas.pack()
        frame.pack()

        self.dice = dice

        for die in dice:
            die.hold = False

        self.n_rolls = 1
        self.game_over = False

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
            die.clear_legend()
            die.hold = False
        self.n_rolls = 0
        msg['text'] = "Dice rolled - make choices."
        self.roll_em()

    @staticmethod
    def report(die):
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
    def __init__(self, tk, playing_dice):
        self.playing_dice = playing_dice
        card = {'aces': self.row(tk, 'Aces'),
                'twos': self.row(tk, 'Twos'),
                'threes': self.row(tk, 'Threes'),
                'fours': self.row(tk, 'Fours'),
                'fives': self.row(tk, 'Fives'),
                'sixes': self.row(tk, 'Sixes'),
                '3 of a kind': self.row(tk, '3 of a kind'),
                '4 of a kind': self.row(tk, '4 of a kind'),
                'full house': self.row(tk, 'Full House'),
                'small straight': self.row(tk, 'Small Straight'),
                'large straight': self.row(tk, 'Large Straight'),
                'yahtzee': self.row(tk, 'Yahtzee'),
                'chance': self.row(tk, 'Chance')
                }
        self.all_dice = card

    def reset(self):
        if self.playing_dice.game_over:
            self.playing_dice.toggle_game_over()

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
        self.playing_dice.toggle_game_over()
        return True

    def callback(self, *args):
        if self.is_game_over():
            return

        category = args[0].lower()
        dice = self.all_dice[category]['dice']

        if sum(dice):
            msg['text'] = f"You have already scored {category}"
            return

        for d, pd in zip(self.playing_dice.dice,
                         [d for d in dice]):
            pd.n = d.n

        method = f"score_{category}".replace(' ', '_')
        score = eval(method)(dice)
        self.all_dice[category]['score'] = score
        self.all_dice[category]['label']['text'] = f"{category}: {score}"
        self.playing_dice.reset()

        self.is_game_over()

    def make_callback(self, category):
        def callback(*args):
            self.callback(category.lower())
        return callback

    def row(self, tk, category):
        frame = Frame(tk, width=300, height=50)
        dice_canvas, dice, _ = make_dice(frame, fills=fills)
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
    msg['text'] = "Dice rolled - make choices."


tk = Tk()
tk.title('Rolling Dice')
tk.geometry('440x800')
tk.resizable(0, 0)
msg = Message(tk, text="Let's play Yahtzee", width=500)
msg.pack()

dice = FiveDice(tk)

score_card = ScoreCard(tk, playing_dice=dice)


button = Button(tk, text='Restart', command=reset_game)
button.pack(side='left')
button2 = Button(tk, text='Exit', command=tk.destroy)
button2.pack(side='left')


tk.after(1000, lambda: msg.config(text='Dice rolled - make choices.'))


tk.mainloop()
