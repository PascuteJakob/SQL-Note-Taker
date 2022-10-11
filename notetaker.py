import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import themed_tk as tk
import customtkinter
from datetime import date

# Create database connection and connect to table
try:
        con = sql.connect('notes_db.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE notes_table (section text, date text, notes_title text, notes text)''')
except:
        print("Database Connection Successful")

# Insert a row of data
def add_notes():
        global t

        todayDate = date.today()
        today = todayDate.strftime("%m/%d/%y")
        #t.pack_forget()
        #Get input values
        window = customtkinter.CTkInputDialog(master=None, text = "Section:", title="Add A Note")
        section = window.get_input()
        window2 = customtkinter.CTkInputDialog(master=None, text = "Title:", title="Add A Note")
        notes_title = window2.get_input()
        #section = section_entry.get()
        #today = date_entry.get()
        #notes_title = notes_title_entry.get()
        #notes = notes_entry.get()
        #Raise a prompt for missing values
        notes = ""
        if (len(section) <= 0) & (len(today) <= 0) & (len(notes_title) <= 0): #& (len(notes) <= 1):
                #messagebox.showerror(message="Enter The Required Fields")
                print('yeet')
        else:
        #Insert into the table
                cur.execute("INSERT INTO notes_table VALUES ('%s','%s','%s','%s')" % (section, today, notes_title, notes))
                messagebox.showinfo(message="Note added")
        #Commit to preserve the changes
                con.commit()
        update_listbox("add_notes")

#Display all the notes
def view_notes():
        #Obtain all the user input
        date = date_entry.get()
        notes_title = notes_title_entry.get()

        #Execute the query
        get_notes = cur.execute("SELECT * FROM notes_table")
        #Obtain all the contents of the query
        rows = cur.fetchall()
        #Check if none was retrieved
        if len(rows) <= 0:
                messagebox.showerror(message="No notes found")
        else:
                #Print the notes
                get_notes = cur.execute("SELECT * FROM notes_table")
                e = Label(GUI, width=10, text='Section', borderwidth = 2, relief='raised', anchor='center', bg='grey')
                e.grid(row=0, column=0)
                e = Label(GUI, width=10, text='Date', borderwidth = 2, relief='raised', anchor='center', bg='grey')
                e.grid(row=0, column=1)
                e = Label(GUI, width=10, text='Title', borderwidth = 2, relief='raised', anchor='center', bg='grey')
                e.grid(row=0, column=2)
                e = Label(GUI, width=10, text='Note', borderwidth = 2, relief='raised', anchor='center', bg='grey')
                e.grid(row=0, column=3)
                i = 1
                for row in get_notes:
                        #messagebox.showinfo(message="Date: "+row[0]+"\nTitle: "+row[1]+"\nNotes: "+row[2])
                    for j in range(len(row)):
                        #messagebox.showinfo(message=)
                        e = Label(GUI, width=10, text=row[j], borderwidth=2, relief='ridge', anchor='center')
                        e.grid(row=i, column=j)
                    i += 1

#Delete the notes
def delete_notes():
        #Obtain input values & format correctly

        index = lb1.curselection()
        data = lb1.get(index, index)
        dataList = list(data)
        dataStr = ','.join(dataList)
        dataFormatted = dataStr.split(', ')
        #Obtain user input
        section = dataFormatted[0]
        today = dataFormatted[1]
        notes_title = dataFormatted[2]
        #Ask if user wants to delete all notes
        #choice = messagebox.askquestion(message="Are you sure you want to delete all notes?")
        #If yes is selected, delete all

        sql_statement = "DELETE FROM notes_table where section ='%s' and date ='%s' and notes_title ='%s'" % (section, today, notes_title)
        cur.execute(sql_statement)
        con.commit()
        messagebox.showinfo(message="Note Deleted")
        update_listbox("delete_notes")

#Update the notes
def update_notes():
        index = lb1.curselection()
        data = lb1.get(index, index)
        dataList = list(data)
        dataStr = ','.join(dataList)
        dataFormatted = dataStr.split(', ')
        #Obtain user input
        section = dataFormatted[0]
        today = dataFormatted[1]
        notes_title = dataFormatted[2]
        notes = t.get("1.0", 'end')

        sql_statement = "UPDATE notes_table SET notes = '%s' where section = '%s' and date ='%s' and notes_title ='%s'" % (notes, section, today, notes_title)

        cur.execute(sql_statement)
        messagebox.showinfo(message="Note Updated")
        con.commit()

#Invoke call to class to view a window
#GUI = Tk()
#GUI = tk.ThemedTk()
#GUI.get_themes()
#GUI.set_theme("blue")
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

GUI = customtkinter.CTk()
GUI.geometry("1000x600")
#Set dimensions of window and title
GUI.title("MindMap")
#GUI.iconbitmap('D:\Code\Senior Capstone\MindMap\MindMap\pad.ico')

greeting = customtkinter.CTkLabel(GUI, text="Map Your Mind")
greeting.place(x=340, y=0)
#Read inputs
#Section Input
section_label = customtkinter.CTkLabel(GUI, text="Section:")
section_label.place(x = 535, y = 40)
section_entry = customtkinter.CTkEntry(GUI, width=400)
section_entry.place(x = 580, y = 70)

