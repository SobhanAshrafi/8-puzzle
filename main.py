import random
from tkinter import *
from tkinter import ttk
import threading
import multiprocessing
from time import sleep


class App(Tk):

    def __init__(self, screen_width=650, screen_height=750):
        super().__init__()

        self.title("8 - Puzzle")

        center_x = self.winfo_screenwidth() // 2 - screen_width // 2
        center_y = self.winfo_screenheight() // 2 - screen_height // 2

        self.geometry(f'{screen_width}x{screen_height}+{center_x}+{center_y}')

        self.minsize(width=600, height=600)

        # Create main Frame of Window!        
        self.main_frame = ttk.Frame(master=self, padding="12 12 12 12")

        # Styling main Frame
        ttk.Style().configure('mainWin.TFrame', background="purple")
        self.main_frame.config(style='mainWin.TFrame')

        self.main_frame.pack(fill='both', expand=1, anchor="c")


class Game:

    def __init__(self, root):

        self.root = root
        self.window = root.main_frame

        # Controller Frame : contains all widgets that user will intract with them (e.g. Start Btn, Stop Btn, Entries of Start state and so on.) 
        self.controller_frame = ttk.LabelFrame(master=self.window, text="controller", padding="20 15 0 15")
        self.controller_frame.pack(fill='both', padx=10)

        # Error Message : The start state is not correct!
        self.error_message = Label(master=self.controller_frame, text='', foreground='red', anchor='w')
        self.error_message.pack(side='top', fill='x')

        # Select One Algorithm to run
        self.algorithm_frame = ttk.LabelFrame(master=self.controller_frame, text="Algorithm", padding="10 20 10 10")
        self.algorithm_frame.pack(side='left', padx=5)

        self.algorithm_selection = ttk.Combobox(master=self.algorithm_frame, values=[], state="readonly")
        self.algorithm_selection.grid(row=0, column=0, columnspan=2, ipadx=14, ipady=2)

        # Start Btn, Stop Btn, Back Btn, Next Btn
        self.start_init_button = Button(master=self.algorithm_frame, text="Start", width=7, command=self.start_game)
        self.start_init_button.grid(row=1, column=0, columnspan=1, pady=15)

        # TODO : set command for stop, previous and next Buttons and implement them.
        self.stop_button = Button(master=self.algorithm_frame, text="Stop", width=7)
        self.stop_button.grid(row=1, column=1, columnspan=1, pady=15)

        next_prev_btn_frame = ttk.Frame(master=self.algorithm_frame)
        next_prev_btn_frame.grid(row=2, column=0, columnspan=2)

        self.previous_button = Button(master=next_prev_btn_frame, text="<<", width=3)
        self.previous_button.pack(side='left')

        self.next_button = Button(master=next_prev_btn_frame, text=">>", width=3)
        self.next_button.pack()

        # maintains amount of each node (puzzle) of start state.
        self.start_state_entries = []

        # background color for puzzle with valid number (uses in start state entries validations!)
        self.bg_color_correct_node = 'aquamarine2'

        # background color for puzzles with same digits as a warning (uses in start state entries validations!)
        self.bg_color_same_values = {'1': 'red1', '2': 'red2', '3': 'red3', '4': 'red4',
                                     '5': 'orange1', '6': 'orange2', '7': 'orange3',
                                     '8': 'orange4'}  # puzzle value : color

        # Start State : User should Enter a start state for the game! so we need 8 entry widget.
        self.init_state_frame = ttk.LabelFrame(self.controller_frame, name='init_state_frame', text='Start State',
                                               padding="20 20 20 20")
        self.init_state_frame.pack(side='right', padx=50)

        # register validate command for every puzzle of start state.
        # %W: name of widget obj , %P: value (content) of widget
        vcmd_start_state = (self.root.register(self.start_state_validate), '%W', '%P')

        # create puzzles of start state.
        for i in range(9):
            frame_i = ttk.Frame(master=self.init_state_frame, padding=3)
            frame_i.grid(row=i // 3, column=i % 3)

            self.start_state_entries.append(Entry(master=frame_i, width=5, justify="c", validate="key",
                                                  validatecommand=vcmd_start_state))
            self.start_state_entries[-1].pack(ipady=10)

        # board of the game : show current state puzzles
        self.board_frame = ttk.Labelframe(master=self.window, text="board")
        self.board_frame.pack(fill='both', expand=1, padx=10, pady=10)

        self.canvas_width = 400
        self.canvas_height = 400
        self.square_size = 100
        self.grid_size = 3

        self.start_state = []  # it will initialize from self.start_state_entries when start btn clicked.
        self.curr_state = []
        self.curr_state_display = []

        self.board_canvas = Canvas(master=self.board_frame, width=self.canvas_width, height=self.canvas_height)
        self.board_canvas.pack(anchor="center", pady=5)

        self.draw_puzzle()

        # TODO : Find algorithms. we can do it with a function
        #  and then every time user click on algorithm_selection it will run and so update algorithm lists.

    def start_state_validate(self, widget_entry_name, value):

        # each puzzle value should be a digit from 1 to 8 or empty str ''.
        if value == '':
            pass
        elif len(value) > 1:
            return False
        elif not str.isdigit(value) or int(value) in (0, 9):
            return False

        # get entry widget
        entry = self.root.nametowidget(widget_entry_name)

        # set 'white' background color for value '' and self.bg_color_correct_node for value 1-8
        if value == '':
            entry.config(bg='white')
        else:
            entry.config(bg=self.bg_color_correct_node)

        # puzzles with same value get special same background color as a warning.

        num_list = [x.get() for x in self.start_state_entries]  # get all entry puzzle values

        # update current entry value in num_list
        i_curr = self.start_state_entries.index(entry)
        num_list[i_curr] = value

        for i in range(1, 9):
            wrong_entry_indexes = []

            for j in range(len(num_list)):
                if num_list[j] == str(i):
                    wrong_entry_indexes.append(j)

            if len(wrong_entry_indexes) > 1:
                for k in wrong_entry_indexes:
                    self.start_state_entries[k].config(bg=self.bg_color_same_values[str(i)])

            elif len(wrong_entry_indexes) == 1:
                self.start_state_entries[wrong_entry_indexes[0]].config(bg=self.bg_color_correct_node)

        return True

    # TODO : draw puzzle should show values of current state.
    def draw_puzzle(self):
        grid_width = self.square_size * self.grid_size
        grid_height = self.square_size * self.grid_size

        x_offset = (self.canvas_width - grid_width) // 2
        y_offset = (self.canvas_height - grid_height) // 2

        square_color = "red"

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = x_offset + col * self.square_size
                y1 = y_offset + row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.board_canvas.create_rectangle(x1, y1, x2, y2)

                self.curr_state_display.append(self.board_canvas.create_text(abs(x2 - x1), abs(y2 - y1)))

    def make_random_start_state(self):
        xx = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
        random.shuffle(xx)

        for i in range(9):
            self.start_state_entries[i].delete(0)
            self.start_state_entries[i].insert(0, xx[i])
            print(self.start_state_entries[i]['text'])


    def start_game(self):

        if len([x for x in self.start_state_entries if x.get() == '']) == 9:
            self.make_random_start_state()

        # TODO : check if selected algorithm is valid?
        # TODO : initialize self.start_state

        # check that start state be ok!

        l = list(filter((lambda x: x['bg'] == self.bg_color_correct_node), self.start_state_entries))

        if len(l) < 8:
            self.error_message['text'] = 'The start state is not correct!'
            return False

        else:
            self.error_message['text'] = ''
            for entry in self.start_state_entries:
                self.start_init_button.focus_set()
                entry['state'] = 'disabled'

        self.start_init_button.config(state='disabled', borderwidth=2)

        # maybe start thread to exec _start_game()
        _start_game_theard = threading.Thread(target=self._start_game)
        _start_game_theard.start()

    # TODO : create a new process to run selected algorithm and sync its data with game board.

    # TODO : implement _start_game method.
    def _start_game(self):

        sleep(10)


def main():

    root = App()

    game = Game(root)

    root.mainloop()


if __name__ == '__main__':
    main()
