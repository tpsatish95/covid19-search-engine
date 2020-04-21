import abc


class Scraper(metaclass=abc.ABCMeta):  # abc.ABC):
    """Scraper class that scrapes a website for FAQs and stores the output to a file"""

    def __init__(self, *, path, filename):
        self._path = path
        self._filename = filename

    @abc.abstractmethod
    def scrape(self):
        """Extracts faqs, converts them using the conversion class
        params: None
        returns: boolean indicating success
            return conversion.write()
        """
        pass