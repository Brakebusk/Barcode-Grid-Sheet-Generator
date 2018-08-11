import barcode
from barcode.writer import ImageWriter

class BarcodeHelper:
    def __init__(self, content, bctype="code39"):
        bcclass = barcode.get_barcode_class(bctype)

        self.barcodeImage = bcclass(content, writer=ImageWriter(), add_checksum=False)
    
    def getBarcodeImage(self):
        return self.barcodeImage.render({
            'module_width': 0.38,
            'font_size': 16,
            'text_distance': 1
        })