import tkinter as tk

class Controller(tk.Tk):

    def __init__(self,pages, page_names, page_args = None,fonts=None, start_page = None, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)



        self.frames = {}
        
        self.data = {}

        if page_args is None:
            page_args = [{}]
        
        if fonts is None:
            self.fonts = {
                "TITLEFONT":("Verdana", 40),
                "LARGEFONT":("Verdana", 30),
                "SMALLFONT":("Verdana", 20)
            }
        else:
            self.fonts = fonts

        for i,F in enumerate(pages):
            frame = F(container, self, **page_args[i])

            self.frames[page_names[i]] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        if start_page is None:
            self.show_frame('start_page')
        else:
            self.show_frame(start_page)
        


        container.grid(row=0, column=0, sticky="NESW")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.show()
        frame.tkraise()
    
