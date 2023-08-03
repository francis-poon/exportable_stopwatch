import tkinter as Tkinter
from datetime import datetime
import csv
import json
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

initial_count = 18000
counter = initial_count
running = False
csv_data = [0]
full_output_filename = ""

config = None
if os.path.exists('config.json'):
  f = open('config.json', 'r')
  config = json.load(f)
  f.close()
if config is None or 'output_dir' not in config or not os.path.exists(config['output_dir']):
  print("Using current dir " + os.path.dirname(os.path.realpath(__file__)) + " as output dir")
  print(os.getcwd())
  file_parent_dir = os.path.dirname(os.path.realpath(__file__)) + "\\"
else:
  file_parent_dir = config['output_dir']

def counter_label(label):
    def count():
        if running:
            global counter
   
            tt = datetime.fromtimestamp(counter)
            string = tt.strftime("%H:%M:%S")
            display=string
   
            label['text']=display   # Or label.config(text=display)
   
            # label.after(arg1, arg2) delays by 
            # first argument given in milliseconds
            # and then calls the function given as second argument.
            # Generally like here we need to call the 
            # function in which it is present repeatedly.
            # Delays by 1000ms=1 seconds and call count again.
            label.after(1000, count) 
            counter += 1
   
    # Triggering the start of the counter.
    count()     
   
# start function of the stopwatch
def Start(label):
    global running
    global csv_data
    global full_output_filename
    running=True
    counter_label(label)
    start['state']='disabled'
    stop['state']='normal'
    #export['state']='normal'
    now = datetime.now()
    full_output_filename = file_parent_dir + now.strftime("%m%d%Y.csv")
    csv_data[0] = [now.strftime("%m/%d/%Y"), now.strftime("%H:%M:%S")]
   
# Stop function of the stopwatch
def Stop():
    global running
    global counter
    global csv_data
    global full_output_filename
    start['state']='normal'
    stop['state']='disabled'
    running = False
    now = datetime.now()
    csv_data[0] += [now.strftime("%H:%M:%S"), datetime.fromtimestamp(counter-1).strftime("%H:%M:%S")]
    counter = initial_count
    
    file_mode = "w"
    if os.path.exists(full_output_filename):
      file_mode = "a"
    with open(full_output_filename, file_mode, newline='') as f:
      writer = csv.writer(f)
      writer.writerow(csv_data[0])
   
# Reset function of the stopwatch
def Reset(label):
    global counter
    counter=initial_count
   
    # If rest is pressed after pressing stop.
    if running==False:      
        reset['state']='disabled'
        label['text']='Welcome!'
   
    # If reset is pressed while the stopwatch is running.
    else:               
        label['text']='Starting...'
        
def Export():
  global csv_data
  global file_parent_dir
  global running
  
  if running:
    Stop()
    
  export['state']='disabled'
  file_name = file_parent_dir + datetime.now().strftime("%m%d%Y_%H%M%S.csv")
  with open(file_name, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
  csv_data = []
   
root = Tkinter.Tk()
root.title("Stopwatch")
   
# Fixing the window size.
root.minsize(width=250, height=70)
label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.pack()
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label))
stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)
#export = Tkinter.Button(f, text='Export',width=6, state='disabled', command=Export)
f.pack(anchor = 'center',pady=5)
start.pack(side="left")
stop.pack(side ="left")
#export.pack(side="left")
root.mainloop()