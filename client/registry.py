import tkinter as tk
import tkinter.ttk as thm
from tkinter import scrolledtext as st
import tkinter.messagebox as msbx
import tkinter.filedialog as file_dlg
import client

class reg_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill=tk.BOTH, expand=True)
		self.make_widgets()
		self.tmp_client = client.Client
		self.parent.title("registry")

	def make_widgets(self):
		#Tạo frame
		self.frame1 = tk.Frame(self)
		self.frame1.pack(fill=tk.BOTH, expand = True)

		self.frame2 = tk.Frame(self.frame1)
		self.frame2.pack(side="top", fill=tk.X)
		
		self.frame3 = tk.Frame(self.frame1)
		self.frame3.pack(side="top", fill=tk.BOTH)

		self.frame4 = tk.LabelFrame(self.frame1, text="Sửa giá trị trực tiếp")
		self.frame4.pack(side="top", fill=tk.BOTH, padx = 10, pady = 10, expand = True)

		self.frame5 = tk.Frame(self.frame4)
		self.frame5.pack(side="top", fill = tk.X)
		
		self.frame6 = tk.Frame(self.frame4)
		self.frame6.pack(side="top", fill = tk.X, anchor = tk.N)
		self.frame_func = tk.Frame(self.frame6)

		self.frame7 = tk.Frame(self.frame4)
		self.frame7.pack(side="top")

		#Đường dẫn file registry
		self.link_label = tk.Label(self.frame2, text="Đường dẫn", width = 10)
		self.link_label.pack(side="left", padx = 5, pady = 5)

		self.link_entry = thm.Entry(self.frame2)
		self.link_entry['state'] = 'readonly'
		self.link_entry.pack(side="left", fill = tk.X, padx = 5, pady = 5, expand = True)

		self.browser_button = thm.Button(self.frame2, text = "Browser...", width = 12, command = self.find_reg)
		self.browser_button.pack(side="right", padx = 5, pady = 5)

		#Nội dung registry
		self.reg_sending_label = tk.Label(self.frame3, text="Nội dung", width = 10)
		self.reg_sending_label.pack(side="left", fill=tk.Y, padx = 5, pady = 5)

		self.reg_sending_entry = tk.Text(self.frame3, width = 45, height = 6)
		self.reg_sending_entry.pack(side="left", padx = 5)

		self.reg_sending_button = thm.Button(self.frame3, text="Gửi nội dung", width = 12, command=self.reg_sending)
		self.reg_sending_button.pack(side="right", fill=tk.Y, padx = 5, pady = 5)

		#Chọn chức năng
		self.select_default = tk.StringVar(value='Chọn chức năng')
		self.select_function = thm.Combobox(self.frame5, textvariable=self.select_default)
		self.select_function['state'] = 'readonly'
		self.select_function["value"] = ("Get value", "Set value", "Delete value", "Create key", "Delete key")
		self.select_function.pack(side="top", fill=tk.X, padx = 5, pady = 5)
		self.select_function.bind('<<ComboboxSelected>>', self.func_combo_bind)

		#Đường dẫn
		self.select_path = thm.Entry(self.frame5)
		self.select_path_default = tk.StringVar(value='Đường dẫn...')
		self.select_path.config(textvariable=self.select_path_default)
		self.select_path['state'] = 'normal'
		self.select_path.pack(side="top", fill=tk.X, padx = 5, pady = 5)

		#Value
		self.name_frame = tk.Frame(self.frame6)
		self.name_frame.pack(side="left", fill=tk.X, expand = True, padx = 5, pady = 5)
		self.value_frame = tk.Frame(self.frame6)
		self.value_frame.pack(side="left", fill=tk.X, expand = True, padx = 5, pady = 5)
		self.data_frame = tk.Frame(self.frame6)
		self.data_frame.pack(side='right', fill = tk.X, expand = True, padx = 5, pady = 5)

		self.name_value_default = tk.StringVar(value='Name value')
		self.value_default = tk.StringVar(value='Value')
		self.data_type_default = tk.StringVar(value='Kiểu dữ liệu')
		
		self.name_value_entry = thm.Entry(self.name_frame, textvariable = self.name_value_default)
		self.name_value_entry.pack(fill=tk.X, expand = True)

		self.value_entry = thm.Entry(self.value_frame, textvariable = self.value_default)
		self.value_entry.pack(fill=tk.X, expand = True)

		self.data_type_combo_box = thm.Combobox(self.data_frame, textvariable = self.data_type_default)
		self.data_type_combo_box['state'] = 'readonly'
		self.data_type_combo_box['value'] = ("String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String")
		self.data_type_combo_box.pack(fill = tk.X, expand = True)
		
		#Đọc giá trị registry
		self.read_registry_entry = tk.Text(self.frame7, height = 6)
		self.read_registry_entry['state'] = 'disabled'
		self.read_registry_entry.pack(side="top", padx = 5, pady = 5)

		self.send_button = thm.Button(self.frame7, text="Gửi", width = 15, command=self.reg_editor)
		self.send_button.pack(side="left", padx = 70, pady = 5)

		self.clear_button = thm.Button(self.frame7, text="Xoá", width = 15, command=self.delete_all)
		self.clear_button.pack(side="right", padx = 70, pady = 5)

	def find_reg(self):
		ftypes = [('registry', '*.reg'), ('All files', '*')]
		dlg = file_dlg.Open(self, filetypes = ftypes)
		fl = dlg.show()

		self.path = tk.StringVar(value=fl)
		self.link_entry.config(textvariable=self.path)

		if fl != '':
			self.text = self.readFile(fl)
			self.reg_sending_entry.delete("1.0", tk.END)
			self.reg_sending_entry.insert(tk.INSERT, self.text)

	def readFile(self, filename):
		f = open(filename, "r")
		text = f.read()
		return text

	def reg_sending(self):
		self.reg = self.reg_sending_entry.get("1.0", tk.END);
		if ((self.reg == '\n') | (self.reg == '')):
			msbx.showwarning('', "Lỗi")
			return None
		res = self.tmp_client.req_reg_import(self.tmp_client, self.reg)
		if res:
			msbx.showinfo('', "Sửa thành công")
		else:
			msbx.showerror('', "Không thể sửa registry")

	def func_combo_bind(self, event):
		if ((self.select_function.get() == "Get value") | (self.select_function.get() == "Delete value")):
			self.value_entry.pack_forget()
			self.data_type_combo_box.pack_forget()
			self.name_value_default = tk.StringVar(value='Name value')
			self.name_value_entry.config(textvariable = self.name_value_default)
			self.name_value_entry.pack(fill=tk.X, expand = True)
		elif ((self.select_function.get() == "Create key") | (self.select_function.get() == "Delete key")):
			self.name_value_entry.pack_forget()
			self.value_entry.pack_forget()
			self.data_type_combo_box.pack_forget()
		else:
			self.name_value_default = tk.StringVar(value='Name value')
			self.value_default = tk.StringVar(value='Value')
			self.data_type_default = tk.StringVar(value='Kiểu dữ liệu')
		
			self.name_value_entry.config(textvariable = self.name_value_default)
			self.name_value_entry.pack(fill=tk.X, expand = True)

			self.value_entry.config(textvariable = self.value_default)
			self.value_entry.pack(fill=tk.X, expand = True)

			self.data_type_combo_box.config(textvariable = self.data_type_default)
			self.data_type_combo_box['state'] = 'readonly'
			self.data_type_combo_box['value'] = ("String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String")
			self.data_type_combo_box.pack(fill=tk.X, expand = True)

	def reg_editor(self):
		self.reg_func = self.select_function.get()
		self.reg_path = self.select_path.get()
		self.reg_name = self.name_value_entry.get()
		self.reg_value = self.value_entry.get()
		self.reg_type = self.data_type_combo_box.get()
		if self.reg_func == "Get value":
			text = self.tmp_client.req_reg_getvalue(self.tmp_client, self.reg_path, self.reg_name)
			if text:
				self.reg_print(text['value'])
			else:
				self.reg_print("Lỗi")
			return None
		if self.reg_func == "Set value":
			res = self.tmp_client.req_reg_setvalue(self.tmp_client, self.reg_path, self.reg_name, self.reg_type, self.reg_value)
			if res:
				self.reg_print("Set value thành công")
			else:
				self.reg_print("Lỗi")
			return None
		if self.reg_func == "Delete value":
			res = self.tmp_client.req_reg_deletevalue(self.tmp_client, self.reg_path, self.reg_name)
			if res:
				self.reg_print("Xoá value thành công")
			else:
				self.reg_print("Lỗi")
			return None
		if self.reg_func == "Create key":
			res = self.tmp_client.req_reg_createkey(self.tmp_client, self.reg_path)
			if res:
				self.reg_print("Create key thành công")
			else:
				self.reg_print("Lỗi")
			return None
		if self.reg_func == "Delete key":
			res = self.tmp_client.req_reg_deletekey(self.tmp_client, self.reg_path)
			if res:
				self.reg_print("Xoá key thành công")
			else:
				self.reg_print("Lỗi")
			return None
		else:
			self.reg_print("Lỗi")

	def reg_print(self, text):
		self.read_registry_entry['state'] = 'normal'
		self.read_registry_entry.insert(tk.INSERT, text + '\n')
		self.read_registry_entry['state'] = 'disabled'

	def delete_all(self):
		self.read_registry_entry['state'] = 'normal'
		self.read_registry_entry.delete("1.0", tk.END)
		self.read_registry_entry['state'] = 'disabled' 
