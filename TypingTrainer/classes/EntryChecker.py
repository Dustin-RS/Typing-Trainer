from classes.WikiParser import WikiParser
MIN_TEXT_LENGTH = 10000


class EntryChecker:
    """
    All logic located here.
    The aim of this class is to check entry(tkinter class) for correct data, and change the text in labels.
    It's connected with text label and input label(label which show what you already typed).
    To work with it, you need to generate an example of it.
    """
    err_cnt = 0  # Amount of user input mistakes.
    sum_cnt = 0  # Total amount of user input characters.
    wiki = WikiParser().info_block  # Get the text from wikipedia article.
    user_inp = None  # Entry widget.
    wiki_label = None  # Label widget. Shows text of article.
    input_label = None  # Label widget. Shows text which was already typed.
    entry_val = None  # String value which related to user_inp. It helps to regulate input text from entry widget.
    input_val = None  # String value which related to input_label. It allows to change label text dynamically.
    wiki_val = None  # String value which related to wiki_label. It allows to change label text dynamically.
    wiki_txt = ''.join(''.join(wiki).split('\n'))  # Make list of string to one string.
    inp_txt = ""  # Used like auxiliary variable.

    def __init__(self):
        """
        Parsing wiki pages until we find the article with more than 10000 characters
        """
        while len(self.wiki_txt) < MIN_TEXT_LENGTH:
            self.wiki = WikiParser().info_block
            self.wiki_txt += ''.join(''.join(self.wiki).split('\n'))

    def entry_limit(self, *args):
        """
        Check the length of input string on entry.
        """
        value = self.entry_val.get()
        if len(value) > 1:
            self.entry_val.set(value[:1])
        self.check_logic()

    def check_logic(self):
        """
        Check if user entered correct character.
        """
        if self.wiki_txt[0] == self.entry_val.get():
            self.inp_txt += self.wiki_txt[0]  # if the character correct, we modify output label.
            if len(self.inp_txt) > 15:  # if the length of output label large we cut the first character.
                self.inp_txt = self.inp_txt[1:]
            if len(self.wiki_txt) > 1:  # if the length of wiki text is not empty we cut correct character.
                self.wiki_txt = self.wiki_txt[1:]

            self.input_val.set(self.inp_txt)
            self.wiki_val.set(self.wiki_txt)

            self.input_label.textvariable = self.input_val
            self.wiki_label.textvariable = self.wiki_val
        elif self.wiki_txt[0] != self.entry_val.get():  # measure amount of mistakes by user.
            self.err_cnt += 1
        self.sum_cnt += 1  # measure amount of total input character by user.
        self.user_inp.delete(0, 'end')  # clear the entry box.