#Date Input
date_label = customtkinter.CTkLabel(GUI, text="Date:")
date_label.place(x = 525, y = 105)
date_entry = customtkinter.CTkEntry(GUI, width=400)
date_entry.place(x = 580, y = 135)

#Notes Title Input
notes_title_label = customtkinter.CTkLabel(GUI, text="Title:")
notes_title_label.place(x = 525, y = 170)
notes_title_entry = customtkinter.CTkEntry(GUI, width=400)
notes_title_entry.place(x = 580, y = 200)

#Notes Input
notes_label = customtkinter.CTkLabel(GUI, text="Note:")
notes_label.place(x = 525, y = 235)
notes_entry = customtkinter.CTkEntry(GUI, width=400, height=100)
notes_entry.place(x = 580, y = 268)

#Perform Notes Functions
button1 = customtkinter.CTkButton(GUI, text='Add Note', command=add_notes).place(x = 38, y = 560)
#button2 = customtkinter.CTkButton(GUI, text='View Notes', command=view_notes).place(x=325, y=500)
button3 = customtkinter.CTkButton(GUI, text='Delete Note(s)', command=delete_notes).place(x = 630, y = 560)
button4 = customtkinter.CTkButton(GUI, text='Update Note', command=update_notes).place(x=400, y=560)
button5 = customtkinter.CTkButton(GUI, text='Close MindMap', command=GUI.destroy).place(x = 858, y = 560)

def create_listbox():
        frame = customtkinter.CTkFrame(GUI, width = 30)
        frame.pack(anchor='nw', side=LEFT)

        global lb1
        lb1 = Listbox(frame, height=28, width=30, bg = '#212224',fg = 'white',font = 'Arial',
                      relief='flat', borderwidth=10, highlightcolor='#275EB2', highlightbackground='#275EB2', cursor='spraycan')
        sb = Scrollbar(frame, orient=VERTICAL, bg = '#212224')
        sb.pack(fill='y', side='left')
        lb1.configure(yscrollcommand=sb.set, exportselection=False)
        sb.config(command=lb1.yview)


        #Obtain all the user input
        date = date_entry.get()
        notes_title = notes_title_entry.get()

        #Execute the query
        get_notes = cur.execute("SELECT * FROM notes_table")
        #Obtain all the contents of the query
        rows = cur.fetchall()

        #test = str(rows[0][0])
        #test = test.replace("{", "").replace("}", "")
        #print(test)
        #Check if none was retrieved
        if len(rows) <= 0:
                lb1.pack(anchor='w', side='right')
                messagebox.showerror(message="No notes found")
        else:
                for i in range(len(rows)):
                        #print(rows[i])
                        rowString = str(rows[i][0]) + ', ' + str(rows[i][1]) + ', ' + str(rows[i][2])
                        lb1.insert(i, rowString)
                lb1.pack(anchor='w', side='right')
                con.commit()
def update_listbox(case):
        global lb1
        size = lb1.size()

        #Obtain all the user input
        date = date_entry.get()
        notes_title = notes_title_entry.get()

        #Execute the query
        get_notes = cur.execute("SELECT * FROM notes_table")
        #Obtain all the contents of the query
        rows = cur.fetchall()

        dataSize = len(rows) - size

        #Check if none was retrieved
        if case == "add_notes":
                if len(rows) <= 0:
                        messagebox.showerror(message="No notes found")
                else:
                        #print(rows[-1:])
                        rowString = str(rows[-1][0]) + ', ' + str(rows[-1][1]) + ', ' + str(rows[-1][2])
                        lb1.insert(size + 1, rowString)
        elif case == "delete_notes":
                index = lb1.curselection()
                lb1.delete(index)


def createTextBox():
        frame = customtkinter.CTkFrame(GUI)
        frame.pack(anchor='e')

        sb = Scrollbar(frame, orient=VERTICAL, bg='#212224')
        sb.pack(fill='y', side='right')
        global t
        t = Text(frame, width=92, height=26, bg = '#212224', fg='white', borderwidth='0', font='arial')
        t.pack(anchor='center', side='left')

        t.configure(yscrollcommand=sb.set, insertbackground='white')
        sb.config(command=lb1.yview)

def onselect(evt):
        global t
        t.delete("1.0", 'end')
        w = evt.widget
        selected = w.curselection()
        if isinstance(w, Listbox) and selected:
                index = selected[0]
                #Obtain all the user input
                #date = date_entry.get()
                #notes_title = notes_title_entry.get()

                #Execute the query
                get_notes = cur.execute("SELECT * FROM notes_table")
                #Obtain all the contents of the query
                rows = cur.fetchall()
                #print(rows[2][3:])
                #print(rows[index][3])
                if rows[index][3]:
                        t.insert(INSERT, rows[index][3])


create_listbox()
createTextBox()


lb1.bind('<<ListboxSelect>>', onselect)

#close the app
GUI.mainloop()
con.close()