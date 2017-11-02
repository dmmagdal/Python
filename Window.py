"""
    Property of CR Capital, LLC. All rights reserved.
    Author: Diego Magdaleno
"""

import tkinter as tinker
from tkinter import ttk


class Page(tinker.Tk):																# take any sort of inheritance
	# method upon initialization
    def __init__(self, *args, **kwargs):
        tinker.Tk.__init__(self, *args, **kwargs)
        tinker.Tk.iconbitmap(self, default="CRC_Logo.ico")							# set icon
        tinker.Tk.wm_title(self, "Ratings Trader")									# set title
        container = tinker.Frame(self, width=500, height=500)						# create new frame of size 500 x 500
        #container.pack(side="top", fill="both", expand=True)						# pack the container (frame) to the top and fill in the whites space and does not expand
        container.grid(row=0, column=0)


        container.grid_rowconfigure(0, weight=1)									# configures rows in grid in tkinter. 0 is the size and weight (priority) is 1
        container.grid_columnconfigure(0, weight=5)

        
        self.frames = {}															# dictionary to hold the frames

        for f in (Page1, Page2, Page3, Page4, Page5, Page6):						# iterate through the pages
        	frame = f(container, self)												 
        	self.frames[f] = frame
        	frame.grid(row = 0, column = 0, sticky="nsew")							# create a new grid for the frame 
        self.show_frame(Page1)														# shows the frame Page1

    # method to bring a frame up to the front of the framse dictionary
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Page1(tinker.Frame):
    def __init__(self, parent, controller):
        tinker.Frame.__init__(self, parent)
        title = tinker.Label(self, text="Welcome to the Ratings Trading desktop app!", font=("Helvetica", 22))
        #title.pack(pady=10, padx=10)
        title.grid(row=0, column=6)													# use grid() over pack for better placement
        body = tinker.Label(self, text = "To use, have the brokerage desktop app open simultaneously with this one.", font=("Helvetica", 12))
        body.grid(row=1, column=6)
        # button to next frame
        nextButton = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Page2))
        nextButton.grid(row=3, column=6)


class Page2(tinker.Frame):
    def __init__(self, parent, controller):
        tinker.Frame.__init__(self, parent)
        title = tinker.Label(self, text="Please select your brokerage:", font=("Helvetica", 22))
        title.pack(pady=10, padx=10)
        # list of brokerages (only IB is available at this) using radiobuttons
        v = tinker.IntVar()
        v.set(1)
        Brokers = [("Interactive Brokers", 1),("More Borkerages coming soon", 2)]
        for text, mode in Brokers:
        	rb = tinker.Radiobutton(self, text=text, variable=v, value=mode)
        	rb.pack()
        # button to next frame
        nextButton = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Page3))
        nextButton.place(x=415, y=450)
        nextButton.pack( padx=10, pady=10, side="right")
        # button to previous frame
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page1))
        backButton.place(x=50, y=450)
        backButton.pack(padx=10, pady=10, side="left")


class Page3(tinker.Frame):
    def __init__(self, parent, controller):
        tinker.Frame.__init__(self, parent)
        title = tinker.Label(self, text="Now, select the credit agency you would like to trade ratings off of:", font=("Helvetica", 22))
        title.pack(pady=10, padx=10)
        # list of credit agencies (again using radio buttons)
        v = tinker.IntVar()
        v.set(1)
        Brokers = [("Moody's", 1),("S&P", 2)]
        for text, mode in Brokers:
        	rb = tinker.Radiobutton(self, text=text, variable=v, value=mode)
        	rb.pack()
        # button to next frame
        nextButton = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Page4))
        nextButton.place(x=415, y=450)
        nextButton.pack(padx=10, pady=10, side="right")
        # button to previous frame
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page2))
        backButton.place(x=50, y=450)
        backButton.pack(padx=10, pady=10, side="left")


class Page4(tinker.Frame):
    def __init__(self, parent, controller):
        tinker.Frame.__init__(self, parent)
        title = tinker.Label(self, text="Here are the securities and upgrades/downgrades:", font=("Helvetica", 22))
        title.pack(pady=10, padx=10)
        # list of securities and upgrades/downgrades
        """
        securitiesListBox = tinker.Listbox(self)
        securitiesListBox.pack()
        for item in ["Stocks"]:
        	securitiesListBox.insert(END, item)											# insert item in the list into the listbox at the END
		"""

        # button to next frame
        nextButton = ttk.Button(self, text="Next", command=lambda: controller.show_frame(Page5))
        nextButton.place(x=415, y=450)
        nextButton.pack(padx=10, pady=10, side="right")
        # button to previous frame
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page3))
        backButton.place(x=50, y=450)
        backButton.pack(padx=10, pady=10, side="left")


class Page5(tinker.Frame):
    def __init__(self, parent, controller):
        tinker.Frame.__init__(self, parent)
        title = ttk.Label(self, text="Select the amount of shares you'd like to buy/sell:", font=("Helvetica", 22))
        title.pack(pady=10, padx=10)
        #number of shares to buy/sell
        label = tinker.Label(self, text="Number of shares:", font=("Helvetica", 12))
        label.pack()
        numberOfShares = ttk.Entry(self)
        numberOfShares.pack(side="top")
        # button to previous frame
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page4))
        backButton.place(x=50, y=450)
        backButton.pack(padx=10, pady=10, side="left")
        # button to print final message
        finishButton = ttk.Button(self, text="Finish", command=lambda: controller.show_frame(Page6))
        finishButton.place(x=50, y=450)
        finishButton.pack(padx=10, pady=10, side="right")


class Page6(tinker.Frame):
	def __init__(self, parent, controller):
		tinker.Frame.__init__(self, parent)
		title = ttk.Label(self, text="Thank you for using the Ratings Trading desktop app! In order to ensure that this application works, please keep it running in the background. You can track historicals here.", font=("Helvetica", 12))
		title.pack(pady=10, padx=10)
		# button to previous frame
		backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Page5))
		backButton.place(x=50, y=450)
		backButton.pack(padx=10, pady=10, side="left")


app = Page()
app.geometry("750x500")
app.mainloop()