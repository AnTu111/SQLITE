import sqlite3
import tkinter as tk
from tkinter import messagebox

connection = sqlite3.connect('Python_raamatukogu.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Autor(
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL, 
sünnikuupäev TEXT)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Žanrid(
žanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
žanri_nimi TEXT NOT NULL)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Raamatud(
raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pealkiri TEXT NOT NULL,
väljaandmise_kuupäev TEXT,
autor_id INTEGER,
žanr_id INTEGER,
FOREIGN KEY (autor_id) REFERENCES Autor (autor_id),
FOREIGN KEY (žanr_id) REFERENCES Žanrid (žanr_id))''')


# Добавление книги
def adding_books():
    pealkiri = entry_title.get()
    väljaandmise_kuupäev = entry_date.get()
    autor_id_val = entry_author_id.get()
    zanr_id_val = entry_genre_id.get()

    if pealkiri != "" and väljaandmise_kuupäev != "" and autor_id_val.isdigit() and zanr_id_val.isdigit() and int(autor_id_val) > 0 and int(zanr_id_val) > 0:
        cursor.execute("INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, žanr_id) VALUES (?, ?, ?, ?)",
                       (pealkiri, väljaandmise_kuupäev, autor_id_val, zanr_id_val,))
        connection.commit()
        messagebox.showinfo("Lisamine,", f"{pealkiri},{väljaandmise_kuupäev},{autor_id_val},{zanr_id_val} on lisatud.")
    else:
        messagebox.showerror("Viga", "Kontrollige kas kõik lahtrid on täidetud.")


# Удаление книги по ID
def deleting_book():
    raamat_id_val = entry_raamat_id.get()
    if raamat_id_val.isdigit():
        cursor.execute("SELECT * FROM Raamatud WHERE raamat_id=?", (raamat_id_val,))
        raamat = cursor.fetchone()
        if raamat != None:
            cursor.execute("DELETE FROM Raamatud WHERE raamat_id=?", (raamat_id_val,))
            connection.commit()
            messagebox.showinfo("Kustutamine", "Raamat on kustutatud.")
        else:
            messagebox.showerror("Viga", "Raamatu ID on puudu.")
    else:
        messagebox.showerror("Viga", "Sisestage kehtiv raamatu ID.")  # Указано не число



def show_books():
    # Очистка списка перед обновлением данных
    alllist_list.delete(0, tk.END) #0 указывает на индекс начала удаления 
    print("Kuvatakse kõik raamatud:")
    raamatud = cursor.execute('''SELECT Raamatud.raamat_id, Raamatud.pealkiri, Raamatud.väljaandmise_kuupäev, 
                                   Autor.autor_nimi, Žanrid.žanri_nimi
                            FROM Raamatud
                            INNER JOIN Autor ON Raamatud.autor_id = Autor.autor_id
                            INNER JOIN Žanrid ON Raamatud.žanr_id = Žanrid.žanr_id''').fetchall()  

    for raamat in raamatud:
        # Вставить строку данных в Listbox
        alllist_list.insert(tk.END, raamat)



def add_author():
    autor_nimi_val = entry_author_name.get()
    autor_date_val = entry_author_date.get()
    if autor_nimi_val != "" and autor_date_val != "":
        cursor.execute("INSERT INTO Autor (autor_nimi, sünnikuupäev) VALUES (?,?)", (autor_nimi_val, autor_date_val,))
        connection.commit()
        messagebox.showinfo("Lisamine", f"Uus autor '{autor_nimi_val}' '{autor_date_val}' on lisatud.")
    else:
        messagebox.showerror("Viga", "Palun sisestage autori nimi ja sünnikuupäev")


# Удаление по ID автора.
def delete_author():
    autor_id_val = entry_authorid.get()
    if autor_id_val.isdigit():
        cursor.execute("SELECT * FROM Autor WHERE autor_id=?", (autor_id_val,))
        autor = cursor.fetchone()
        if autor != None:
            cursor.execute("DELETE FROM Autor WHERE autor_id=?", (autor_id_val,))
            connection.commit()
            messagebox.showinfo("Kustutamine", "Autor on edukalt kustutatud")
        else:
            messagebox.showerror("Viga", "Autori ID on puudu.")
    else:
        messagebox.showerror("Autori ID", "On kehtetu või valesti sisestatud.")


def show_all_authors():
    alllist_list.delete(0, tk.END)
    
    print("Kuvatakse kõik autors:")
    autors = cursor.execute('''SELECT autor_id, autor_nimi, sünnikuupäev FROM Autor''').fetchall()
    for autor in autors:
        alllist_list.insert(tk.END, autor)



def add_žanr():
    žanri_nimi =  entry_žanr_name.get()
    if žanri_nimi != "":
            cursor.execute("INSERT INTO Žanrid (žanri_nimi) VALUES (?)", (žanri_nimi,))
            connection.commit()
            messagebox.showinfo("Lisamine", f"Uus žanr '{žanri_nimi}' on lisatud.")
    else:
        messagebox.showerror("Viga", "Palun sisestage žanri nimi.")

def delete_žanr():
    žanr_id = entry_žanr_id.get()
    if žanr_id.isdigit:
        cursor.execute("SELECT * FROM Žanrid WHERE žanr_id=?", (žanr_id,))
        žanr = cursor.fetchone()
        if žanr != None:
            cursor.execute("DELETE FROM Žanrid WHERE žanr_id=?", (žanr_id,))
            connection.commit()
            messagebox.showinfo("Kustutamine,",f"{žanr_id} on edukalt kustutatud")
        else:
            messagebox.showerror("Viga", "žanri ID on puudu.")
    else:
        messagebox.showerror("žanriID on kehtetu või valesti sisestatud.")

def show_all_žanrid():
    # Очистка списка перед обновлением данных
    alllist_list.delete(0, tk.END)
    
    print("Kuvatakse kõik žanrid:")
    žanrid = cursor.execute('''SELECT žanr_id, žanri_nimi FROM Žanrid''').fetchall()
    for žanr in žanrid:
           # Вставить строку данных в Listbox
        alllist_list.insert(tk.END, žanr)
        
        

root = tk.Tk()
root.title("Raamatukogu database")
root.configure(bg="#333")

button_frame1 = tk.Frame(root, bg="#333")
button_frame1.pack(side=tk.LEFT, padx=10)

btn_show_books = tk.Button(button_frame1, text="Kuva kõik raamatud", command=show_books, bg='white')
btn_show_books.pack()

btn_delete_book = tk.Button(button_frame1, text="Kustuta raamat", command=deleting_book, bg='white')
btn_delete_book.pack()
entry_raamat_id = tk.Entry(button_frame1)
entry_raamat_id.pack()

label_title = tk.Label(button_frame1, text="Pealkiri: ", bg="#333", fg="white")
label_title.pack()
entry_title = tk.Entry(button_frame1)
entry_title.pack()

label_date = tk.Label(button_frame1, text="Kuupäev: ", bg="#333", fg="white")
label_date.pack()
entry_date = tk.Entry(button_frame1)
entry_date.pack()

label_author_id = tk.Label(button_frame1, text="Autori ID:", bg="#333", fg="white")
label_author_id.pack()
entry_author_id = tk.Entry(button_frame1)
entry_author_id.pack()

label_genre_id = tk.Label(button_frame1, text="Žanri ID:", bg="#333", fg="white")
label_genre_id.pack()
entry_genre_id = tk.Entry(button_frame1)
entry_genre_id.pack()

btn_add_book = tk.Button(button_frame1, text="Lisa raamat", command=adding_books, bg='white')
btn_add_book.pack()




button_frame2 = tk.Frame(root, bg="#333")
button_frame2.pack(side=tk.LEFT, padx=10)

btn_show_authors = tk.Button(button_frame2, text="Kuva kõik autoreid", command=show_all_authors, bg='white')
btn_show_authors.pack()

btn_delete_author = tk.Button(button_frame2, text="Kustuta autor", command=delete_author, bg='white')
btn_delete_author.pack()
entry_authorid = tk.Entry(button_frame2)
entry_authorid.pack()

label_author_name = tk.Label(button_frame2, text="Autori nimi: ", bg="#333", fg="white")
label_author_name.pack()
entry_author_name = tk.Entry(button_frame2)
entry_author_name.pack()

label_author_date = tk.Label(button_frame2, text="Autori sünnikuupäev: ", bg="#333", fg="white")
label_author_date.pack()
entry_author_date = tk.Entry(button_frame2)
entry_author_date.pack()

btn_add_author = tk.Button(button_frame2, text="Lisa autor: ", command=add_author, bg='white')
btn_add_author.pack()



button_frame3 = tk.Frame(root, bg="#333")
button_frame3.pack(side=tk.LEFT, padx=10)

btn_show_žanr = tk.Button(button_frame3, text="Kuva kõik žanrid", command=show_all_žanrid, bg='white')
btn_show_žanr.pack()

btn_delete_žanr = tk.Button(button_frame3, text="Kustuta žanr", command=delete_žanr, bg='white')
btn_delete_žanr.pack()
entry_žanr_id = tk.Entry(button_frame3)
entry_žanr_id.pack()

label_žanr_name = tk.Label(button_frame3, text="Žanr nimi:: ", bg="#333", fg="white")
label_žanr_name.pack()
entry_žanr_name = tk.Entry(button_frame3)
entry_žanr_name.pack()

btn_add_žanr = tk.Button(button_frame3, text="Lisa žanr: ", command= add_žanr, bg='white')
btn_add_žanr.pack()






alllist_list = tk.Listbox(root, height=10, width=50, bg="white", fg="black")
alllist_list.pack(padx=10, pady=10)


root.mainloop()

connection.close()