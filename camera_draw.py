import threading
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk
from flask import Flask, render_template

# How big we want the drawing array to be
xZones = 64
yZones = 64

running = True
LEDarray = [[0]*yZones for _ in range(xZones)]  # initialize empty array
drawEnable = False
color = "black"


# Camera dimensions, this is specifically for my camera and would need to be changed
    # for use with other cameras
cameraX = 640
cameraY = 480

model = YOLO("runs/detect/train3/weights/best.pt")

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

# window
window = tk.Tk()
window.geometry("800x800")
window.title("Grid")


# initialize 32x32 grid for colors, with space left on each side
def init_grid():
    print("Initializing Grid with " + str(xZones) + " columns and " + str(yZones) + " rows")
    # First row & column should not be colored and have more space
    window.columnconfigure(0, weight=int(0.2*xZones))
    window.rowconfigure(0, weight=int(0.2*yZones))
    
    for i in range(1, xZones):
        window.columnconfigure(i, weight=1)
        
    for k in range(1, yZones):
        window.rowconfigure(k, weight=1)
    
    # Last column and row should not be colored and have more space
    window.columnconfigure(xZones, weight=int(0.2*xZones))
    window.rowconfigure(yZones, weight=int(0.2*yZones))

    for i in range(yZones-1):
        for k in range(xZones-1):
            # print(str(LEDarray[i][k]), end="")
            label = ttk.Label(window, background="white")
            label.grid(row=(i+1), column=(k+1), sticky="nsew")
        # print("")


def detect():
    global LEDarray, color
    i = 0
    k = 0

    try:
        results = model.predict(source="0", show=True, stream=True, conf=0.6)

        for result in results:
            if(running == False):
                break

            for box in result.boxes:
                conf = box.conf.item()
                if (conf >= 0.6):
                    x1 = float(box.xyxy[0][0])
                    y1 = float(box.xyxy[0][1])
                    x2 = float(box.xyxy[0][2])
                    y2 = float(box.xyxy[0][3])
                    cx = (x1+x2)/2
                    cy = (y1+y2)/2
                    # print("center x: " + str(cx) + " | center y: " + str(cy))
                    draw(cx, cy)

            # print full array for testing purposes
            for i in range(yZones):
                for k in range(xZones):
                    print(str(LEDarray[i][k]), end="")
                print("")
            print("")
                      
    except Exception as e:
        print("Detect error")
        
def start_website():
    app.run(debug=True, use_reloader=False)

def draw(xPos, yPos):
    global LEDarray

    print("entered draw with xPos = " + str(xPos) + "and yPos = " + str(yPos))
    xGridPos = int((xPos/cameraX)*xZones)
    yGridPos = int((yPos/cameraY)*yZones)

    # ignore if position is in the first boxes, as those should be used for other purposes
    if(xGridPos == 0 or xGridPos >= xZones):
        return
    if(yGridPos == 0 or yGridPos >= yZones):
        return

    LEDarray[yGridPos][xGridPos] = 1
    label = ttk.Label(window, background=color)
    label.grid(row=yGridPos, column=xGridPos, sticky="nsew")


def main():
    init_grid()

    # Start object detection
    t1 = threading.Thread(target=detect, daemon=True)
    t1.start()

    # # Start website
    # t2 = threading.Thread(target=start_website, daemon=True)
    # t2.start()

    # Tkinter GUI loop
    window.mainloop()
    

if __name__ =="__main__":
    try:
        main()
    except KeyboardInterrupt:
        running = False
        print("Exiting program...")
    except Exception as e:
        running = False
        print("Unexpected error")