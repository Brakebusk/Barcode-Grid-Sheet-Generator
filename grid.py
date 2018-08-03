from PIL import Image, ImageDraw
import os

#config:
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
barcodePath = "./barcodes/" #folder containing image files of all the barcodes

#number of barcodes to fit in each axes:
gridWidth = 5
gridHeight = 13

sheetResolutions = {
    'A4-Print': (2480, 3508)
}
outputDimensions = sheetResolutions['A4-Print']; #Pixel dimensions of each output sheet

margins = (20, 40) #right/left, up/down in pixels
padding = (0, 20) #right/left, up/down padding withing each barcode grid space

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#calculate pixel dimensions of barcodes on the grid:
barcodeDimensions = (int((outputDimensions[0] - 2 * margins[0]) / gridWidth), int((outputDimensions[1] - 2 * margins[1]) / gridHeight))

def createSheet(buffer): 
    #create and return sheet of barcodes in specified grid as PIL RGB image
    sheet = Image.new('RGB', (outputDimensions), color='white')
    
    row = 0
    column = 0
    for filePath in buffer:
        if column == gridWidth:
            row += 1
            column = 0
        
        imgFile = Image.open(filePath)
        imgFile = imgFile.resize((barcodeDimensions[0] - 2 * padding[0], barcodeDimensions[1] - 2 * padding[1]))

        offset = (margins[0] + padding[0] + column * barcodeDimensions[0], margins[1] + padding[1] + row * barcodeDimensions[1])
        sheet.paste(imgFile, offset) #place barcode onto the sheet at the correct location
        column += 1

    return sheet

sheetBuffer = [] #will contain PIL images of each sheet containing barcodes
barcodeBuffer = []
for filename in os.listdir(barcodePath):
    filePath = barcodePath + filename
    barcodeBuffer.append(filePath)

    if len(barcodeBuffer) == gridWidth * gridHeight:
        #create a sheet with all the barcodes and clear the buffer
        sheetBuffer.append(createSheet(barcodeBuffer))
        barcodeBuffer = []

if len(barcodeBuffer) > 0:
    #add remaining barcodes onto a sheet
    sheetBuffer.append(createSheet(barcodeBuffer))


#convert sheets to a single pdf file
sheetBuffer[0].save("output.pdf", "PDF", resolution=100.0, save_all=True, append_images=sheetBuffer[1:])