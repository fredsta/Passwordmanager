# Passwordmanager with GUI
# Version: 19.09.2021
# author: fredsta

import time
from tkinter import *
from tkinter import messagebox, filedialog
from passwd_gen import * 
from cryptography.fernet import Fernet
from transfer import transfer

key_string, fernet = None, None

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.selection = None  # Aktuelle Auswahl in der Listbox, damit die Elemente einfacher gelöscht werden können
        self.pwdGenerator = passwd_gen()  # instanziere den Password-Generator
        self.loadedData = {}  # Dic zum temporären Speichern der Passwörter etc.
        self.firstTime = 1  # Damit eine Methode beim ersten Ausführen eine andere Funktion ausführt.

        # Menüstruktur
        #self.create_menu(master)

        menubar = Menu(master, bg="#14161B", fg="White", bd=0, activebackground="#14161B", activeforeground="#c7c7c7", activeborderwidth=0)
        
        #self.windowKill
        setupmenu = Menu(menubar, tearoff=0, fg="White", bg="#14161B", bd=0, selectcolor="Green")
        setupmenu.add_command(label="Export", command=self.export_data)
        setupmenu.add_command(label="Import", command=self.import_data)
        setupmenu.add_command(label="Show Key", command=self.show_key)

        show_password = BooleanVar()
        #show_password.set(True)
        setupmenu.add_checkbutton(label="Show password", onvalue=1, offvalue=0, variable=show_password)
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

        self.frTable = Frame(self.frMain, bg="White")  # Frame for the content
        self.frTable.pack()


        # Labels
        self.lblURL = Label(self.frURL, text="Website", font=("Arial", 12), bg="#222936", fg="white")
        self.lblURL.pack(side=LEFT, padx=10)

        self.lblUsername = Label(self.frUser, text="Username", font=("Arial", 12), bg="#222936", fg="white")
        self.lblUsername.pack(side=LEFT, padx=10)

        self.lblPassword = Label(self.frPassword, text="Password", font=("Arial", 12), bg="#222936", fg="white")
        self.lblPassword.pack(side=LEFT, padx=10)

        self.lblFurtherInf = Label(self.frTable, text="", font=("Arial",12),bg="#222936", fg="white")
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

        self.loadData()  # Bereits vorhandene Passwörter in das Textfeld laden

        # Images (labels)
        self.lens = PhotoImage(file="img/lens.png")
        self.imgLens = Label(self.frSearch, image=self.lens, bg="White")
        self.imgLens.place(x=335, y=1)


    # Live-Suche in der Listbox nach URLs
    def search_refresh(self, var):
        if self.firstTime:  # Workaround wegen der .trace Funktion im Konstruktor
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
        messagebox.showwarning("Help", "Dies ist keine Hilfe.")

    def show_key(self):
        messagebox.showinfo("Key", key_string)

    def import_data(self):
        filename = filedialog.askopenfilename()
        transfer.transfer(filename)
        self.loadData()
        messagebox.showinfo("Success", "Your passwords have been imported successfully!")

    def export_data(self):
        filename = filedialog.askdirectory() + "/pawoman_export.txt"
        transfer.export(filename)
        messagebox.showinfo("Success", "Your passwords have been exported successfully!")


    # Speichert einen neuen Eintrag im .txt, im Dictionary und schreibt die URL in das entsprechende Feld
    def saveEntry(self):
        data = []
        entries = [self.entURL, self.entUsername, self.entPassword]

        self.loadedData.update({entries[0].get():[entries[1].get(), entries[2].get()]})
        self.lbSites.insert(END, entries[0].get())

        for entry in entries:
            encrypted_data = fernet.encrypt(entry.get().encode())
            data.append(encrypted_data.decode())
            entry.delete(0, END)  

        with open(".data.txt", "a") as myFile:
            for i in range(len(data)):
                myFile.write(data[i])
            myFile.write("\n")

    
    # Generiert ein Kennwort und setzt es in das entsprechende Feld
    def generate(self):
        password = self.pwdGenerator.generate_password() # hier noch weiters Fenster mit Parameter-Auswahl öffnen
        self.entPassword.delete(0, END)
        self.entPassword.config(fg="Black")
        self.entPassword.insert(0, password)


    def more(self):  # further settings for the password-generator
        pass


    # Lädt die Daten aus dem .txt in das Dictionary und schreibt die URL in das entsprechende Feld
    def loadData(self):
        # Erhält ein String bei jeder Verschlüsselung einen unterschiedliches Ergebnis? -> Prüfen!!
        with open(".data.txt", "r") as f:
            for line in f:
                temp_url = fernet.decrypt(line[0:100].encode()).decode()
                temp_user = fernet.decrypt(line[100:200].encode()).decode()
                temp_pw = fernet.decrypt(line[200:300].encode()).decode()
                self.loadedData.update({temp_url:[temp_user, temp_pw]})
                self.lbSites.insert(END, temp_url)


    # Löscht den aktuell ausgewählten Eintrag (Passwort, User, URL)
    def deleteItem(self):
        lines = []
        if self.selection:
            index = self.selection[0]
            # Eintrag aus dem Dictionary entfernen
            key = list(self.loadedData.keys())[index]
            del self.loadedData[key]

            # Liste neu laden
            self.lbSites.delete(0, END)
            for key in self.loadedData.keys():
                self.lbSites.insert(END, key)

            # Eintrag aus dem .txt-File entfernen
            with open(".data.txt", "r") as f:
                lines = f.readlines()
            lines.pop(index)
            with open(".data.txt", "w") as f:
                for line in lines:
                    f.write(line)

        else:
            pass  # nothing else should happen


    # Callback-Funktion, wenn ein Element der Listbox ausgewählt wird.
    def lbSelect(self, event):
        self.selection = event.widget.curselection()
        if self.selection:
            linked_password = self.loadedData.get(event.widget.get(self.selection[0]))[1]
            linked_username = self.loadedData.get(event.widget.get(self.selection[0]))[0]
            self.lblFurtherInf.config(text=linked_username)

            # Passwort ins Clipboards schieben - nur verfügbar solange das Programm läuft.
            master.clipboard_clear()
            master.clipboard_append(linked_password)
            master.update()

    def FocusIn(self, event):
        event.widget.delete(0, END)
        event.widget.insert(0, "")
        event.widget.config(fg="Black")


