import os
import tkinter as tk
from tkinter.constants import NO, S
import tkinter.ttk as thm
from client import Client
import tkinter.filedialog as file_dlg
import tkinter.messagebox as msbx

class folder_tree(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.make_widget()
        self.parent.title("Cây thư mục")

    def make_widget(self):
        global nodes
        nodes = dict()
        
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        global tree
        tree = thm.Treeview(self.frame)
        # self.yScrollBar = thm.Scrollbar(self.frame, orient='vertical',command=self.tree.yview)
        # self.xScrollBar = thm.Scrollbar(self.frame, orient='horizontal',command=self.tree.xview)
        # self.tree.configure(yscroll=self.yScrollBar.set, xscroll=self.xScrollBar.set)
        tree.heading('#0', text="Cây thư mục", anchor="w")

        # self.tree.grid(row=0, column=0, sticky="nsew")
        # self.yScrollBar.grid(row=0, column=1, sticky='ns')
        # self.xScrollBar.grid(row=1, column=0, sticky='ew')

        tree.pack(fill=tk.BOTH, pady=10, padx=10, expand=True)

        self.drive = Client.req_dirtree_getdrives(self)

        for i in self.drive:
            self.insert_node('', i + "\\", i + "\\")
        self.rightClick = RightClick(self.parent)
        tree.bind('<<TreeviewOpen>>', self.open_node)
        tree.bind('<Button-3>', self.rightClick.popup)
        
    def insert_node(self, parent, text, abspath):
        node = tree.insert(parent, 'end', text=text, open=False)
        nodes[node] = abspath
        tree.insert(node, 'end')

    def open_node(self, event):
        node = tree.focus()
        abspath = nodes.pop(node, None)
        if abspath:
            tree.delete(tree.get_children(node))
            listDir = Client.req_dirtree_getfiles('', abspath)
            for p in listDir['folders']:
                self.insert_node(node, p, abspath + '\\' + p)
            for p in listDir['files']:
                self.insert_node(node, p, abspath + '\\' + p)

class RightClick:
    def __init__(self, parent):
            
        self.aMenu = tk.Menu(parent, tearoff = 0)
        self.aMenu.add_command(label="Xóa", command=self.delete)
        self.aMenu.add_command(label="Sao chép từ Server tới Client", command=self.copyServer2Client)
        self.aMenu.add_command(label="Sao chép từ Client tới Server", command=self.copyClient2Server)

        self.tree_item = ''

    def delete(self):
        abspath = nodes.pop(self.tree_item, None)
        if self.tree_item:
            res = Client.req_dirtree_deletefile(self, abspath)
            if res:
                tree.delete(self.tree_item)
                msbx.showinfo('Xóa', "Xóa thành công.")
            else:
                msbx.showinfo('Xóa', "Xóa thất bại")


    def copyServer2Client(self):
        abspath = nodes.pop(self.tree_item, None)
        save_path = file_dlg.askdirectory(title="Save to...")
        if abspath and save_path:
            res = Client.req_dirtree_server2client(self, abspath, save_path)
            if res:
                msbx.showinfo('Sao chép từ Server tới Client', "Đã sao chép thành công.")
            else:
                msbx.showinfo('Sao chép từ Server tới Client', "Không thế sao chép tập tin.")

    def copyClient2Server(self):
        abspath = nodes.pop(self.tree_item, None)
        file_path = file_dlg.askopenfilename(title="Select file to copy")
        if abspath and file_path:
            res = Client.req_dirtree_client2server(self, file_path, abspath)
            if res:
                msbx.showinfo('Sao chép từ CLient tới Server', "Đã sao chép thành công.")
            else:
                msbx.showinfo('Sao chép từ CLient tới Server', "Không thế sao chép tập tin.")


    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)
        self.tree_item = tree.focus()