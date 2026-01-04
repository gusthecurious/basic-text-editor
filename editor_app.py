import tkinter as tk
from tkinter import filedialog, messagebox
import os, json

class EditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Editor")
        self.root.state("zoomed")
        self.current_file = None

        self.setup_ui()
        self.restore_session()

    def run(self):
        self.root.mainloop()

    # ===================== FILE =====================

    def open_file(self):

        if not self.confirm_unsaved_changes():
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.text.edit_modified(False)

        self.current_file = file_path
        self.root.title(f"Editor - {os.path.basename(file_path)}")
        self.update_status()


    def confirm_unsaved_changes(self):
        if not self.text.edit_modified():
            return True  # nada para salvar

        response = messagebox.askyesnocancel(
            "Unsaved changes",
            "You have unsaved changes.\nDo you want to save them?"
        )
        if response is None:
            return False  
        elif response:
            self.save_file()
            return True
        else:
            return True 
        

    def save_file(self):
        if not self.current_file:
            self.save_as_file()
            return

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))
            self.text.edit_modified(False)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        self.current_file = file_path
        self.save_file()
        self.root.title(f"Editor - {os.path.basename(file_path)}")
    
    
    # ===================== UI =====================

    def setup_ui(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)

        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        self.show_status = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(
            label="Status Bar",
            variable=self.show_status,
            command=self.toggle_status_bar
        )

        # Themes menu
        theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=theme_menu)
        self.theme_var = tk.StringVar(value="Light")

        for theme_name in THEMES:
            theme_menu.add_radiobutton(
                label=theme_name,
                variable=self.theme_var,
                value=theme_name,
                command=lambda t=theme_name: self.apply_theme(t)
            )

        # Editor frame
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(fill="both", expand=True)

        # Text widget
        self.text = tk.Text(editor_frame, wrap="word", undo=True)
        self.text.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(editor_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Line 1, Column 0",
            anchor="w",
            relief="sunken",
            padx=10
        )
        self.status_bar.pack(side="bottom", fill="x")

        # Key bindings
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())

        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease>", self.update_status)

        self.apply_theme(self.theme_var.get())

    # ===================== EDIT =====================

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    # ===================== STATUS / THEME =====================

    def update_status(self, event=None):
        line, col = self.text.index(tk.INSERT).split(".")
        self.status_bar.config(text=f"Line {line}, Column {col}")

    def toggle_status_bar(self):
        if self.show_status.get():
            self.status_bar.pack(side="bottom", fill="x")
        else:
            self.status_bar.pack_forget()

    def apply_theme(self, theme_name):
        theme = THEMES[theme_name]

        self.root.config(bg=theme["bg"])
        self.text.config(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["insert"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["fg"]
        )
        self.status_bar.config(
            bg=theme["status_bg"],
            fg=theme["status_fg"]
        )

    # ===================== SESSION =====================

    def save_session(self):
        session = {"theme": self.theme_var.get()}
        with open("session.json", "w", encoding="utf-8") as f:
            json.dump(session, f)

    def restore_session(self):
        if not os.path.exists("session.json"):
            return

        with open("session.json", "r", encoding="utf-8") as f:
            session = json.load(f)
            self.theme_var.set(session.get("theme", "Light"))
            self.apply_theme(self.theme_var.get())

    def on_exit(self):
        if not self.confirm_unsaved_changes():
            return

        self.save_session()
        self.root.destroy()


THEMES = {
    "Light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "insert": "#000000",
        "select_bg": "#cce3ff",
        "status_bg": "#f0f0f0",
        "status_fg": "#000000"
    },
    "Dark": {
        "bg": "#1e1e1e",
        "fg": "#d4d4d4",
        "insert": "#ffffff",
        "select_bg": "#264f78",
        "status_bg": "#2d2d2d",
        "status_fg": "#ffffff"
    }
}

if __name__ == "__main__":
    app = EditorApp()
    app.run()
