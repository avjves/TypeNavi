from gui.tkinter_gui import TkinterGUI 
from ocr.tesseract import TesseractEngine
import tkinter as tk
import editdistance

class Navigator:

    def __init__(self):
        self.current_gui = TkinterGUI
        self.current_ocr_engine = TesseractEngine
        self.minimum_word_similarity = 0.90
        self.currently_highlighted_term = None
        self.ocr_engine_instance = self.current_ocr_engine.initialize()
        pass

    def start(self):
        #image = self._take_screenshot()
        #self.results = self.ocr_engine_instance.run_ocr(image)

        self.gui_instance = self.current_gui.initialize()
        self.gui_instance.add_callback("search_term_change", self._search_term_changed) 
        self.gui_instance.add_callback("click_term", self._click_highlighted_term)
        self.gui_instance.start()
  
    def _click_highlighted_term(self):
        """
        Called when user signals that they want the mouse to click the currently highlighted term.
        """
        print("Clicking: ", self.currently_highlighted_term)
        self.gui_instance.exit()

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
            print(similarity)
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
        print("Matching...")
        current_search_term = self.gui_instance.get_search_term()
        if not current_search_term.strip(): return
        ocr_results = self.ocr_engine_instance.get_ocr_results('placeholder.png')
        #ocr_results = [("kissa", [100, 200]), ("koira", [200, 300])]
        # For now, assuming that the data is ready
        
        possible_matches = self._match_term_to_results(current_search_term, ocr_results)
        # TODO: remember current position and allow passing through different matches
        print(possible_matches)
        if possible_matches:
            self.currently_highlighted_term = possible_matches[0]
            self.gui_instance.highlight_term(possible_matches[0])
            
                
    def _take_screenshot(self):
        """
        Takes a screenshot of current screen.
        """
        # For now, loading a placeholder image.
        image = open("placeholder.png", "rb").read()
        return image

if __name__ == "__main__":
    
    n = Navigator()
    n.start()
    
