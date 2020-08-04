import easyocr

class EasyOCREngine:

    def __init__(self):
        self.reader = None
        pass 

    @staticmethod
    def initialize():
        engine = EasyOCREngine()
        #engine._make_reader()
        return engine

    def get_ocr_results(self, image_path):
        """
        Given a path to an image, runs said image through the OCR system and returns the results.
        """
        #results = self.reader.readtext(image_path)
        import pickle
        #pickle.dump(results, open("results.pkl", "wb"))
        results = pickle.load(open("results.pkl", "rb"))
        formatted_results = []
        for result in results:
            position = result[0]
            word = result[1]
            formatted_results.append((word, position))

        return formatted_results

    def _make_reader(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
