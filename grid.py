from PIL import Image, ImageDraw
from BarcodeHelper import BarcodeHelper

#Sheet config:
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#number of barcodes to fit in each axes:
gridWidth = 5
gridHeight = 13

sheetResolutions = {
    'A4-Print': (2480, 3508)
}
outputDimensions = sheetResolutions['A4-Print']; #Pixel dimensions of each output sheet

margins = (25, 40) #right/left, up/down in pixels
padding = (20, 25) #right/left, up/down padding withing each barcode grid space
interSpace = (5, 0) #horizontal, vertical Space between each grid block
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#calculate pixel dimensions of barcodes on the grid:
barcodeDimensions = (int((outputDimensions[0] - 2 * margins[0] - (gridWidth - 1) * interSpace[0]) / gridWidth), int((outputDimensions[1] - 2 * margins[1] - (gridHeight - 1) * interSpace[1]) / gridHeight))

def createSequentialBarcodes():
    #Barcode generation config:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    prefix = ""
    suffix = ""
    
    start = 101
    end = 299
    padNumToLength = 3 #pad so that each number has the same number of digits by adding necessary 0-es at the start

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    barcodes = []

    for num in range(start, end + 1):
        content = str(num)
        if len(content) < padNumToLength:
            content = "0" * (padNumToLength - len(content)) + content
        content = prefix + content + suffix

        barcodes.append(BarcodeHelper(content).getBarcodeImage())

    return barcodes

def createSheet(buffer): 
    #create and return sheet of barcodes in specified grid as PIL RGB image
    sheet = Image.new('RGB', (outputDimensions), color='white')
    
    row = 0
    column = 0
    for imgFile in buffer:
        if column == gridWidth:
            row += 1
            column = 0
        
        #resize barcode image to fit inside padded barcodeDimensions box
        ratio = min((barcodeDimensions[0] - 2 * padding[0]) / imgFile.size[0], (barcodeDimensions[1] - 2 * padding[1]) / imgFile.size[1])
        imgFile = imgFile.resize((int(ratio * imgFile.size[0]), int(ratio * imgFile.size[1])))

        #center barcode image in box
        offsetX = int(margins[0] + padding[0] + column * (barcodeDimensions[0] + interSpace[0]) + (barcodeDimensions[0] - imgFile.size[0]) / 2)
        offsetY = int(margins[1] + padding[1] + row * (barcodeDimensions[1] + interSpace[1]) + (barcodeDimensions[1] - imgFile.size[1]) / 2)

        sheet.paste(imgFile, (offsetX, offsetY)) #place barcode onto the sheet at the correct location
        column += 1

    return sheet

sheetBuffer = [] #will contain PIL images of each sheet containing barcodes
barcodeBuffer = []
for bcImage in createSequentialBarcodes():
    barcodeBuffer.append(bcImage)

    if len(barcodeBuffer) == gridWidth * gridHeight:
         #create a sheet with all the barcodes and clear the buffer
         sheetBuffer.append(createSheet(barcodeBuffer))
         barcodeBuffer = []

if len(barcodeBuffer) > 0:
    #add remaining barcodes onto a sheet
    sheetBuffer.append(createSheet(barcodeBuffer))


#convert sheets to a single pdf file
sheetBuffer[0].save("output.pdf", "PDF", resolution=300.0, save_all=True, append_images=sheetBuffer[1:])