# from tkinter import *

# root = Tk()

# # myLabel1 = Label(root, text="Hello World!")
# # myLabel2 = Label(root, text="awe aw asdfwe asefew")
# # myLabel1.grid(row=0, column=0)
# # myLabel2.grid(row=1, column=0)

# e = Entry(root, width=20, font=('Helvetica', 12))
# e.pack()

# def myClick():
# 	hello = "Hello " + e.get()
# 	myLabel = Label(root, text=hello)
# 	myLabel.pack()


# myButton= Button(root, text="btn", padx=30, command=myClick)
# myButton.pack()


# root.mainloop()



import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

   
Data1 = {'Country': ['US','CA','GER','UK','FR'],
        'GDP_Per_Capita': [45000,42000,52000,49000,47000]
       }

df1 = DataFrame(Data1, columns= ['Country', 'GDP_Per_Capita'])
df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()


root= tk.Tk() 
  

figure1 = plt.Figure(figsize=(6,5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1.plot(kind='bar', legend=True, ax=ax1)
ax1.set_title('Country Vs. GDP Per Capita')

root.mainloop()