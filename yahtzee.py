"""
Implement a simple version of the game Yahtzee using tkinter.

Marc Schwarzschild 20240515

"""

from datetime import datetime
from tkinter import Tk, Button, Message, Label, Frame, Text
from dice.rolling_dice import make_dice

fills = ['red', 'blue', 'green', 'purple', 'orange']
categories = ['Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
              '3 of a Kind', '4 of a Kind', 'Full House',
              'Small Straight', 'Large Straight', 'Yahtzee', 'Chance']


def save_score(player_score, computer_score):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('yahtzee_scores.txt', 'a') as f:
        f.write(f"{time_stamp} "
                f"Player: {player_score} Computer:"
                f" {computer_score}\n")


def set_msg():
    s = "Y"

    # Save state of game_over before calling is_game_over
    game_over = score_card.game_over

    if score_card.is_game_over():
        s = "Game Over - y"
        if not game_over:
            # game over state changed
            save_score(score_card.score, score_card_2.score)
    elif dice.n_rolls == 3:
        s = "Already had 3 rolls - y"
    s = f"{s}our score: {score_card.score} " \
        f"vs Computer score: {score_card_2.score}."
    if not s.startswith('Game Over'):
        s += f"  Rolls left: {3 - dice.n_rolls}"
    msg['text'] = s


def count_dice(dice, n):
    s = sum([d.n == n for d in dice])
    return s


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
    for die in set(dice):
        if count_dice(dice, die.n) >= 3:
            return sum(dice)
    return 0


def score_4_of_a_kind(dice):
    for die in set(dice):
        if count_dice(dice, die.n) >= 4:
            return sum(dice)
    return 0


def score_full_house(dice):
    s = set(dice)
    if len(s) == 2 and count_dice(dice, min(s).n) >= 2:
        return 25
    return 0


def score_small_straight(dice):
    # 1, 2, 3, 3, 4, 5, 5
    s = set(dice)
    n = len(s)
    possibilities = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
    if n < 4:
        return 0
    elif n == 6:
        return 30
    elif n == 4:
        s = sorted([d.n for d in s])
        if s in possibilities:
            return 30
    elif n == 5:
        s = sorted([d.n for d in s])
        if s[0:4] in possibilities or s[1:5] in possibilities:
            return 30

    return 0


def score_large_straight(dice):
    s = set(dice)
    if len(s) != 5:
        return 0

    s = sorted([d.n for d in s])
    possibilities = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
    if s in possibilities:
        return 40

    return 0


def score_yahtzee(dice):
    if len(set(dice)) == 1:
        return 50
    return 0


def score_chance(dice):
    return sum(dice)


class FiveDice:
    def __init__(self, frame):
        callbacks = [self.red, self.blue, self.green, self.purple, self.orange]

        dice_canvas, dice, _ = make_dice(frame,
                                         fills=fills,
                                         callbacks=callbacks,
                                         initialize=False)
        dice_canvas.pack()

        self.dice = dice

        for die in dice:
            die.clear()
            die.hold = False

        self._n_rolls = 0

    @property
    def n_rolls(self):
        return self._n_rolls

    def roll_em(self):
        for die in self.dice:
            if all and not die.hold:
                die.roll()
                die.hold = False

        self._n_rolls += 1

    def reset(self):
        for die in self.dice:
            die.n = 0
            die.hold = False
        self._n_rolls = 0
        msg['text'] = "Roll the dice."

    def report(self, i):
        die = self.dice[i]
        if die.n == 0:
            return
        if die.hold:
            die.clear_legend()
            die.hold = False
        else:
            die.set_legend("HOLD")
            die.hold = True

    def red(self, *args):
        self.report(0)

    def blue(self, *args):
        self.report(1)

    def green(self, *args):
        self.report(2)

    def purple(self, *args):
        self.report(3)

    def orange(self, *args):
        self.report(4)


class ScoreCard:
    def __init__(self, tk, playing_dice, name='Player', auto_play=False):
        self.playing_dice = playing_dice
        self.auto_play = auto_play
        frame = Frame(tk, width=300, height=650)
        title = Label(frame, text=name, width=20)
        title.pack(expand=True, fill='x')
        card = {category: self.row(frame, category) for category in categories}
        self.all_dice = card
        self._frame = frame
        self.game_over = False

    @property
    def frame(self):
        return self._frame

    def reset(self):
        self.playing_dice.reset()
        self.game_over = False

        for row in self.all_dice.values():
            for d in row['dice']:
                d.n = 0
            row['score'] = 0
            row['label']['text'] = f"{row['label']['text'].split(':')[0]}: 0"

    @property
    def score(self):
        return sum([row['score'] for row in self.all_dice.values()])

    def is_game_over(self):
        for row in self.all_dice.values():
            if sum(row['dice']) == 0:
                return False
        self.game_over = True
        return True

    def callback(self, *args):
        playing_dice = self.playing_dice

        if sum(playing_dice.dice) == 0:
            return False

        if self.game_over:
            return False

        category = args[0]
        dice = self.all_dice[category]['dice']

        if sum(dice):
            msg['text'] = f"You have already scored {category}"
            return False

        for pd, d in zip(playing_dice.dice, [d for d in dice]):
            d.n = pd.n

        method = f"score_{category}".replace(' ', '_')
        row_score = eval(method.lower())(dice)
        self.all_dice[category]['score'] = row_score
        self.all_dice[category]['label']['text'] = f"{category}: {row_score}"

        playing_dice.reset()

        if not self.auto_play:
            play_for_computer()
            playing_dice.reset()

        set_msg()

        return True

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
        if not self.auto_play:
            dice_canvas.bind('<Button-1>', self.make_callback(category))
        return {'dice': dice, 'label': label, 'score': 0}


def reset_game():
    dice.reset()
    score_card.reset()
    score_card_2.reset()
    msg['text'] = "Roll the dice."


def score_all(dice):
    methods = [f"score_{c}".replace(' ', '_').lower() for c in categories]
    methods = [eval(m) for m in methods]
    scores = [(m(dice.dice), c) for c, m in zip(categories, methods)]
    scores.sort()
    scores.reverse()
    return scores


def play_for_computer():
    dice.roll_em()

    # Get scores for each category in descending order by score
    scores = score_all(dice)

    for score, category in scores:
        if score_card_2.callback(category):
            # Found a category to use
            break


def roll_em():
    game_over = score_card.is_game_over()

    if game_over:
        print(f"Game Over - Your score: {score_card.score}")
    elif dice.n_rolls < 3:
        dice.roll_em()

    set_msg()


tk = Tk()
tk.title('Rolling Dice')
tk.geometry('1000x800')
tk.resizable(0, 0)
msg = Message(tk, text="Let's play Yahtzee", width=500)
msg.pack()

frame = Frame(tk, width=300, height=50)
button = Button(frame, text='Roll', command=roll_em)
button.pack(side='left')
dice = FiveDice(frame)
frame.pack()

frame = Frame(tk)
card_frame = Frame(frame)
score_card = ScoreCard(card_frame, dice, name='Player')
score_card.frame.pack(side='left')
score_card_2 = ScoreCard(card_frame, dice, name='Computer', auto_play=True)
score_card_2.frame.pack()
card_frame.pack()
frame.pack()


button = Button(tk, text='Restart', command=reset_game)
button.pack(side='left')
button2 = Button(tk, text='Exit', command=tk.destroy)
button2.pack(side='left')

tk.mainloop()
