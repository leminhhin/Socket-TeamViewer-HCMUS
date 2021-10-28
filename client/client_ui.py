import tkinter as tk
import tkinter.ttk as thm
import tkinter.messagebox as msbx
import client
import process
import listApp
import registry
import keylog
import pic

class client_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill=tk.BOTH, padx = 30, pady = 30, expand=True)
		self.make_widgets()
		self.status = False
		self.parent.title("Client")

	def make_widgets(self):
		#Nhập địa chỉ IP
		ip_frame = tk.Frame(self)
		ip_frame.pack(fill=tk.X)
		
		ip_label = thm.Label(ip_frame, text="Nhập địa chỉ IP:", width=15)
		ip_label.pack(side="left")
		
		self.ip_entry = thm.Entry(ip_frame)
		self.ip_entry.pack(fill = tk.X, side="left", padx = 10, expand = True)

		self.ip_button = thm.Button(ip_frame, text="OK", width=13, command = self.ip_connect)
		self.ip_button.pack(side="right")
		
		#Tạo Khung Frame
		function_frame = tk.Frame(self)
		function_frame.pack(fill=tk.BOTH, pady = 15, expand = True)

		function_frame1 = tk.Frame(function_frame)
		function_frame1.pack(side="right", fill = tk.BOTH, expand =True)

		function_frame2 = tk.Frame(function_frame1)
		function_frame2.pack(side="top", fill = tk.BOTH, expand = True, anchor = tk.NW)

		function_frame3 = tk.Frame(function_frame2)
		function_frame3.pack(side="left", fill=tk.BOTH, expand = True)

		function_frame4 = tk.Frame(function_frame3)
		function_frame4.pack(side="bottom", fill=tk.BOTH, expand = True, anchor = tk.W)

		function_frame5 = tk.Frame(function_frame1)
		function_frame5.pack(side="bottom", fill = tk.BOTH, expand = True)
		
		#Process Running

		self.process_running_button = thm.Button(function_frame, text="Process\nRunning", width=15, command=self.process_run)
		self.process_running_button.pack(side="left",fill = tk.Y, padx = 5, pady = 5)
		
		#App Running

		self.app_running_button = thm.Button(function_frame3, text = "App Running", width=30, command=self.listApp_run)
		self.app_running_button.pack(side="top", fill=tk.BOTH, padx = 5, pady = 5, expand = True)

		#Tắt máy

		self.shut_down_button = thm.Button(function_frame4, text = "Tắt\nmáy", width = 1, command=self.shut_down)
		self.shut_down_button.pack(side="left", fill=tk.BOTH, padx = 5, pady = 5, expand = True)
		
		#Chụp màn hình
		self.prt_screen_button = thm.Button(function_frame4, text = "Chụp màn hình", width = 15, command=self.screenshot)
		self.prt_screen_button.pack(side="right", fill=tk.BOTH, padx = 5, pady = 5, expand=True)
		
		#Key Log
		self.key_stroke_button = thm.Button(function_frame2, text = "Keystroke", width = 20, command=self.keylog_run)
		self.key_stroke_button.pack(side="right", fill=tk.BOTH, anchor = tk.NE, padx = 5, pady = 5)
		
		#Sửa registry

		self.regedit_button = thm.Button(function_frame5, text="Sửa registry", width=15, command = self.registry_run)
		self.regedit_button.pack(side="left", fill=tk.BOTH,padx = 5, pady = 5, expand = True)

		#Thoát
		self.exit_button = thm.Button(function_frame5, text="Thoát", width=10, command=self.parent.destroy)
		self.exit_button.pack(side="right", fill=tk.Y, padx = 5, pady = 5)

	#Kết nối đến địa chỉ IP
	def ip_connect(self):
		global ip_address
		ip_address = self.ip_entry.get()
		if ip_address == '':
			msbx.showwarning('', "Chưa nhập địa chỉ IP")
			return None
		self.tmp_client = client.Client
		self.tmp_client.host = ip_address
		self.tmp_client.port = 10000
		res = self.tmp_client.connect(self.tmp_client)
		self.status = res
		if res:
			msbx.showinfo("Kết nối đến Server", " Kết nối thành công.")
		else:
			msbx.showerror("Kết nối đến Server", "Kết nối thất bại.")
		
	#Process Run
	def process_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x426+50+50")
		self.app = process.process_frame(self.top)

	#listApp Run
	def listApp_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x426+100+100")
		self.app = listApp.listApp_frame(self.top)

	#Registry Run
	def registry_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("679x497+150+150")
		self.app = registry.reg_frame(self.top)

	#keylog_run
	def keylog_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x426+200+200")
		self.app = keylog.keylog_frame(self.top)

	#Chụp màn hình
	def screenshot(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x324+250+250")
		self.app = pic.pic_frame(self.top)

	#Shut down
	def shut_down(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.tmp_client.req_shutdown(self.tmp_client)
		msbx.showinfo("Shutdown", "Server đã shut down.")
		
root = tk.Tk()
root.geometry("582x426+10+10")
app = client_frame(root)
app.mainloop()