# Kümmert sich um Konfigurationen etc.
def startup():
    global key_string, fernet
    try:   
        with open(".config", "r") as f: # Wenn das file existiert, kann der Key eingelesen werden.
            key_string = f.readlines()[0].strip("\n")

    except FileNotFoundError:
        with open(".config", "w") as f:
            # Neuen key generieren
            key_string = Fernet.generate_key().decode()
            f.write(key_string)

        with open(".data.txt", "w") as q:  # erstellt das Passwort-File
            pass
    
    key = key_string.encode()
    fernet = Fernet(key)


if __name__ == '__main__':
    startup()
    master = Tk()
    photo = PhotoImage(file="img/lockdark.png")
    master.iconphoto(False, photo)

    #master.withdraw() --> versteckt das Fenster
    master.geometry("500x500")
    master.title("Password-Manager")
    app = Application(master)
    
    app.mainloop()


# Passwortgenerator mit einbauen: Teilweise erledigt
# Optische Gestaltung verbessern

# Als .pyw speichern, um keine Konsole zu öffnen

# evtl. ne .exe draus bauen, damit man es auf anderen Geräte auch verwenden kann?

# Für verschiedene Rechner eine Funktion schreiben, wo man den "alten" key eingeben kann
# und dann wird der Inhalt aus der .txt-Datei auf den neuen Key umgekrypted...

# Ne Art Installation-Manger basteln, damit man das 'frisch' nutzen kann?!

# Wegen der unterschiedlichen Länge: Einfach alles mit Leerzeichen strecken?

# Idiotensicher machen.nice
# 