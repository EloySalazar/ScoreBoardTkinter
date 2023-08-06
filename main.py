import glob
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter as ct
import matplotlib as mpl
import matplotlib.pyplot

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue") 

class Add_Player_Box(ct.CTkToplevel):
    def __init__(self,category):
        super().__init__()
        self.title("Add Player")
        self.geometry("300x300")
        self.resizable(0,0)
        self.category = category
    
        self.initialize_gui()

    def save(self,event):

        numeral_pattern = r'^[0-9]'
        view = re.compile(numeral_pattern)
        view_victories = self.victories_text.get().strip()
        view_defeats  = self.defeats_text.get().strip()
        if re.match(view, view_victories) is None:
            messagebox.showwarning("Error", "Solo numeros")
           
        elif re.match(view, view_defeats) is None:
            messagebox.showwarning("Error", "Solo numeros")
            

        self.data = open(self.category, "a")
        self.data.write("\n")
        self.data.write("J" + self.name_text.get() + "\n")
        self.data.write("V" + self.victories_text.get() + "\n")
        self.data.write("D" + self.defeats_text.get() + "\n")
        self.data.close()

        app.updated(None)

        self.destroy()

    def initialize_gui(self):

        self.name_label = ct.CTkLabel(self,font = ("Arial",18),text = "Name:")
        self.name_label.place(x = 0,y = 0)

        self.defeats_label = ct.CTkLabel(self,font = ("Arial",18),text = "Defeats:")
        self.defeats_label.place(x = 0,y = 40)

        self.victories_label = ct.CTkLabel(self,font = ("Arial",18),text = "Victories:")
        self.victories_label.place(x = 0,y = 80)

        self.name_text = ct.CTkEntry(self,font = ("Arial",18))
        self.name_text.place(x = 60,y = 0)    

        self.defeats_text = ct.CTkEntry(self,font = ("Arial",18))
        self.defeats_text.place(x = 60,y = 40) 

        self.victories_text = ct.CTkEntry(self,font = ("Arial",18))
        self.victories_text.place(x = 70,y = 80) 

        self.protocol("WM_DELETE_WINDOW",lambda: self.save(None))




class Player(ct.CTkToplevel):
    
    def __init__(self,victories,defeats,name,data):
        super().__init__()
        self.title("Player")

        print(victories,defeats)
        self.victories = victories
        self.defeats = defeats
        self.name = name
        self.data = data

        self.palette={"primary":"#FEF702",
         "background": "#252525",
         "primary_chart":"#F1F1F1",
         "text_color": "#F4F6F7"}

        self.colors_list = ["#21618c","#7b241c"]
        mpl.rcParams["axes.titlesize"] = 32
        mpl.rcParams['text.color'] = "F4F6F7"
        mpl.rcParams["figure.facecolor"] = self.palette["background"]
        mpl.rcParams["axes.facecolor"] = self.palette["background"]
        mpl.rcParams["savefig.facecolor"] = self.palette["background"]
        mpl.rcParams['axes.labelcolor']= self.palette["text_color"]
        
        
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        self.figure_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, )
        NavigationToolbar2Tk(self.figure_canvas, self)

        self.axes = self.figure.add_subplot()
        self.line = self.axes.pie((self.victories,self.defeats),labels= ["Victories","Defeats"],autopct="%0.1f %%",colors = self.colors_list)
        self.axes.axis("equal")
        self.axes.set_title('Statistics')

        self.geometry("600x600")
        self.resizable(0,0)
        self.initialize_gui()

    def increase(self,label):
        text_original = label.cget("text")[:label.cget("text").find(":") + 1]
        tex = label.cget("text")
        value = [int(s) for s in re.findall(r'\d+', tex)]
        label.configure(text = text_original + str(value[0] + 1))

    def decrease(self,label):
        text_original = label.cget("text")[:label.cget("text").find(":") + 1]
        tex = label.cget("text")
        value = [int(s) for s in re.findall(r'\d+', tex)]
        label.configure(text = text_original + str(value[0] - 1))

    def save(self,name,victories,defeats,data,victories_original,defeats_original):
        data_read = open(data)
        line_data = []

        for line in data_read.readlines():

            line_data.append(line)

        number = [number for number in range(len(line_data))]

        for l in zip(number, line_data):

            if l[1].startswith("V"):
                if l[1][1:] == victories_original:
                    
                    line_data[l[0]] = "V" + victories.cget("text")[victories.cget("text").find(
                        ":") + 1:].replace(" ", "") + "\n"
                   

            elif l[1].startswith("D"):
                if l[1][1:] == defeats_original:
                    
                    line_data[l[0]] = "D" + defeats.cget("text")[defeats.cget("text").find(
                        ":") + 1:].replace(" ", "") + "\n"
                    

        data_read.close()

        data_append = open(data, "w")
        data_append.writelines(line_data)
        data_append.close()

        app.updated(None)

        self.destroy()

    def initialize_gui(self):
        
        self.name_label  = ct.CTkLabel(self,font= ("Arial",24),text= "name: " +self.name)
        self.name_label.place(x = 0 ,y = 100)

        self.victories_label = ct.CTkLabel(self,font= ("Arial",18),text= "Victories: " + self.victories)
        self.victories_label.place(x= 130,y = 1)

        self.defeats_label = ct.CTkLabel(self,font= ("Arial",18),text= "Defeats: " + self.defeats )
        self.defeats_label.place(x = 130,y = 50)
        
        self.victories_buton_sum = ct.CTkButton(self,font= ("Arial",22),text= ">",width= 7,command= lambda: self.increase(self.victories_label))
        self.victories_buton_sum.place(x = 250,y = 1)

        self.victories_buton_res = ct.CTkButton(self,font= ("Arial",23),text= "<",width= 7,command= lambda: self.decrease(self.victories_label))
        self.victories_buton_res.place(x = 80,y = 1)

        self.defeats_buton_sum = ct.CTkButton(self,font= ("Arial",22),text= ">",width= 7,command= lambda: self.increase(self.defeats_label))
        self.defeats_buton_sum.place(x = 250,y = 50)

        self.defeats_buton_res = ct.CTkButton(self,font= ("Arial",23),text= "<",width= 7,command= lambda: self.decrease(self.defeats_label))
        self.defeats_buton_res.place(x = 80,y = 50)

        self.protocol("WM_DELETE_WINDOW",lambda: self.save(self.name_label,self.victories_label,self.defeats_label,self.data,self.victories,self.defeats))

