import os

class TesseractEngine:

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        return TesseractEngine()

    def get_ocr_results(self, image_path):
        """
        Given a path to an image, runs said image through tesseract OCR and returns the results.
        """
        # os.system("tesseract {} out txt makebox".format(image_path))
        os.system("C:/Tesseract-OCR/tesseract {} out tsv".format(image_path))
        tsv = open("out.tsv", errors="ignore").readlines()
        results = []
        for line in tsv[1:]:
            splits = line.split()
            if not len(splits) == 12:
                continue
            else:
                left, top, width, height = [float(val) for val in splits[6:10]]
                text = splits[11]
                results.append([text, [left, top, width, height]])
        # text = open("out.txt").read()
        # words = [word for word in text.split()]
        # boxes = open("out.box").readlines()
        # boxes = [line.strip() for line in boxes if not line.startswith("~")]
        # results = []
        # assert len(boxes) == len(''.join(words))
        # for word in words:
            # chars = boxes[:len(word)]
            # values = [v.split(" ") for v in chars]
            # boxes = boxes[len(word):]
            # left = min([float(v[1]) for v in values])
            # bottom = min([float(v[2]) for v in values])
            # right = max([float(v[3]) for v in values])
            # top = max([float(v[4]) for v in values])
            # results.append([word, [left, bottom, right, top]])
        return results
