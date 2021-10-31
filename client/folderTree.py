import os
from posixpath import abspath
import tkinter as tk
import tkinter.ttk as thm

class folder_tree(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.make_widget()
        self.parent.title("Cây thư mục")

    def make_widget(self):
        self.nodes = dict()
        
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.tree = thm.Treeview(self.frame)
        # self.yScrollBar = thm.Scrollbar(self.frame, orient='vertical',command=self.tree.yview)
        # self.xScrollBar = thm.Scrollbar(self.frame, orient='horizontal',command=self.tree.xview)
        # self.tree.configure(yscroll=self.yScrollBar.set, xscroll=self.xScrollBar.set)
        self.tree.heading('#0', text="Cây thư mục", anchor="w")

        # self.tree.grid(row=0, column=0, sticky="nsew")
        # self.yScrollBar.grid(row=0, column=1, sticky='ns')
        # self.xScrollBar.grid(row=1, column=0, sticky='ew')

        self.tree.pack(fill=tk.BOTH, pady=10, padx=10, expand=True)

        self.abspath = os.path.abspath("\\")
        self.insert_node('', self.abspath, self.abspath)
        self.rightClick = RightClick(self.parent)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind('<Button-3>', self.rightClick.popup)
        
    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

class RightClick:
    def __init__(self, parent):
        
        self.aMenu = tk.Menu(parent, tearoff = 0)
        self.aMenu.add_command(label="Delete", command=self.delete)
        self.aMenu.add_command(label="Copy", command=self.copy)

        self.tree_item = ''

    def delete(self):
        if self.tree_item:
            app.tree.delete(self.tree_item)

    def copy(self):
        print("Copying...")

    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)
        self.tree_item = app.tree.focus()

root = tk.Tk()
root.geometry("679x497")
app = folder_tree(root)
app.mainloop()