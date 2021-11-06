import tkinter as tk, threading
import tkinter.ttk as thm
import tkinter.messagebox as msbx
import tkinter.filedialog as file_dlg
from PIL import Image, ImageTk
import pyautogui
import client
import imageio

class live_frame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		self.parent = parent
		self.pack(fill = tk.BOTH, expand = True)
		self.make_widgets()
		
		self.label = thm.Label(self.frame2)
		self.record = False
		self.tmp_client = client.Client
		self.parent.title("Chụp màn hình")

	def make_widgets(self):
		#Tạo các frame
		frame1 = tk.Frame(self)
		frame1.pack(fill=tk.BOTH, padx = 10, pady = 10, expand = True)	

		self.frame2 = tk.LabelFrame(frame1)
		self.frame2.pack(side = "left", fill = tk.BOTH, padx = 10, pady = 20, expand = True)
		
		frame3 = tk.Frame(frame1)
		frame3.pack(side = "right", fill = tk.Y)

		frame4 = tk.Frame(frame3)
		frame4.pack(fill = tk.Y, expand = True)

		frame5 = tk.Frame(frame3)
		frame5.pack(fill = tk.Y)

		#Tạo widgets
		self.shot = thm.Button(frame4, text="Bắt đầu quay", command=self.shot_image)
		self.shot.pack(fill=tk.BOTH, pady = 20, expand = True)

		self.save = thm.Button(frame5, text="Dừng quay", command=self.stop_record)
		self.save.pack(fill=tk.BOTH, ipady = 20, pady = 20, expand=True)

	def stream(self, label):

		self.record = True
		while self.record:
			img = self.tmp_client.req_get_screenshot(self.tmp_client)
			resized_img = img.resize((800, 450))
			frame_image = ImageTk.PhotoImage(resized_img)
			label.config(image = frame_image)
			label.image = frame_image

	def shot_image(self):
		self.label.pack()
		thread = threading.Thread(target=self.stream, args=(self.label,))
		thread.daemon = 1
		thread.start()
	

	def stop_record(self):
		self.record = False