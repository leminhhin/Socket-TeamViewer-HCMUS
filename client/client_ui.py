import tkinter as tk
import tkinter.ttk as thm
import tkinter.messagebox as msbx
import client
import process
import listApp
import registry
import keylog
import pic
import liveScreen
import folderTree

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
		self.ip_frame = tk.Frame(self)
		self.ip_frame.pack(fill=tk.X)
		
		ip_label = thm.Label(self.ip_frame, text="Nhập địa chỉ IP:", width=15)
		ip_label.pack(side="left")
		
		self.ip_entry = thm.Entry(self.ip_frame)
		self.ip_entry.pack(fill = tk.X, side="left", padx = 10, expand = True)

		self.ip_button = thm.Button(self.ip_frame, text="OK", width=13, command = self.ip_connect)
		self.ip_button.pack(side="right")

		self.ipAddr_frame = tk.Frame(self)
		self.ipAddr_frame.pack(fill = tk.X)

		self.ipAddr_label = thm.Label(self.ipAddr_frame, text = "Đã kết nối đến địa chỉ IP: Chưa kết nối")
		self.ipAddr_label.pack(fill = tk.X, side="bottom", padx = 5, pady = 5, expand = True)
		
		#Tạo Khung Frame
		function_frame = tk.Frame(self)
		function_frame.pack(fill=tk.BOTH, pady = 15, expand = True)

		function_frame1 = tk.LabelFrame(function_frame, text="Quản lý hệ thống", width=1)
		function_frame1.pack(side = "left", fill=tk.BOTH, expand = True)

		function_frame2 = tk.LabelFrame(function_frame, text="Quản lý nhập liệu và hiển thị", width=1)
		function_frame2.pack(side = "left",fill=tk.BOTH, expand = True)

		function_frame3 = tk.LabelFrame(function_frame, text="Phần cứng và thoát ", width=1)
		function_frame3.pack(side = "left",fill=tk.BOTH, expand = True)
		
		#Process Running

		self.process_running_button = thm.Button(function_frame1, text="Process Running", command=self.process_run)
		self.process_running_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		
		#App Running

		self.app_running_button = thm.Button(function_frame1, text = "App Running", command=self.listApp_run)
		self.app_running_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Tắt máy

		self.shut_down_button = thm.Button(function_frame3, text = "Tắt máy", command=self.shut_down)
		self.shut_down_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Log out

		self.log_out_button = thm.Button(function_frame3, text = "Log out", command=self.log_out)
		self.log_out_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		
		#Chụp màn hình
		self.prt_screen_button = thm.Button(function_frame2, text = "Chụp màn hình", command=self.screenshot)
		self.prt_screen_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Live màn hình
		self.screen_live_button = thm.Button(function_frame2, text = "Live màn hình", command=self.record_screen)
		self.screen_live_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		
		#Key Log
		self.key_stroke_button = thm.Button(function_frame2, text = "Keystroke", command=self.keylog_run)
		self.key_stroke_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
		
		#Sửa registry

		self.regedit_button = thm.Button(function_frame1, text="Sửa registry", command = self.registry_run)
		self.regedit_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Xem địa chỉ MAC

		self.get_macAddr = thm.Button(function_frame3, text="Xem địa chỉ MAC", command = self.getMAC_run)
		self.get_macAddr.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Cây thư mục

		self.explorer = thm.Button(function_frame1, text="Cây thư mục", command = self.folderTree_run)
		self.explorer.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		##Khoá bàn phí11

		self.lock_keyboard_text = tk.StringVar()
		self.lock_keyboard_text.set("Khoá bàn phím")
		self.lock_keyboard = thm.Button(function_frame2, textvariable = self.lock_keyboard_text, command = self.lockKeyboard_run)
		self.lock_keyboard.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		#Thoát
		self.exit_button = thm.Button(function_frame3, text="Thoát", command=self.parent.destroy)
		self.exit_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
			self.ipAddr_label.config(text = "Đã kết nối đến địa chỉ IP: " + ip_address)
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

	#getMAC Run
	def getMAC_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		MAC_addr = client.Client.req_mac_address(self)
		msbx.showinfo("Get MAC Address", "Địa chỉ MAC của Server là: " + MAC_addr.upper())

	def lockKeyboard_run(self):

		if self.lock_keyboard_text.get() == "Khoá bàn phím":
			client.Client.req_lock_keyboard(self)
			msbx.showinfo("Khóa bàn phím", "Đã khoá bàn phím.")
			self.lock_keyboard_text.set("Mở khoá bàn phím")
			return None

		if self.lock_keyboard_text.get() == "Mở khoá bàn phím":
			client.Client.req_unlock_keyboard(self)
			msbx.showinfo("Mở khóa bàn phím", "Đã mở khoá bàn phím.")
			self.lock_keyboard_text.set("Khoá bàn phím")
			return None

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

    #Ghi màn hình
	def record_screen(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("950x528+250+250")
		self.app = liveScreen.live_frame(self.top)

	#Shut down
	def log_out(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.tmp_client.req_logout(self.tmp_client)
		msbx.showinfo("Logout", "Đã log out.")
		self.ipAddr_label.destroy()

	#Shut down
	def shut_down(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.tmp_client.req_shutdown(self.tmp_client)
		msbx.showinfo("Shutdown", "Server đã shut down.")
		self.ipAddr_label.destroy()

	def folderTree_run(self):
		if not self.status:
			msbx.showerror("Kết nối đến Server", "Chưa kết nối đến Server.")
			return None
		self.top = tk.Toplevel(self.parent)
		self.top.geometry("582x324+250+250")
		self.app = folderTree.folder_tree(self.top)

root = tk.Tk()
root.geometry("679x497")
app = client_frame(root)
app.mainloop()