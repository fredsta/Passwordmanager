# Config window for the password-generator, which will be called out of passwordmanager.py

from tkinter import *

class config_window(Frame):
    def __init__(self, config, master=None):
        Frame.__init__(self, master)
        self.config = config  # List with config

        # Frames
        self.frLength = Frame(master)
        self.frLength.pack()
        self.frExtras = Frame(master)
        self.frExtras.pack()
        self.frCapitals = Frame(master)
        self.frCapitals.pack()
        self.frButton = Frame(master)
        self.frButton.pack()

        # pwlength
        self.lblPWlength = Label(self.frLength, text="Length (4-32)?")
        self.lblPWlength.pack(side=LEFT)

        self.slLength = Scale(self.frLength, from_=4, to=32, orient=HORIZONTAL)
        self.slLength.pack(side=LEFT)

        # including extra chars
        self.lblExtraChars = Label(self.frExtras, text="Include extra chars (e.g. 012%&_?)?")
        self.lblExtraChars.pack(side=LEFT)

        self.varExtra = IntVar()
        self.cbtnExtra = Checkbutton(self.frExtras, variable=self.varExtra)
        self.cbtnExtra.pack(side=LEFT)

        # including capitals
        self.lblCapitals = Label(self.frCapitals, text="Include capital Letters")
        self.lblCapitals.pack(side=LEFT)

        self.varCapitals = IntVar()
        self.cbtnCapitals = Checkbutton(self.frCapitals, variable=self.varCapitals)
        self.cbtnCapitals.pack(side=LEFT)

        # okay-button
        self.btnOkay = Button(self.frButton, text="Okay", command=self.evaluate)
        self.btnOkay.pack(side=LEFT)

    def evaluate(self):
        self.config = [self.varCapitals.get(), self.varExtra.get(), self.slLength.get()]
        print(self.config)
        self.master.destroy()  # kill the window

        

if __name__ == '__main__':
    root = Tk()
    config_window(root)
    root.mainloop()