class Data(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Statistics")
        self.geometry("625x500")
        self.resizable(0,0)
        

        self.total_players = []
        self.players = []
        self.victories = []
        self.defeasts = []



        style = ttk.Style()
    
        style.theme_use("default")
    
        style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            font = 25,
                            rowheight=25,
                            fieldbackground="#343638",
                            bordercolor="#343638",
                            borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                            background="#565b5e",
                            foreground="white",
                            relief="flat")
        style.map("Treeview.Heading",
                      background=[('active', '#3484F0')])
        
        self.toplevel_window = None
        self.toplevel_window_data = None
        
        self.initialize_gui()

    def updated(self,event):
        print(self.players)
        data = open(self.category.get())
        
        self.table.delete(*self.table.get_children())
        
        self.category_label.configure(text = self.category.get())

        self.players.clear()
        self.victories.clear()
        self.defeasts.clear()

        

        for line in data:
            if line[:1] == "J":
                self.players.append(line[1:])
            if line[:1] == "V":
                self.victories.append(line[1:])
            if line[:1] == "D":
                self.defeasts.append(line[1:])
        
        print(self.total_players)

        for informacion in self.total_players:
            for i in range(len(self.total_players[0][1])):
                self.table.insert("", tk.END, text=informacion[0][i], values=(
                    informacion[1][i], informacion[2][i]))

        data.close()    
        self.total_players.clear()
        self.total_players.append([self.players, self.victories,self.defeasts])


    def view_player(self,event):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            item = self.table.selection()[0]
            v = self.table.item(item, option="values")[0]
            d = self.table.item(item, option="values")[1]
            n = self.table.item(item, option="text")

            self.toplevel_window = Player(v,d,n,self.category.get())  
        else:
            self.toplevel_window.focus()  

    def initialize_table(self):

        data = open(self.category.get())
        
        for linea in data:
            if linea[:1] == "J":
                self.players.append(linea[1:])
            if linea[:1] == "V":
                self.victories.append(linea[1:])
            if linea[:1] == "D":
                self.defeasts.append(linea[1:])

        self.total_players.append([self.players, self.victories,self.defeasts])

        for informacion in self.total_players:
            for i in range(len(self.total_players[0][1])):
                self.table.insert("", tk.END, text=informacion[0][i], values=(
                    informacion[1][i], informacion[2][i]))

        data.close()

    def show_all(self):
        palette={"primary":"#FEF702",
        "background": "#252525",
        "primary_chart":"#F1F1F1",
        "text_color": "#F4F6F7"}
        data = {}
        for p,v in zip(self.players,self.victories):
            data[p] = int(v)


        mpl.rcParams["axes.titlesize"] = 32
        mpl.rcParams['text.color'] = "F4F6F7"
        mpl.rcParams["figure.facecolor"] = palette["background"]
        mpl.rcParams["axes.facecolor"] = palette["background"]
        mpl.rcParams["savefig.facecolor"] = palette["background"]
        mpl.rcParams['axes.labelcolor']= palette["text_color"]

        matplotlib.pyplot.bar(data.keys(),data.values())
        matplotlib.pyplot.show()

    def add_category(self):
        self.dialog = ct.CTkInputDialog(text="enter the name of the category:", title="Input")
        self.datos = open(self.dialog.get_input() + ".dat","w")
        self.category.configure(values=glob.glob('*.dat'))

    def add_player(self):
        if self.toplevel_window_data is None or not self.toplevel_window_data.winfo_exists():
 
            self.toplevel_window_data = Add_Player_Box(self.category.get())  
        else:
            self.toplevel_window_data.focus() 

    def initialize_gui(self):

        self.table = ttk.Treeview(self, columns=("victorias","derrotas"))
        self.table.heading("#0", text="Players")
        self.table.heading("victorias", text="Victories")
        self.table.heading("derrotas", text="Defeats")
        self.table.bind("<<TreeviewOpen>>", self.view_player)
        self.table.pack( padx=20, pady=20)

        self.category = ct.CTkComboBox(self,values=glob.glob('*.dat'),command= self.updated)
        self.category.pack(padx = 1,pady = 1)

        self.category_label = ct.CTkLabel(self,font=("Arial",24),text= glob.glob('*.dat')[0])
        self.category_label.pack( padx=1, pady=5)
        
        self.show_all_boton = ct.CTkButton(self,font = ("Arial",18),text="Show_all",command= self.show_all)
        self.show_all_boton.pack(padx = 0,pady = 5)

        self.add_category_boton = ct.CTkButton(self,font = ("Arial",18),text = "Add Category",command= self.add_category)
        self.add_category_boton.pack(padx = 0,pady = 5)

        self.add_player_boton = ct.CTkButton(self,font = ("Arial",18),text = "Add Player",command= self.add_player)
        self.add_player_boton.pack(padx = 20,pady = 5)

        self.initialize_table() 
        
        
        


app = Data()
app.mainloop()