from similarity import sim_docs_query
from queries_preprocess import query_preprocessing
from queries_representation import calculate_weigths_queries
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

   
if __name__=='__main__':
    
    file=open("idfs.json","r")
    idfs=json.load(file)
    file.close()

    file=open("vecs_docs.json","r")
    docs=json.load(file)
    file.close()

    file=open("limits.json","r")
    limits=json.load(file)
    file.close()
    
    def myfunction(event):
        canvas.configure(scrollregion=canvas.bbox("all"),width=1185,height=450)

    root=Tk()

    root.title("Roocle")

    root.resizable(False,False)

    root.geometry('1200x600')

    root.config(bg='purple')

    Label(root,text='Bienvenido a Roocle',bg='purple',font=('Arial',30),fg='yellow').place(x=400,y=25)

    entry=Entry(root,width=35)
    entry.place(x=400,y=100)
    
    docs_frame=Frame(root,width=1200,height=450)
    docs_frame.place(y=150)

    canvas=Canvas(docs_frame,width=1185,height=450)
    inner_frame=Frame(canvas,width=1185,height=450,bg='gray')
    myscrollbar=Scrollbar(docs_frame,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=inner_frame,anchor='nw')
    inner_frame.bind("<Configure>",myfunction)
    
    def search():
        
        query_terms=query_preprocessing(entry.get(), idfs)
        query_weights=calculate_weigths_queries(0.5, idfs, [query_terms])[0]
    
        sim_docs=sim_docs_query(docs, query_weights, 10)
    
        file=open("cran/cran.all.1400")
        lines=file.readlines()
        file.close()
    
        texts=[]
    
        for doc in sim_docs:
            l=limits[doc-1]
            text=[]
            for i in range(l[0],l[1]+1):
                text.append(lines[i])
            texts.append(text)
       
        for i in range(len(texts)):
            Label(inner_frame,text=i+1,bg='gray').grid(row=i,column=0)
        
            text=Text(inner_frame,width=80,height=35)
            text.grid(row=i,column=1,padx=10,pady=10)
        
            for line in texts[i]:
                text.insert(INSERT, line)
    
            text.config(state="disable")
            
            Label(inner_frame,text='¿Ha sido útil este documento?', bg='gray').grid(row=i,column=2,padx=10,pady=10)
            
            Button(inner_frame, text='Sí',font=('Arial',10), bg='green').grid(row=i,column=3,padx=10,pady=10)
            
            Button(inner_frame, text='No',font=('Arial',10), bg='red').grid(row=i,column=4,padx=10,pady=10)

    Button(root,text='Buscar',font=('Arial',8),command=search).place(x=700,y=100)
    
    root.mainloop()