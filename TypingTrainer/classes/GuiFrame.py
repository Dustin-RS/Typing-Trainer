import tkinter as tk
import time
from classes.EntryChecker import EntryChecker
MAX_PERCENTAGE = 100
MAX_RATE = 1
AVG_AMOUNT_CHAR_IN_WORD = 5
SEC_IN_MINUTES_IN_HOUR = 60


class GuiFrame:
    """
    All widgets generation and drawing located here.
    GuiFrame - is a class which generate and show all visual widgets.
    It has 5 methods all are public(will be changed to private in future).
    To work with it, you need to generate it's example.
    Class constructor will draw all widgets.
    """
    start_time = None  # Time since typing start.
    end_time = None  # Time when typing end.
    gui = EntryChecker()  # Created only once. We add to it all objects which connected with entry.
    results = []  # Results of program measurements: CPM, WPM, Accurate, final time.
    result_label = None  # Label where the result will be written.

    def visual_chg_start(self):
        """
        Change and locate widgets after start button was pressed.
        """
        self.gui.wiki_label.grid(row=1, column=1, sticky="w")  # Locate label and put it on the west of grid column.
        self.gui.input_label.grid(row=1, column=0, sticky="e")  # Locate label and put it on the east of grid column.
        self.gui.user_inp.grid(row=2, column=0)
        self.stop_button.grid(row=0, column=1)

        self.start_button.grid_forget()  # Make a start button invisible.

        self.gui.wiki_label.config(fg="black")
        self.gui.user_inp.config(state="normal")
        self.start_button.config(state="disable")
        self.stop_button.config(state="active")
        self.result_label.config(text="")

    def visual_chg_stop(self):
        """
        Change and locate widgets after stop button was pressed.
        """
        self.start_button.grid(row=0, column=0)

        self.stop_button.grid_forget()  # Make a stop button invisible.

        self.gui.user_inp.config(state="disable")
        self.start_button.config(state="active")
        self.gui.wiki_label.config(fg="gray")
        self.stop_button.config(state="disable")
        self.result_label.config(text=''.join(self.results))

    def measure_start(self):
        """
        Start a timer to measure how long the user has been typing.
        """
        self.visual_chg_start()

        self.start_time = time.time()

    def measure_stop(self):
        """
        Stop the timer and calculate params.
        """
        if self.end_time is None:
            self.end_time = time.time() - self.start_time
        else:
            back_time = time.time() - self.start_time
            self.end_time += back_time
        try:
            minutes = int(self.end_time / SEC_IN_MINUTES_IN_HOUR)
            seconds = self.end_time % SEC_IN_MINUTES_IN_HOUR
            cps = self.gui.sum_cnt / self.end_time
            wpm = cps * SEC_IN_MINUTES_IN_HOUR / AVG_AMOUNT_CHAR_IN_WORD
            acc = MAX_PERCENTAGE * (MAX_RATE-self.gui.err_cnt/self.gui.sum_cnt)
        except ZeroDivisionError:
            cps = 0
            wpm = 0
            acc = 0
        self.results = ["Your results:\n", f"Time: min:{int(minutes)} sec:{int(seconds)}\n",
                        f"Characters Per Second: {int(cps)}\n", f"Word Per Minute: {int(wpm)}\n",
                        f"Accurate: {int(acc)}%\n"]
        self.visual_chg_stop()

    def gui_init(self):
        """
        Creating widgets inside gui object which bounded with each other.
        """
        self.gui.entry_val = tk.StringVar()
        self.gui.input_val = tk.StringVar()
        self.gui.wiki_val = tk.StringVar()
        self.gui.wiki_val.set(self.gui.wiki_txt)

        self.gui.entry_val.trace('w', self.gui.entry_limit)

        self.gui.wiki_label = tk.Label(self.root, textvariable=self.gui.wiki_val, width=100, anchor="w",
                                       font=("Helvetica", 18), fg="gray")
        self.gui.input_label = tk.Label(self.root, textvariable=self.gui.input_val, anchor="e", fg="red",
                                        font=("Helvetica", 18))
        self.gui.user_inp = tk.Entry(self.root, width=10, textvariable=self.gui.entry_val, highlightthickness=0,
                                     borderwidth=0, insertontime=0, state="disable", bg="#f0f0f0")
        self.gui.user_inp.focus()

    def __init__(self):
        """
        Creating and locate all widgets with all dependencies.
        """
        self.root = tk.Tk()

        self.start_button = tk.Button(self.root, text="Start!", command=self.measure_start, bd=2,
                                      font=("Helvetica", 10), width=15, fg="#2980b9", bg="#bdc3c7",
                                      highlightbackground="#e74c3c")  # Design start button.
        self.stop_button = tk.Button(self.root, text="Stop!", command=self.measure_stop, state="disable", bd=2,
                                     font=("Helvetica", 10), width=15, fg="#2980b9", bg="#bdc3c7")
        self.result_label = tk.Label(self.root, font=("Helvetica", 18))

        self.result_label.grid(row=3, column=1)
        self.start_button.grid(row=0, column=0)
        self.stop_button.grid_forget()  # Make stop button invisible.
        self.gui_init()

        self.root.mainloop()
