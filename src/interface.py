"""
=======================================================================

 File: interface.py

 Description: Modernized Tkinter GUI for the Planner using ttkbootstrap.

=======================================================================
"""

# system includes
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

# project includes
from handler import Handler

FONT = ("Arial", 12)
TITLE_FONT = ("Arial", 20, "bold")


class Interface:
    def __init__(self, debug=False):
        self.handler = Handler()
        self.pkmn_list = []
        self.debug = debug
        self.current_theme = "cosmo"

        self.setup_window()
        self.create_widgets()
        self.__post_init__()

    def setup_window(self):
        self.root = tb.Window(themename=self.current_theme)
        self.root.title("Pokémon Team Planner")
        self.root.geometry("1400x800")
        self.style = tb.Style()

        # Create style instance once
        self.style = tb.Style()

        # Grid configuration for main layout
        self.root.columnconfigure(0, weight=1, minsize=300)  # Sidebar
        self.root.columnconfigure(1, weight=4)  # Main content
        self.root.rowconfigure(0, weight=1)

    def create_widgets(self):
        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        # Sidebar Frame
        self.sidebar = tb.Frame(self.root, padding=10, bootstyle="light")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Title
        title = tb.Label(self.sidebar, text="Team Planner", font=TITLE_FONT, bootstyle="primary")
        title.pack(pady=(10, 20), anchor="w")

        # Theme Toggle
        self.theme_btn = tb.Checkbutton(
            self.sidebar,
            text="Dark Mode",
            bootstyle="round-toggle",
            command=self.toggle_theme
        )
        self.theme_btn.pack(pady=(0, 20), anchor="w")

        # Input Section
        input_frame = tb.Labelframe(self.sidebar, text="Add Pokémon", padding=10)
        input_frame.pack(fill="x", pady=10)

        self.input_field = tb.Entry(input_frame, font=FONT)
        self.input_field.pack(fill="x", pady=5)
        self.input_field.focus_set()

        btn_frame = tb.Frame(input_frame)
        btn_frame.pack(fill="x", pady=5)

        self.submit_button = tb.Button(
            btn_frame,
            text="Add",
            command=self.submit_input,
            bootstyle="primary"
        )
        self.submit_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.remove_button = tb.Button(
            btn_frame,
            text="Remove",
            command=self.remove_last_pkmn,
            bootstyle="danger-outline"
        )
        self.remove_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.root.bind("<Return>", self.submit_input)

        # Status & Analysis Section
        analysis_frame = tb.Labelframe(self.sidebar, text="Status & Analysis", padding=10)
        analysis_frame.pack(fill="both", expand=True, pady=10)

        # Last Action Label
        tb.Label(analysis_frame, text="System Message:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.status_label = tb.Label(analysis_frame, text="Welcome!", font=("Arial", 10), wraplength=250, bootstyle="info")
        self.status_label.pack(anchor="w", pady=(0, 10))

        # Team Status
        tb.Label(analysis_frame, text="Team Status:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.team_status_label = tb.Label(analysis_frame, text="Incomplete", font=("Arial", 10))
        self.team_status_label.pack(anchor="w", pady=(0, 10))

        # Hard Problems
        tb.Label(analysis_frame, text="Hard Problems:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.hard_problems_label = tb.Label(analysis_frame, text="None", font=("Arial", 9), wraplength=250)
        self.hard_problems_label.pack(anchor="w", pady=(0, 10))

        # Soft Problems
        tb.Label(analysis_frame, text="Soft Problems:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.soft_problems_label = tb.Label(analysis_frame, text="None", font=("Arial", 9), wraplength=250)
        self.soft_problems_label.pack(anchor="w", pady=(0, 10))


    def create_main_content(self):
        self.main_frame = tb.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Pokemon Tables Grid
        self.table_container = tb.Frame(self.main_frame)
        self.table_container.pack(fill="both", expand=True)

        self.tables = []
        self.table_frames = [] # To hold title and table
        self.table_titles = []

        # Create 6 slots for Pokemon
        for i in range(6):
            frame = tb.LabelFrame(self.table_container, text=f"Slot {i+1}", padding=5)
            # Grid logic: 2 rows of 3
            row = i // 3
            col = i % 3
            frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            self.table_container.columnconfigure(col, weight=1)
            self.table_container.rowconfigure(row, weight=1)

            self.table_titles.append(frame) # keeping reference to change text later

            columns = ("Type", "Atk", "Def")
            table = tb.Treeview(
                frame,
                columns=columns,
                show="headings",
                height=5,
                bootstyle="info"
            )
            table.pack(fill="both", expand=True)
            self.tables.append(table)

            table.heading("Type", text="Type")
            table.heading("Atk", text="Atk")
            table.heading("Def", text="Def")

            table.column("Type", width=50, anchor="w")
            table.column("Atk", width=40, anchor="center")
            table.column("Def", width=40, anchor="center")

        # Final Team Summary
        summary_frame = tb.LabelFrame(self.main_frame, text="Team Summary", padding=10)
        summary_frame.pack(fill="x", pady=(20, 0))

        self.final_table = tb.Treeview(
            summary_frame,
            columns=("Type", "Atk", "Def"),
            show="headings",
            height=6,
            bootstyle="success"
        )
        self.final_table.pack(fill="x", expand=True)

        self.final_table.heading("Type", text="Type")
        self.final_table.heading("Atk", text="Atk")
        self.final_table.heading("Def", text="Def")

        self.final_table.column("Type", width=100, anchor="center")
        self.final_table.column("Atk", width=80, anchor="center")
        self.final_table.column("Def", width=80, anchor="center")

        # Bind selection
        self.final_table.bind("<<TreeviewSelect>>", self.on_final_table_select)

    def __post_init__(self):
        self.update_status("Please enter a Pokémon", "info")
        self.root.mainloop()

    def toggle_theme(self):
        if self.current_theme == "cosmo":
            self.current_theme = "darkly"
            self.sidebar.configure(bootstyle="secondary")
        else:
            self.current_theme = "cosmo"
            self.sidebar.configure(bootstyle="light")

        self.style.theme_use(self.current_theme)

    def submit_input(self, event=None):
        user_input = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)

        if self.debug and user_input == "debug": # Trigger debug team
            self.pkmn_list = [
                "arcanine", "scrafty", "excadrill",
                "archeops", "leavanny", "stoutland"
            ]
            self.update_table()
            self.update_status("Loaded debug team.", "success")
            return

        if not user_input:
            return

        if not self.handler.pkmn_is_valid(user_input):
            self.update_status(f"Invalid input: {user_input}", "danger")
        else:
            if len(self.pkmn_list) >= 6:
                self.update_status(f"Team is full! Cannot add {user_input}.", "warning")
            else:
                self.pkmn_list.append(user_input)
                self.update_status(f"Added {user_input}.", "success")
                self.update_table()

    def update_status(self, message, bootstyle="default"):
        self.status_label.configure(text=message, bootstyle=bootstyle)

    def update_table(self):
        self.show_team_interactions()
        self.show_final_team_interactions()

    def show_team_interactions(self):
        # Clear all tables first if list is empty or strictly update existing
        for i, table in enumerate(self.tables):
            # Clear table
            for row in table.get_children():
                table.delete(row)

            # Reset Title
            self.table_titles[i].configure(text=f"Slot {i+1}")

        for i, pkmn in enumerate(self.pkmn_list):
            interactions = self.handler.get_pkmn_interactions(pkmn)

            # Update title
            text = pkmn.capitalize()
            self.table_titles[i].configure(text=text)

            table = self.tables[i]
            for key, value in interactions.items():
                table.insert("", tk.END, values=(key, value[0], value[1]))

    def show_final_team_interactions(self):
        team_interactions = self.handler.get_team_interactions(self.pkmn_list)

        # Update Analysis Panel
        if len(self.pkmn_list) == 6:
            # Use the new structured data method
            data = self.handler.get_completion_data(team_interactions)

            # Update Status
            if data["status"] == "Complete!":
                status_color = "success"
            elif data["status"] == "Almost complete.":
                status_color = "warning"
            else:
                status_color = "danger"
            self.team_status_label.configure(text=data["status"], bootstyle=status_color)

            # Update Hard Problems
            if data["hard_problems"]:
                hard_text = "\n".join([f"{item[0]}: {item[1]}" for item in data["hard_problems"]])
                self.hard_problems_label.configure(text=hard_text, bootstyle="danger")
            else:
                self.hard_problems_label.configure(text="None", bootstyle="success")

            # Update Soft Problems
            if data["soft_problems"]:
                soft_text = "\n".join([f"{item[0]}: {item[1]}" for item in data["soft_problems"]])
                self.soft_problems_label.configure(text=soft_text, bootstyle="warning")
            else:
                self.soft_problems_label.configure(text="None", bootstyle="success")

        else:
            self.team_status_label.configure(text=f"Building ({len(self.pkmn_list)}/6)", bootstyle="info")
            self.hard_problems_label.configure(text="...", bootstyle="secondary")
            self.soft_problems_label.configure(text="...", bootstyle="secondary")

        # Populate Final Table
        for row in self.final_table.get_children():
            self.final_table.delete(row)

        for key, value in team_interactions.items():
            self.final_table.insert("", tk.END, values=(key, value[0], value[1]))

    def on_final_table_select(self, event):
        selected_items = self.final_table.selection()
        if not selected_items:
            return

        selected_types = [
            self.final_table.item(item, "values")[0] for item in selected_items
        ]

        for table in self.tables:
            table.selection_remove(table.selection())
            for row in table.get_children():
                type_value = table.item(row, "values")[0]
                if type_value in selected_types:
                    table.selection_add(row)
                    table.see(row)

    def remove_last_pkmn(self):
        if self.pkmn_list:
            removed = self.pkmn_list.pop()
            self.update_status(f"Removed {removed}.", "warning")
            self.update_table()
        else:
            self.update_status("Team is already empty.", "info")
