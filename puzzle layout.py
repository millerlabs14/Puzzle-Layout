import tkinter as tk

class App:
   def __init__(self):
      self.clicks = 0
      self.convx  = 0
      self.convy  = 0
      
      #Window
      self.root = tk.Tk()
      self.root.geometry("{}x{}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))   #Full Screen
      self.root.resizable(False,False)

      #Picture
      self.picture = tk.PhotoImage(file = 'Puzzle.gif')

      #Canvas
      self.canvas = tk.Canvas(self.root, width = self.picture.width(), height = self.picture.height())
      self.canvas.grid(rowspan = 5,row = 0, column = 0)
      self.canvas.create_image(0,0, image = self.picture, anchor = "nw")

      #Labels
      self.coords = tk.StringVar()
      self.coords.set("Coordinates: ")
      self.xlabel = tk.Label(self.root, textvariable = self.coords, font=("Helvetica", 20))
      self.xlabel.grid(row = 0, column = 1, sticky = "nw")

      self.measurements = tk.StringVar()
      self.measurements.set("Measurements:")
      self.measurement_label = tk.Label(self.root, textvariable = self.measurements, font=("Helvetica", 20))
      self.measurement_label.grid(row = 3, column = 1, sticky = "sw")

      #Lines
      self.xline  = self.canvas.create_line(0,0,0,0, fill = "yellow", width = 1)
      self.canvas.itemconfigure(self.xline, state = "hidden")                    #initially only vertical line should show
      self.yline  = self.canvas.create_line(0,0,0,0, fill = "yellow", width = 1)
      self.vmark1 = self.canvas.create_line(0,0,0,0, fill = "white", width = 2)
      self.vmark2 = self.canvas.create_line(0,0,0,0, fill = "white", width = 2)
      self.hmark1 = self.canvas.create_line(0,0,0,0, fill = "white", width = 2)
      self.hmark2 = self.canvas.create_line(0,0,0,0, fill = "white", width = 2)

      #Bindings
      self.canvas.bind('<Motion>', self.motion)
      self.canvas.bind('<Button-1>', self.click)

      self.root.update()

   def convert(self, x):
      offset = 5  #ignore white around edges
      pixels = x - offset

      conversion = (self.picture.width() - (2 * offset)) / 108.5
      inches = pixels / conversion

      return round(inches, 1)
      

   def motion(self, event):
      #Get mouse coordinates
      pic_width = self.picture.width() 
      pic_height = self.picture.height()
      x, y = event.x, event.y

      #Draw indicator lines
      self.canvas.coords(self.xline,0,y,1100,y)
      self.canvas.coords(self.yline,x,0,x,720)

      #Adjust x and y to change side measurements are taken from
      if x >= (pic_width / 2) and y < (pic_height / 2):     #Top Right
         x = pic_width - x
      elif x >= (pic_width / 2) and y >= (pic_height / 2):  #Bottom Right
         y = pic_height - y
         x = pic_width - x
      elif x < (pic_width / 2) and y >= (pic_height / 2):   #Bottom Left
         y = pic_height - y
      else:                                                 #Top Left
         #Do not change x or y
         pass
         
      #Update measurment display
      x, y = self.convert(x), self.convert(y)
      self.convx, self.convy = x, y
      
      self.coords.set("Coordinates: {}\" x {}\"".format(x,y))

   def click(self, event):
      self.clicks += 1
      x, y = event.x, event.y

      if self.clicks == 1:    #1 click:  vertical line 1-------
         self.canvas.coords(self.vmark1,x,0,x,720)
         self.canvas.itemconfigure(self.vmark1, state = "normal") 
         self.measurements.set(self.measurements.get() + "\nL-R:\t{}\"".format(self.convx))
      elif self.clicks == 2:  #2 clicks: vertical line 2-------
         self.canvas.coords(self.vmark2,x,0,x,720)
         self.canvas.itemconfigure(self.vmark2, state = "normal") 
         self.canvas.itemconfigure(self.xline,  state = "normal")
         self.canvas.itemconfigure(self.yline,  state = "hidden")
         self.measurements.set(self.measurements.get() + "\nL-R:\t{}\"".format(self.convx))
      elif self.clicks == 3:  #3 clicks: horizontal line 1-----
         self.canvas.coords(self.hmark1,0,y,1100,y)
         self.canvas.itemconfigure(self.hmark1, state = "normal")
         self.measurements.set(self.measurements.get() + "\n\nT-B:\t{}\"".format(self.convy))
      elif self.clicks == 4:  #4 clicks: horizontal line 2-----
         self.canvas.coords(self.hmark2,0,y,1100,y)
         self.canvas.itemconfigure(self.hmark2, state = "normal")
         self.canvas.itemconfigure(self.xline,  state = "hidden")
         self.measurements.set(self.measurements.get() + "\nT-B:\t{}\"".format(self.convy))
      else:                   #5 clicks: reset-----------------
         self.clicks = 0
         self.canvas.itemconfigure(self.vmark1, state = "hidden")
         self.canvas.itemconfigure(self.vmark2, state = "hidden")
         self.canvas.itemconfigure(self.hmark1, state = "hidden")
         self.canvas.itemconfigure(self.hmark2, state = "hidden")
         self.canvas.itemconfigure(self.xline,  state = "hidden")
         self.canvas.itemconfigure(self.yline,  state = "normal")
         self.measurements.set("Measurements:")
         

      

window = App()
