import tkinter as tk
from tkinter import ttk


class ID_page(tk.Frame):
   def __init__(self, parent, controller, title_label_args = None, id_label_args=None, id_args = None, button_args = None, info_label_args=None, next_page=None): 
      tk.Frame.__init__(self, parent)


      self.controller = controller
      self.next_page = next_page


      if id_args is None:
         id_args = {}
      if "text" not in id_args:
         id_args["text"] = "ID"
      if "font" not in id_args:
         id_args["font"] = controller.fonts['LARGEFONT']


      if button_args is None:
         button_args = {}
      if 'text' not in button_args:
         button_args['text'] = "Submit"
      if 'font' not in button_args:
         button_args['font'] = controller.fonts['LARGEFONT']

      
      if title_label_args is None:
         title_label_args = {}
      if 'text' not in title_label_args:
         title_label_args["text"] = ""
      if 'font' not in title_label_args:
         title_label_args["font"] = controller.fonts['TITLEFONT']

      
      if id_label_args is None:
         id_label_args = {}
      if "text" not in id_label_args:
         id_label_args["text"] = "Participant ID:"
      if "font" not in id_label_args:
         id_label_args  ['font'] = controller.fonts['LARGEFONT']

      if info_label_args is None:
         info_label_args = {}
      if 'text' not in info_label_args:
         info_label_args['text'] = ""
      if 'font' not in button_args:
         info_label_args['font'] = controller.fonts['SMALLFONT']

      into_label = ttk.Label(self, **info_label_args)
      into_label.grid(row = 1, column = 1, padx = 10, pady = 10) 

      ttk.Label(self).grid(row = 2, column = 0, padx = 10, pady = 10) 

      title_label = ttk.Label(self, **title_label_args)
      title_label.grid(row = 0, column = 1, padx = 10, pady = 10) 

      id_label = ttk.Label(self, **id_label_args)
      id_label.grid(row = 3, column = 0, pady = 10) 

      self.id_var=tk.StringVar()
      self.id_entry = tk.Entry(self,textvariable = self.id_var, **id_args)
      self.id_entry.grid(row = 3, column = 1, pady = 10) 

      self.sub_btn=tk.Button(self, command = self.submit, **button_args)
      self.sub_btn.grid(row = 3, column = 2, pady = 10) 

   def submit(self):
      participant_id = self.id_entry.get()
      self.controller.data["participant_id"] = participant_id
      if self.next_page is not None:
         self.controller.show_frame(self.next_page)
        
   def show(self):
      pass


class Text_Page(tk.Frame):
   def __init__(self, parent, controller, text_args=None, button_args=None, next_page=None, button_func=None, button_delay=0): 
      tk.Frame.__init__(self, parent)


      self.controller = controller
      self.next_page = next_page
      self.button_func = button_func

      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)

      self.button_delay = button_delay


      if button_args is None:
         button_args = {}
      if 'text' not in button_args:
         button_args['text'] = "Next"
      if 'font' not in button_args:
         button_args['font'] = controller.fonts['LARGEFONT']

      
      if text_args is None:
         text_args = {}
      if "text" not in text_args:
         text_args["text"] = ""
      if "font" not in text_args:
         text_args['font'] = controller.fonts['LARGEFONT']
      if "justify" not in text_args:
         text_args['justify'] = tk.CENTER 

      self.into_label = ttk.Label(self, **text_args)
      self.into_label.grid(row = 0, column = 0, padx = 10, pady = 10) 

      self.sub_btn=tk.Button(self, command = self.submit, **button_args)
     

   def submit(self):
      if self.button_func is not None:
         self.button_func(self)
      if self.next_page is not None:
         self.controller.show_frame(self.next_page)
   
   def show(self):
      self.sub_btn.grid_forget()
      self.sub_btn.after(self.button_delay, lambda: self.sub_btn.grid(row = 1, column = 0, pady = 10)  )



