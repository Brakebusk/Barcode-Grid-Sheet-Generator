import barcode
from barcode.writer import ImageWriter

class BarcodeHelper:
    def __init__(self, content, bctype="code128"):
        bcclass = barcode.get_barcode_class(bctype)

        self.barcodeImage = bcclass(content, writer=ImageWriter())
    
    def getBarcodeImage(self):
        return self.barcodeImage.render({
            'module_width': 0.4,
            'text_distance': 1
        })