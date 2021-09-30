# Passwordmanager with tkinter-GUI
# Version: 30.09.2021
# author: fredsta

import time
from tkinter import *
from tkinter import messagebox, filedialog
from passwd_gen import * 
from cryptography.fernet import Fernet
from transfer import transfer

key_string, fernet = None, None

# Class for the whole application
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.selection = None               # for the listbox
        self.pwdGenerator = passwd_gen()    # create instance of the passwordgenerator
        self.loadedData = {}                # the decrypted data will be loaded into a dictionary
        self.firstTime = 1                  # bootflag for one function
        self.config = [1, 1, 16]            # Generator config

        # config menubar
        menubar = Menu(master, bg="#14161B", fg="White", bd=0, activebackground="#14161B", activeforeground="#c7c7c7", activeborderwidth=0)
        
        setupmenu = Menu(menubar, tearoff=0, fg="White", bg="#14161B", bd=0, selectcolor="Green")
        setupmenu.add_command(label="Export", command=self.export_data)
        setupmenu.add_command(label="Import", command=self.import_data)
        setupmenu.add_command(label="Show Key", command=self.show_key)
        setupmenu.add_command(label="Config Generator", command=self.config_generator)

        self.show_password = BooleanVar()
        setupmenu.add_checkbutton(label="Show password", onvalue=1, offvalue=0, variable=self.show_password)
        menubar.add_cascade(label="Setup", menu = setupmenu)

        helpmenu = Menu(menubar, tearoff=0, fg="White", bg="#14161B", bd=0)
        helpmenu.add_command(label="Quit", command=self.windowKill)
        helpmenu.add_command(label="About", command=self.about)
        helpmenu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu = helpmenu)

        master.config(menu = menubar)
        master.config(bg="#222936")

        # Frame for general Size etc.
        self.frMain = Frame(master, width=800, height=600, bg="#222936")
        self.frMain.pack()

        self.frForm = Frame(self.frMain, bg="#222936")
        self.frForm.pack(pady=20)

        self.frURL = Frame(self.frForm, width=800, height=200, bg="#222936")
        self.frURL.pack(anchor=E)

        self.frUser = Frame(self.frForm, width=800, height=200, bg="#222936")
        self.frUser.pack(pady=10, anchor=E)

        self.frPassword = Frame(self.frForm, width=800, height=200, bg="#222936")
        self.frPassword.pack(anchor=E)

        self.frButtons = Frame(self.frMain, width=800, height=200, bg="#222936")
        self.frButtons.pack(pady=10)

        self.frSearch = Frame(self.frMain)  # Frame for the searchbar and the lens-picture
        self.frSearch.pack()

        self.frTable = Frame(self.frMain, bg="#222936")  # Frame for the content
        self.frTable.pack()


        # Labels
        self.lblURL = Label(self.frURL, text="Website", font=("Arial", 12), bg="#222936", fg="white")
        self.lblURL.pack(side=LEFT, padx=10)

        self.lblUsername = Label(self.frUser, text="Username", font=("Arial", 12), bg="#222936", fg="white")
        self.lblUsername.pack(side=LEFT, padx=10)

        self.lblPassword = Label(self.frPassword, text="Password", font=("Arial", 12), bg="#222936", fg="white")
        self.lblPassword.pack(side=LEFT, padx=10)

        self.lblFurtherInf = Label(self.frTable, text="", font=("Arial",12),bg="#222936", fg="white", highlightbackground="White", highlightcolor="White", highlightthickness=2)
        self.lblFurtherInf.pack(side=BOTTOM, padx=2, pady=2, fill=BOTH)

        # Buttons
        self.imgAdd = PhotoImage(file="img/add.png")
        self.btnAdd = Button(self.frButtons, image=self.imgAdd, command=self.saveEntry, bd=0, relief=FLAT, bg="#222936", highlightbackground="#222936", activebackground="#222936")
        self.btnAdd.pack(side=LEFT)

        self.imgGenerate = PhotoImage(file="img/generate.png")
        self.btnGenPwd = Button(self.frButtons, image=self.imgGenerate, command=self.generate, bd=0, relief=FLAT, bg="#222936", highlightbackground="#222936", activebackground="#222936")
        self.btnGenPwd.pack(side=LEFT)

        self.imgDelete = PhotoImage(file="img/delete.png")
        self.btnDelete = Button(self.frButtons, image=self.imgDelete, command=self.deleteItem, bd=0, relief=FLAT, bg="#222936", highlightbackground="#222936", activebackground="#222936")
        self.btnDelete.pack(side=LEFT)

        # Entrys
        self.entURL = Entry(self.frURL, font=("Arial",12), fg="#878787", relief=FLAT)
        self.entURL.pack(side=LEFT, padx=10)
        self.entURL.insert(0, "Website")
        self.entURL.bind("<FocusIn>", self.FocusIn)

        self.entUsername = Entry(self.frUser, font=("Arial",12), fg="#878787", relief=FLAT)
        self.entUsername.pack(side=LEFT, padx=10)
        self.entUsername.insert(0, "Username")
        self.entUsername.bind("<FocusIn>", self.FocusIn)

        self.entPassword = Entry(self.frPassword, font=("Arial",12), fg="#878787", relief=FLAT)
        self.entPassword.pack(side=LEFT, padx=10)
        self.entPassword.insert(0, "Password")
        self.entPassword.bind("<FocusIn>", self.FocusIn)        

        # Listboxes
        self.lbSites = Listbox(self.frTable, font=("Arial",12), width=40, relief=FLAT, bd=1)
        self.lbSites.pack(side=BOTTOM)
        self.lbSites.bind("<<ListboxSelect>>", self.lbSelect)

        var = StringVar()
        var.trace("w", lambda name, index, mode, var=var: self.search_refresh(var))

        self.entSearch = Entry(self.frSearch, font=("Arial",13), fg="#878787", textvariable=var, borderwidth=0, width=36)
        self.entSearch.pack(side=LEFT)
        self.entSearch.insert(0, "Suche...")
        self.entSearch.bind("<FocusIn>", self.FocusIn)

        self.loadData()  # loads already existing passwords into the listbox

        # Images (labels)
        self.lens = PhotoImage(file="img/lens.png")
        self.imgLens = Label(self.frSearch, image=self.lens, bg="White")
        self.imgLens.place(x=335, y=1)

    # live-search for entries in the listbox
    def search_refresh(self, var):
        if self.firstTime:  # Workaround because of .trace function in constructor
            self.firstTime = 0
        else:
            self.lbSites.delete(0, END)
            content = var.get()
            for key in self.loadedData.keys():
                if key.find(content) != -1:
                    self.lbSites.insert(END, key)


    def windowKill(self):
        master.destroy()

    def about(self):
        messagebox.showinfo("About", "Password-Manager created by fredsta")

    def show_help(self):
        messagebox.showwarning("Help", "This is no help.")

    def show_key(self):
        messagebox.showinfo("Key", key_string)

    def import_data(self):
        filename = filedialog.askopenfilename()
        if len(filename) == 0:
            return
        try:
            transfer.transfer(filename)
            self.loadData()
        except Exception as e:
            messagebox.showerror("Import failed!", "That didn't work :(")
            print("Error!", str(e))
            return
        messagebox.showinfo("Success", "Your passwords have been imported successfully!")

    def export_data(self):
        filename = filedialog.askdirectory() + "/pawoman_export.txt"
        try:
            transfer.export(filename)
        except Exception as e:
            print("ERROR!", str(e))
            messagebox.showerror("Failed", "Export failed!")
        messagebox.showinfo("Success", "Your passwords have been exported successfully!")


    # Saves a new data-packet into the dictionary and to the .data.txt file
    def saveEntry(self):
        data = []
        entries = [self.entURL, self.entUsername, self.entPassword]
        for entry in entries:  # Catch user-input-errors
            if entry.get() == "" or entry.get() == "Website" or entry.get() == "Username" or entry.get() == "Password":
                messagebox.showerror("Error", "Please fill in all entries")
                return
            else:
                for key in self.loadedData:
                    if entry.get() == key:
                        messagebox.showerror("Error", "This Website/Service already has an entry in the list.")
                        return
        self.loadedData.update({entries[0].get():[entries[1].get(), entries[2].get()]})
        self.lbSites.insert(END, entries[0].get())

        for entry in entries:
            encrypted_data = fernet.encrypt(entry.get().encode())
            data.append(encrypted_data.decode())
            entry.delete(0, END)  

        with open(".data.txt", "a") as myFile:
            for i in range(len(data)):
                myFile.write(data[i]+"|")
            myFile.write("\n")

    
    #  Generates a random password and puts it into the passwordfield
    def generate(self):
        length = self.config[2]
        extras = self.config[1]
        capitals = self.config[0]
        password = self.pwdGenerator.generate_password(length, capitals, extras) # Paste other config which was modified with the toplevel-window
        self.entPassword.delete(0, END)
        self.entPassword.config(fg="Black")
        self.entPassword.insert(0, password)


    # Opens a new toplevel window to let the user configure the passwordgenerator
    def config_generator(self):
        self.wSettings = Toplevel(master)
        self.wSettings.title("Setup generator")

         # Frames
        self.frLength = Frame(self.wSettings, bg="#222936")
        self.frLength.pack()
        self.frExtras = Frame(self.wSettings, bg="#222936")
        self.frExtras.pack()
        self.frCapitals = Frame(self.wSettings, bg="#222936")
        self.frCapitals.pack()
        self.frButton = Frame(self.wSettings, bg="#222936")
        self.frButton.pack()

        # pwlength
        self.lblPWlength = Label(self.frLength, text="Length (4-32)?", font=("Arial", 12), bg="#222936", fg="white")
        self.lblPWlength.pack(side=LEFT, pady=10, padx=10)

        self.slLength = Scale(self.frLength, from_=4, to=32, orient=HORIZONTAL, bg="#222936", fg="White", borderwidth=0, troughcolor="White", relief=FLAT, cursor="arrow")
        self.slLength.pack(side=LEFT, pady=10, anchor=E)
        self.slLength.set(16)

        # including extra chars
        self.lblExtraChars = Label(self.frExtras, text="Include extra chars (e.g. 012%&!_)  ", font=("Arial", 12), bg="#222936", fg="white")
        self.lblExtraChars.pack(side=LEFT, pady=10)

        self.varExtra = IntVar()
        self.varExtra.set(True)
        self.cbtnExtra = Checkbutton(self.frExtras, variable=self.varExtra, bg="#222936", activebackground="#222936", selectcolor="White", fg="Green")
        self.cbtnExtra.pack(side=LEFT, pady=10)

        # including capitals
        self.lblCapitals = Label(self.frCapitals, text="Include capital Letters  ", font=("Arial", 12), bg="#222936", fg="white")
        self.lblCapitals.pack(side=LEFT, pady=10)

        self.varCapitals = IntVar()
        self.varCapitals.set(True)
        self.cbtnCapitals = Checkbutton(self.frCapitals, variable=self.varCapitals, bg="#222936", activebackground="#222936", fg="Green")
        self.cbtnCapitals.pack(side=LEFT, pady=10)

        # okay-button
        self.btnOkay = Button(self.frButton, text="Okay", command=self.evaluate, font=("Arial", 12), bg="#222936", fg="white", activebackground="White", activeforeground="#222936")
        self.btnOkay.pack(side=LEFT, pady=10)

        self.wSettings.geometry("300x200")
        self.wSettings.config(bg="#222936")


    # collect the settings from the toplevel window
    def evaluate(self):
        self.config = [self.varCapitals.get(), self.varExtra.get(), self.slLength.get()]
        print(self.config)
        self.wSettings.destroy()  # kills the window


    # loads data from .data.txt and puts them into the right place
    def loadData(self):
        with open(".data.txt", "r") as f:
            for line in f:
                separators, index = [], 0
                for i in range(2):
                    index = line.find("|", index)
                    separators.append(index)
                    index += 1
                temp_url = fernet.decrypt(line[0:separators[0]].encode()).decode()
                temp_user = fernet.decrypt(line[separators[0]:separators[1]].encode()).decode()
                temp_pw = fernet.decrypt(line[separators[1]:].encode()).decode()
                self.loadedData.update({temp_url:[temp_user, temp_pw]})
                self.lbSites.insert(END, temp_url)


    # clears the current selected entry out of .data.txt (and the dictionary)
    def deleteItem(self):
        lines = []
        if self.selection:
            index = self.selection[0]
            # Remove from dictionary
            key = list(self.loadedData.keys())[index]
            del self.loadedData[key]

            # reload listbox-entries
            self.lbSites.delete(0, END)
            for key in self.loadedData.keys():
                self.lbSites.insert(END, key)

            # Remove entry from .data.txt
            with open(".data.txt", "r") as f:
                lines = f.readlines()
            lines.pop(index)
            with open(".data.txt", "w") as f:
                for line in lines:
                    f.write(line)
        else:
            messagebox.showerror("Error", "Nothing selected to delete.")


    # Callback function if an element in the listbox gets selected
    def lbSelect(self, event):
        self.selection = event.widget.curselection()
        if self.selection:
            linked_password = self.loadedData.get(event.widget.get(self.selection[0]))[1]
            linked_username = self.loadedData.get(event.widget.get(self.selection[0]))[0]
            text_to_show = linked_username
            if self.show_password.get() == 1:  # Also shows the password when the checkbox is checked
                text_to_show += ": " + linked_password
            self.lblFurtherInf.config(text=text_to_show)

            # Paste the password into the clipboard, only accessible while the programm's running
            master.clipboard_clear()
            master.clipboard_append(linked_password)
            master.update()

    def FocusIn(self, event):
        event.widget.delete(0, END)
        event.widget.insert(0, "")
        event.widget.config(fg="Black")


# cares about config etc.
def startup():
    global key_string, fernet, generator_config
    try:   
        with open(".config", "r") as f:     # the key can be read if the file exists
            key_string = f.readlines()[0].strip("\n")

    except FileNotFoundError:
        with open(".config", "w") as f:
            # generate new key
            key_string = Fernet.generate_key().decode()
            f.write(key_string)

        with open(".data.txt", "w") as q:  # creates a password file
            pass
    
    key = key_string.encode()
    fernet = Fernet(key)


# main 
if __name__ == '__main__':
    startup()
    master = Tk()
    photo = PhotoImage(file="img/lockdark.png")
    master.iconphoto(False, photo)

    master.geometry("500x500")
    master.title("Password-Manager")
    app = Application(master)
    
    app.mainloop()