class Response_Page(tk.Frame):
   def __init__(self, parent, controller, text_args=None, button_args=None,intensity_entry_args = None, 
                number_entry_args=None, next_page=None, intensity_label_args = None, number_label_args = None, 
                extra_func = None, extra_func_args={}, rest_page = None, rest_id=None): 
      tk.Frame.__init__(self, parent)

      self.controller = controller
      self.next_page = next_page

      self.extra_func = extra_func
      self.extra_func_args = extra_func_args

      self.rest_page = rest_page
      self.rest_id = rest_id

      self.i = 0

      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(1, weight=1)
      self.grid_columnconfigure(1, weight=1)

      if text_args is None:
         text_args = {}
      if "text" not in text_args:
         text_args["text"] = ""
      if "font" not in text_args:
         text_args['font'] = controller.fonts['LARGEFONT']
      if "justify" not in text_args:
         text_args['justify'] = tk.CENTER 

      if intensity_entry_args is None:
         intensity_entry_args = {}
      if "font" not in intensity_entry_args:
         intensity_entry_args["font"] = controller.fonts['LARGEFONT']
      

      if number_entry_args is None:
         number_entry_args = {}
      if "font" not in number_entry_args:
         number_entry_args["font"] = controller.fonts['LARGEFONT']
      
      if button_args is None:
         button_args = {}
      if 'text' not in button_args:
         button_args['text'] = "Submit"
      if 'font' not in button_args:
         button_args['font'] = controller.fonts['LARGEFONT']

      if intensity_label_args is None:
         intensity_label_args = {}
      if "text" not in intensity_label_args:
         intensity_label_args["text"] = "Intensity:"
      if "font" not in intensity_label_args:
         intensity_label_args['font'] = controller.fonts['LARGEFONT']
      if "justify" not in intensity_label_args:
         intensity_label_args['justify'] = tk.RIGHT 

      if number_label_args is None:
         number_label_args = {}
      if "text" not in number_label_args:
         number_label_args["text"] = "Number:"
      if "font" not in number_label_args:
         number_label_args['font'] = controller.fonts['LARGEFONT']
      if "justify" not in text_args:
         number_label_args['justify'] = tk.RIGHT 
      

      

      self.intensity_var=tk.StringVar()
      self.intensity_entry = tk.Entry(self,textvariable = self.intensity_var, **intensity_entry_args)
      self.intensity_entry.grid(row = 1, column = 1, pady = 10)
      
      self.num_var=tk.StringVar()
      self.num_entry = tk.Entry(self,textvariable = self.num_var, **number_entry_args)
      self.num_entry.grid(row = 2, column = 1, pady = 10)

      self.into_label = ttk.Label(self, **text_args)
      self.into_label.grid(row = 0, column = 0, padx = 10, pady = 10) 

      self.intensity_label = ttk.Label(self, **intensity_label_args)
      self.intensity_label.grid(row = 1, column = 0, padx = 10, pady = 10)

      self.number_label = ttk.Label(self, **number_label_args)
      self.number_label.grid(row = 2, column = 0, padx = 10, pady = 10)

      sub_btn=tk.Button(self, command = self.submit, **button_args)
      sub_btn.grid(row = 3, column = 1, pady = 10)

   def submit(self):
         intensity = self.intensity_entry.get()
         number = self.num_entry.get()
         valid = False
         if number in ['1','2','3','4','5','6','7','8','9']:
            self.controller.data["number"] = number
            valid = True
         else:
            self.number_label['text'] = "Please enter a number between 1-9"

         try:
            float(intensity)
            valid = valid and True
            self.controller.data["intensity"] = intensity
         except ValueError:
            valid = False
            self.intensity_label['text'] = "Please enter a numeric value"

         if valid:
            self.number_label['text'] = "Number:"
            self.intensity_label['text'] = "Intensity:"
            self.num_entry.delete(0, 'end')
            self.intensity_entry.delete(0, 'end')
            
            self.i += 1
            if self.rest_id is not None:
               print(self.i % self.rest_id)
               if self.i % self.rest_id == 0:
                  self.controller.show_frame(self.rest_page)
               elif self.next_page is not None:
                  self.controller.show_frame(self.next_page)
            
            elif self.next_page is not None:
               self.controller.show_frame(self.next_page)
        
         if self.extra_func is not None:
            self.extra_func(self.controller, **self.extra_func_args)
   
   def show(self):
      pass