import tkinter as tk
from tkinter import ttk, messagebox
import logging
from resource_identifier import ResourceIdentifier

# Define font constants
FONT_NAME = "Helvetica"
FONT_SIZE = 16
FONT = (FONT_NAME, FONT_SIZE)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TT Scanner Buddy")
        self.configure(bg="#2e2e2e")
        self.res_identifier = ResourceIdentifier()
        self.create_widgets()

    def create_widgets(self):
        # Frame for mining type selection
        frame_mining_type = ttk.Frame(self, padding=(10, 5), style="Dark.TFrame")
        frame_mining_type.pack(pady=10)
        label_mining_type = ttk.Label(frame_mining_type, text="Select Mining Type:", style="Dark.TLabel", font=FONT)
        label_mining_type.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.mining_type = tk.StringVar(value="Asteroid")
        radio_button_asteroid = ttk.Radiobutton(frame_mining_type, text="Asteroid", variable=self.mining_type,
                                                value="Asteroid", style="Dark.TRadiobutton")
        radio_button_asteroid.grid(row=0, column=1, padx=5)
        self.create_tooltip(radio_button_asteroid, "Select this option if the mining location is an asteroid.")

        radio_button_planet = ttk.Radiobutton(frame_mining_type, text="Planet", variable=self.mining_type,
                                              value="Planet", style="Dark.TRadiobutton")
        radio_button_planet.grid(row=0, column=2, padx=5)
        self.create_tooltip(radio_button_planet, "Select this option if the mining location is a planet.")

        # Frame for RS signature input
        frame_rs_signature = ttk.Frame(self, padding=(10, 5), style="Dark.TFrame")
        frame_rs_signature.pack(pady=10)
        label_rs_signature = ttk.Label(frame_rs_signature, text="Enter RS Signature:", style="Dark.TLabel", font=FONT)
        label_rs_signature.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.entry_rs_signature = ttk.Entry(frame_rs_signature, width=15, font=FONT)
        self.entry_rs_signature.grid(row=0, column=1, padx=10)
        self.entry_rs_signature.bind('<Return>', lambda event: self.on_identify_button_click())
        self.create_tooltip(self.entry_rs_signature, "Enter the RS signature. Press Enter or click 'Identify'.")

        # Frame for result display
        frame_result = ttk.Frame(self, padding=(10, 5), style="Dark.TFrame")
        frame_result.pack(pady=10)
        self.label_result = ttk.Label(frame_result, text="Result:", style="Dark.TLabel", font=FONT)
        self.label_result.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.treeview = ttk.Treeview(frame_result, columns=("Rock Type", "Quantity", "Prob Resource %"),
                                     show="headings", style="Dark.Treeview")
        self.treeview.heading("Rock Type", text="Rock Type", anchor=tk.W)
        self.treeview.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        self.treeview.heading("Prob Resource %", text="Prob Resource %", anchor=tk.W)
        self.treeview.column("Rock Type", width=150, anchor=tk.W)
        self.treeview.column("Quantity", width=100, anchor=tk.CENTER)
        self.treeview.column("Prob Resource %", width=300, anchor=tk.W)
        self.treeview.grid(row=1, column=0, padx=10, pady=5)

        # Configure treeview tag colors from both rock dictionaries
        for rock_name, (rock_value, color, resources) in {**self.res_identifier.asteroid_rock_values,
                                                            **self.res_identifier.planet_rock_values}.items():
            self.treeview.tag_configure(rock_name, foreground=color)
        self.treeview.tag_configure("error", foreground="red")
        self.treeview.tag_configure("resource", foreground="white")

        # Frame for Identify and Help buttons
        frame_buttons = ttk.Frame(self, padding=(10, 5), style="Dark.TFrame")
        frame_buttons.pack(pady=10)
        identify_button = ttk.Button(frame_buttons, text="Identify", command=self.on_identify_button_click,
                                     style="Dark.TButton", padding=(5, 10))
        identify_button.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(identify_button, "Click to identify the RS signature.")
        help_button = ttk.Button(frame_buttons, text="Help", command=self.on_help_button_click,
                                 style="Dark.TButton", padding=(5, 10))
        help_button.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(help_button, "Click for help and more information.")

        self.apply_styles()
        # Set the focus to the RS signature entry field on startup.
        self.entry_rs_signature.focus_set()

    def on_identify_button_click(self):
        rs_signature_str = self.entry_rs_signature.get()
        mining_location = self.mining_type.get()
        try:
            rs_signature = int(rs_signature_str)
        except ValueError:
            self.display_result("Unknown RS signature", rs_signature_str)
            return

        # Clear previous results
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        result = self.res_identifier.identify_resource(rs_signature, mining_location)
        if isinstance(result, str):
            self.treeview.insert("", "end", values=("", "", result), tags=("error",))
            self.label_result.config(text=f"Results for {rs_signature}:")
        else:
            for rock_name, num_rocks, resources in result:
                resources_lines = resources.split("\n")
                if resources_lines:
                    self.treeview.insert("", "end", values=(rock_name, num_rocks, resources_lines[0]), tags=(rock_name,))
                    for resource in resources_lines[1:]:
                        self.treeview.insert("", "end", values=("", "", resource), tags=("resource",))
                    self.treeview.insert("", "end", values=("", "", ""), tags=("resource",))
            self.label_result.config(text=f"Results for {rs_signature}:")
        self.entry_rs_signature.delete(0, tk.END)
        self.entry_rs_signature.focus_set()

    def display_result(self, message, signature):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        self.treeview.insert("", "end", values=("", "", message), tags=("error",))
        self.label_result.config(text=f"Results for {signature}:")
        self.entry_rs_signature.focus_set()

    def on_help_button_click(self):
        messagebox.showinfo("Help", "Enter an RS signature and select the mining location (Asteroid or Planet). Then click 'Identify' to determine the resource.")

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip_label = ttk.Label(tooltip, text=text, background="#ffffe0",
                                  relief='solid', borderwidth=1, wraplength=200, font=FONT)
        tooltip_label.pack(ipadx=1)
        tooltip.withdraw()

        def show_tooltip(event):
            x, y, cx, cy = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Dark.TFrame", background="#2e2e2e")
        style.configure("Dark.TLabel", background="#2e2e2e", foreground="white", font=FONT)
        style.configure("Dark.TRadiobutton", background="#2e2e2e", foreground="white", font=FONT)
        style.configure("Dark.TEntry", fieldbackground="#1e1e1e", foreground="white", font=FONT)
        style.configure("Dark.TButton", background="#3e3e3e", foreground="white", font=FONT)
        style.configure("Dark.Treeview", background="#1e1e1e", foreground="white",
                        fieldbackground="#1e1e1e", font=FONT)
        style.configure("Dark.Treeview.Heading", background="#3e3e3e", foreground="white", font=FONT)
        style.map("Dark.TRadiobutton",
                  background=[('active', '#2e2e2e')],
                  foreground=[('active', 'white')])
        style.configure("Dark.TRadiobutton", padding=(10, FONT_SIZE // 2))


if __name__ == '__main__':
    app = App()
    app.mainloop()
