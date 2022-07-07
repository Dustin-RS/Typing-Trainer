import re
import requests   # pip install requests
import wikipedia  # pip install wikipedia
from bs4 import BeautifulSoup   # pip install bs4


class WikiParser:
    """
    All text generation logic located here.
    WikiParser - is a class which parse a text from wikipedia website.
    The constructor of this class randomly generate the wiki link, and takes all the paragraphs.
    To work with it, you need to generate an example of it.
    info_block attribute has all the paragraphs from random wiki-site.
    """
    info_block = []  # List of each paragraph from wikipedia.

    def __init__(self):
        """
        Take a text from random wiki article and remove from it:
            all non ascii characters,
            all links(data in square brackets).
        After it put processed strings put into info_block list.
        """
        self.URL = self.random_page().url  # Wiki article link.
        respond = requests.get(self.URL)  # Get html code.
        soup = BeautifulSoup(respond.text, features="html.parser")  # Make it a text.

        info_wiki = soup.find_all('p')  # Only get a paragraphs block.
        for item in info_wiki[3:]:
            encoded_string = item.text.encode("ascii", "ignore")  # Remove all non ascii characters.
            decode_string = encoded_string.decode()
            decode_string = "".join(re.split(r"\(|\)|\[|\]", decode_string)[::2])  # Remove unnecessary brackets.
            self.info_block.append(decode_string)  # Put all text into info_block

    def random_page(self):
        """
        Get a random page from wikipedia(it return page url, title, links, data inside.
        """
        random = wikipedia.random(1)
        try:
            result = wikipedia.page(random)
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
            result = self.random_page()
        return result
