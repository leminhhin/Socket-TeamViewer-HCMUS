import tkinter as tk
import tkinter.ttk as thm
import pyautogui
import server

class server_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill=tk.BOTH, expand=True)
		self.make_widgets()
		self.parent.title("Server")

	def make_widgets(self):
		self.open_button = thm.Button(self, text="MỞ SERVER", width = 30, command=self.open_server)
		self.open_button.pack(fill=tk.Y, pady = 30, expand=True)
	
	def open_server(self):
		res = server.open_server()
		self.parent.destroy()

root = tk.Tk()
root.geometry("277x153+10+10")
app = server_frame(root)
app.mainloop()
