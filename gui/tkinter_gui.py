import tkinter as tk

class TkinterGUI:

    def __init__(self):
        self.callbacks = {}

    @staticmethod
    def initialize():
        """
        Static method to create the GUI
        """
        gui = TkinterGUI()
        gui._initialize_elements() 
        return gui

    def add_callback(self, key, function):
        """
        Adds a callback function to GUI under the given parameter.
        """
        self.callbacks[key] = function 

    def exit(self):
        """
        Ends the mainloop of GUI, allowing the software to terminate.
        """
        self.window.destroy()

    def get_search_term(self):
        """
        Returns the current search term.
        """
        return self.search_term_entry.get()

    def highlight_term(self, term):
        """
        Highlights the given term with the position from the term.
        term = [word, position]
        """
        print("Highlighting :", term)

    def remove_highlights(self):
        """
        Removes all and any highlights that are currently on.
        """
        pass

    def start(self):
        """
        Stars the mainloop of the GUI.
        """
        self.window.mainloop()

    def _initialize_elements(self):
        """
        Initializes all elements to be shown.
        """
        window = tk.Tk()
        window.geometry("2560x1440")
        #canvas = tk.Canvas(window, width = 2560, height=1440)
        #canvas.pack()
        img = tk.PhotoImage(file="placeholder.png")
        bg = tk.Label(window, image=img)
        bg.place(x=0,y=0, relwidth=1, relheight=1)
        bg.image = img
        #self.gui_instance.canvas.create_image(0,0, anchor=tk.NW, image=img)
        #self.canvas = canvas
        label = tk.Label(window, text="Current search term:")
        label.pack()
        entry = tk.Entry(window)
        entry.bind("<KeyPress>", self._on_press_key)
        entry.pack()
        self.window = window
        self.search_term_entry = entry


    def _on_press_key(self, event):
        """
        Callback called whenever a key is pressed.
        Seperates Enter and rest of the keypresses to their own functions.
        """
        if event.keycode == 36:
            self._on_press_enter()
        else:
            self._on_term_change()

    def _on_press_enter(self):
        """
        Called when pressing enter to click the highlight.
        """
        if "click_term" in self.callbacks:
            self.callbacks["click_term"]()
        else:
            print("No callback set for pressing the enter key.")
        
        return True

    def _on_term_change(self):
        """
        Called when the search term changes at all.
        """
        if "search_term_change" in self.callbacks:
            self.callbacks["search_term_change"]()
        else:
            print("No callback set for term change.")

        return True 
