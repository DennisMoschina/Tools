import pygame
import serial
import time


width = 700

expectedLengh = 500

applicationClose = False
serialStringIn = ""
newDataAvailable = False
BLACK   = ( 0, 0, 0 )
WHITE   = ( 255, 255, 255 )
GREEN   = ( 0, 255, 0 )
RED     = ( 255, 0, 0 )
BLUE    = ( 0, 0, 255 )
PINK    = ( 255, 0, 255 )
YELLOW  = ( 255, 255, 0 )
timeUnit = "us"

loops = 0
max_value = 0
min_value = 255

reference = 175

recordedData = []
recording = False
showRecordings = False

showedInterval = [0, 0]


timeBase = 100

pygame.init()

pygame.font.init()

myfont = pygame.font.SysFont('monospace', 16)

size = (width + 100, 450)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Oscilloscope")


try:
    serialPort = serial.Serial("/dev/cu.usbmodem14601", 115200)
except:
    serialPort = serial.Serial("/dev/cu.usbmodem14401", 115200)
serialPort.timeout = 0.05


while applicationClose == False:


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if showRecordings:
                if event.unicode == "q":
                    showRecordings = False
                    showedInterval = [0, 0]
                    # serialPort.reset_input_buffer()
                    time.sleep(0.1)
                if event.unicode == "+":
                    if showedInterval[0] + 150 < showedInterval[1]:
                        showedInterval[0] += 50
                        showedInterval[1] -= 50
                if event.unicode == "-":
                    if not showedInterval[0] == 0:
                        showedInterval[0] -= 50
                        showedInterval[1] += 50
                if event.key == 275:
                    if showedInterval[1] + 100 <= len(recordedData):
                        showedInterval[0] += 100
                        showedInterval[1] += 100
                if event.key == 276:
                    if showedInterval[0] - 100 >= 0:
                        showedInterval[0] -= 100
                        showedInterval[1] -= 100
                if event.key == 273:
                    if reference + 5 <= 255:
                        reference += 5
                if event.key == 274:
                    if reference - 5 >= 0:
                        reference -= 5
            else:
                if event.unicode == "r" and not showRecordings:
                    recording = True
                    recordedData = []
                if event.unicode == "s" and not showRecordings:
                    recording = False
                if event.unicode == "p":
                    if len(recordedData) > 0:
                        showRecordings = True
                        showedInterval = [0, len(recordedData)]
                    else:
                        showRecordings = False

        if event.type == pygame.QUIT:
            applicationClose = True
            serialPort.close()
            pygame.display.quit()
            pygame.quit()

    if applicationClose:
        break



    if serialPort.in_waiting > 0 and not showRecordings:
        serialStringIn = serialPort.readline()
        if serialStringIn[:len(serialStringIn) - 2] == b'R?':
            serialPort.reset_input_buffer()
            serialPort.write(b"K")
            while serialPort.in_waiting < expectedLengh - 1:
                time.sleep(0.00001)

            data = serialPort.read(expectedLengh)

            if recording:
                recordedData += data

            newDataAvailable = True

            average = sum(data) / len(data)

            if loops % 10 == 0:
                max_value = 0
                min_value = 255

            max_value = max(data)
            min_value = min(data)

        serialPort.reset_input_buffer()

    if newDataAvailable or showRecordings:
        screen.fill(BLACK)

        if showRecordings:
            showedData = recordedData[showedInterval[0]:showedInterval[1]]

            for i in range(0, len(showedData) - 2):
                pygame.draw.line(screen, RED, [40 + ((i * 100 / len(showedData)) * (width / 100)), 400 - showedData[i]], [40 + (((i + 1) * 100 / len(showedData)) * (width / 100)), 400 - showedData[i+1]], 2)

            max_value = max(showedData)
            min_value = min(showedData)

            average = sum(showedData) / len(showedData)

            label_time0     = myfont.render('0' + timeUnit, False, (255, 255, 255))
            label_time25    = myfont.render(str(round(timeBase * len(showedData) * 0.25, 0)) + timeUnit, False, (255, 255, 255))
            label_time50    = myfont.render(str(round(timeBase * len(showedData) * 0.50, 0)) + timeUnit, False, (255, 255, 255))
            label_time75    = myfont.render(str(round(timeBase * len(showedData) * 0.75, 0)) + timeUnit, False, (255, 255, 255))
            label_time100   = myfont.render(str(round(timeBase * len(showedData) * 0.100, 0)) + timeUnit, False, (255, 255, 255))

            pygame.draw.line(screen, YELLOW, [40, 400 - reference], [width, 400 - reference], 1)

            referenceV = round((reference / 255) * 5, 2)
            label_reference = myfont.render(str(referenceV) + 'V', False, YELLOW)
            screen.blit(label_reference, (width + 10, 393 - reference))

        else:
            for i in range(0, len(data) - 2):
                pygame.draw.line(screen, RED, [40 + ((i * 100 / len(data)) * (width / 100)), 400 - data[i]], [40 + (((i + 1) * 100 / len(data)) * (width / 100)), 400 - data[i+1]], 2)

            label_time0     = myfont.render('0' + timeUnit, False, (255, 255, 255))
            label_time25    = myfont.render(str(round(timeBase * len(data) * 0.25)) + timeUnit, False, (255, 255, 255))
            label_time50    = myfont.render(str(round(timeBase * len(data) * 0.50)) + timeUnit, False, (255, 255, 255))
            label_time75    = myfont.render(str(round(timeBase * len(data) * 0.75)) + timeUnit, False, (255, 255, 255))
            label_time100   = myfont.render(str(round(timeBase * len(data) * 1)) + timeUnit, False, (255, 255, 255))



        pygame.draw.line(screen, BLUE, [40, 400 - average], [width, 400 - average], 1)

        pygame.draw.line(screen, GREEN, [40, 400], [width, 400], 1)
        pygame.draw.line(screen, GREEN, [40, 400], [40, 145], 1)

        label_5V    = myfont.render('5.0V', False, (255, 0, 0))
        label_3_3V  = myfont.render('3.3V', False, (255, 0, 0))
        label_2_5V  = myfont.render('2.5V', False, (255, 0, 0))
        label_0V    = myfont.render('0V', False, (255, 0, 0))


        averageV = (average / 255) * 5
        averageV = round(averageV, 2)
        label_average = myfont.render(str(averageV) + 'V', False, (0, 0, 255))
        screen.blit(label_average, (width + 10, 393 - average))

        minV = round((min_value / 255) * 5, 2)
        maxV = round((max_value / 255) * 5, 2)
        label_max = myfont.render(str(maxV) + 'V', False, PINK)
        label_min = myfont.render(str(minV) + 'V', False, WHITE)
        pygame.draw.line(screen, WHITE, [40, 400 - min_value], [width, 400 - min_value], 1)
        pygame.draw.line(screen, PINK, [40, 400 - max_value], [width, 400 - max_value], 1)
        screen.blit(label_max, (width + 10, 393 - max_value))
        screen.blit(label_min, (width + 10, 393 - min_value))

        screen.blit(label_5V, (5, 138))
        screen.blit(label_3_3V, (5, 225))
        screen.blit(label_2_5V, (5, 266))
        screen.blit(label_0V, (5, 393))

        screen.blit(label_time0, (40, 410))
        screen.blit(label_time25, (40+((width - 50) * 0.25), 410))
        screen.blit(label_time50, (40+((width - 50) * 0.5), 410))
        screen.blit(label_time75, (40+((width - 50) * 0.75), 410))
        screen.blit(label_time100, (40+(width - 50), 410))

        newDataAvailable = False
        pygame.display.flip()

        loops += 1
