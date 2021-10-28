import tkinter as tk
import tkinter.ttk as thm
import tkinter.messagebox as msbx
import client

class listApp_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill = tk.BOTH, expand = True)
		self.make_widgets()
		self.tmp_client = client.Client
		self.parent.title("Application")

	def make_widgets(self):
		#Tạo các button
		frame1 = tk.Frame(self)
		frame1.pack(fill=tk.BOTH, padx = 20, pady = 20, expand = True)	

		frame2 = tk.Frame(frame1)
		frame2.pack(side = "top", fill = tk.BOTH, expand = True)
		
		frame3 = tk.Frame(frame1)
		frame3.pack(side = "bottom", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.kill_button = thm.Button(frame2, text = "Kill", command=self.kill_window)
		self.kill_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.view_button = thm.Button(frame2, text = "Xem", command=self.get_running_applications)
		self.view_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.delete_button = thm.Button(frame2, text = "Xoá", command=self.delete)
		self.delete_button.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 10, expand = True)

		self.start_button = thm.Button(frame2, text = "Start", command=self.start_window)
		self.start_button.pack(side = "right", fill = tk.BOTH, padx = 10, pady = 10, expand = True)
		
		#Tạo bảng

		 # Set the treeview 
		self.tree = thm.Treeview(frame3, columns=('name', 'pid', 'num_threads'), show='headings')
		

        # Set the heading (Attribute Names)
		self.tree.heading('#1', text='Name Application')
		self.tree.heading('#2', text='ID Application')
		self.tree.heading('#3', text='Count Threads')

        # Specify attributes of the columns (We want to stretch it!)
		self.tree.column('#1', stretch=tk.YES, width = 280)
		self.tree.column('#2', stretch=tk.YES, width = 110)
		self.tree.column('#3', stretch=tk.YES, width = 110)
		self.tree.grid(row=0, column=0, sticky='nsew')

		self.scrollbar = thm.Scrollbar(frame3, orient='vertical')
		self.scrollbar.configure(command=self.tree.yview)
		self.scrollbar.grid(row=0, column=1, sticky='ns')

		self.tree.config(yscrollcommand=self.scrollbar.set)

	def get_running_applications(self):
		try:
			procs = self.tmp_client.req_process_getallapp(self.tmp_client)

			self.delete()
			for proc in procs:
				self.tree.insert('', 'end', values=(proc['name'], proc['pid'], proc['num_threads']))
		except:
			return None

	def kill_window(self):
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x50+150+150")
		self.top.winfo_toplevel().title("Kill")

		self.top.text_default = tk.StringVar(value="Nhập PID")
		self.kill_entry = thm.Entry(self.top, textvariable = self.top.text_default)
		self.kill_entry.pack(side="left", padx = 5, fill=tk.X, expand = True)

		self.kill_button = thm.Button(self.top, text="Kill", width = 15, command = self.kill_process)
		self.kill_button.pack(side="right", padx = 5)

	def kill_process(self):
		pid = self.kill_entry.get()
		if ((pid == '') | (pid == "Nhập PID")):
			msbx.showwarning('', "Chưa nhập PID")
			return None
		res = self.tmp_client.req_process_kill(self.tmp_client, int(pid))
		
		if res:
			msbx.showinfo('', "Đã diệt chương trình")
		else:
			msbx.showerror('', "Không tìm thấy chương trình")

	def delete(self):
		for p in self.tree.get_children():
			self.tree.delete(p)
		self.update

	def start_window(self):
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x50+150+150")
		self.top.winfo_toplevel().title("Start")

		self.top.text_default = tk.StringVar(value="Nhập tên")
		self.start_entry = thm.Entry(self.top, textvariable = self.top.text_default)
		self.start_entry.pack(side="left", padx = 5, fill=tk.X, expand = True)

		self.start_button = thm.Button(self.top, text="Start", width = 15, command = self.start_process)
		self.start_button.pack(side="right", padx = 5)

	def start_process(self):
		name = self.start_entry.get()
		if ((name == '') | (name == "Nhập tên")):
			msbx.showwarning('', "Chưa nhập tên Process")
			return None
		res = self.tmp_client.req_process_start(self.tmp_client, name)
		if res:
			msbx.showinfo('', "Chương trình đã được bật")
		else:
			msbx.showerror('', "Không tìm thấy chương trình")