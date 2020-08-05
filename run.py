import pyautogui
import editdistance
import pyscreenshot as ImageGrab
import win32api, win32con

from gui.wxpython_gui import WxPythonGUI
from ocr.tesseract import TesseractEngine

class Navigator:

    def __init__(self):
        self.current_gui = WxPythonGUI
        self.current_ocr_engine = TesseractEngine
        self.minimum_word_similarity = 0.90
        self.currently_highlighted_term = None
        self.ocr_engine_instance = self.current_ocr_engine.initialize()
        pass

    def start(self):
        image_path = self._take_screenshot()
        self.ocr_results = self.ocr_engine_instance.get_ocr_results(image_path)

        self.gui_instance = self.current_gui.initialize()
        self.gui_instance.add_callback("search_term_change", self._search_term_changed) 
        self.gui_instance.add_callback("click_term", self._click_highlighted_term)
        self.gui_instance.start()
  
    def _click_highlighted_term(self):
        """
        Called when user signals that they want the mouse to click the currently highlighted term.
        """
        if self.currently_highlighted_term:
            self.gui_instance.exit()
            print("Clicking: ", self.currently_highlighted_term)
            # current_x, current_y = pyautogui.displayMousePosition()
            x,y = self.currently_highlighted_term[1][0:2]
            x, y = int(x), int(y)

            win32api.SetCursorPos((x, y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


    def _match_term_to_results_with_levenshtein(self, current_search_term, ocr_results):
        """
        Given a list of (word, position) pairs, matches the words to current search term.
        Uses levenshtein distance to match the term and a threshold. Assumes the ocr results are
        returned in the order they're seen on the screen, so all results that contain the same similarity score
        will just be sorted by that order.
        """
        possible_matches = []
        for result in ocr_results:
            ocr_result_word = result[0]
            distance = editdistance.eval(current_search_term, ocr_result_word)
            similarity = 1 - distance / max(len(ocr_result_word), len(current_search_term)) 
            if similarity > self.minimum_word_similarity:
                possible_matches.append(result)

        return possible_matches

    def _match_term_to_results(self, current_search_term, ocr_results):
        """
        Given a list of (word, position) pairs, attempts to find if the current search therm appears somewhere in them
        and highlights that portion of said word/term.
        """
        possible_matches = []
        for result in ocr_results:
            ocr_result_word = result[0].lower()
            if current_search_term in ocr_result_word:
                possible_matches.append(result)
        return possible_matches


    def _search_term_changed(self):
        current_search_term = self.gui_instance.get_search_term()
        if not current_search_term.strip(): return
        # For now, assuming that the data is ready
        possible_matches_contains = self._match_term_to_results(current_search_term, self.ocr_results)
        possible_matches_lev = self._match_term_to_results_with_levenshtein(current_search_term, self.ocr_results)
        possible_matches = possible_matches_contains + possible_matches_lev
        # TODO: remember current position and allow passing through different matches
        if possible_matches:
            self.currently_highlighted_term = possible_matches[0]
            self.gui_instance.highlight_term(possible_matches[0])
        else:
            self.gui_instance.remove_highlights()

    def _take_screenshot(self):
        """
        Takes a screenshot of current screen.
        """
        # For now, loading a placeholder image.
        im = ImageGrab.grab()
        im.save('crnt.png')
        return 'crnt.png'

if __name__ == "__main__":
    
    n = Navigator()
    n.start()


