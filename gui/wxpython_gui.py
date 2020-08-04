import wx

class WxPythonGUI:

    def __init__(self):
        self.callbacks = {}
        self.highlight_frames = []

    @staticmethod
    def initialize():
        """
        Static method to create the GUI instance.
        """
        gui = WxPythonGUI()
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
        self.remove_highlights()
        self.search_frame.Close()

    def get_search_term(self):
        """
        Returns the current search term.
        """
        return self.search_term_entry.GetValue().lower()

    def highlight_term(self, term):
        """
        Highlights the given term with the position from the term.
        term = [word, position]
        """
        print("Highlighting :", term)
        left, top, width, height = term[1]
        self.remove_highlights()

        frame = wx.Frame(None, pos=wx.Point(left, top), size=wx.Size(width, height), style=wx.BORDER_NONE)
        #frame = wx.Frame(None, pos=wx.Point(x,y), size=wx.Size(width, height), style=wx.BORDER_NONE)
        frame.SetBackgroundColour(wx.Colour(255, 128, 255))
        frame.SetTransparent(500)
        frame.Show()
        self.highlight_frames.append(frame)

        self.search_term_entry.SetFocus() # Keep focus on the search term frame


    def remove_highlights(self):
        """
        Removes all and any highlights that are currently on.
        """
        while self.highlight_frames:
            frame = self.highlight_frames.pop(0)
            frame.Close()

    def start(self):
        """
        Stars the mainloop of the GUI.
        """
        self.search_frame.Show()
        self.app.MainLoop()

    def _initialize_elements(self):
        """
        Initializes all elements to be shown.
        """
        app = wx.App()
        frame = wx.Frame(None)
        search_term_entry = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
        search_term_entry.Bind(wx.EVT_TEXT, self._on_press_key)
        self.search_term_entry = search_term_entry
        self.search_frame = frame
        self.app = app

    def _on_press_key(self, event):
        """
        Callback called whenever a key is pressed.
        Seperates Enter and rest of the keypresses to their own functions.
        """
        string = event.GetString()
        if string and ord(string[-1]) == 10:
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
