# system includes
import tkinter as tk
from tkinter import ttk

# project includes
from handler import Handler

FONT = ("Arial", 14)
TITLE_FONT = ("Arial", 24, "bold")
TEAM_FONT = ("Arial", 16, "italic")


class Interface:
    def __init__(self, is_sample=False):
        self.handler = Handler()
        self.root = tk.Tk()
        self.root.title("Pokémon Team Planner")
        self.root.geometry("1280x720")

        self.pkmn_list = []
        self.is_sample = is_sample

        self.create_widgets()
        self.__post_init__()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, text="Pokémon Team Planner", font=TITLE_FONT
        )
        self.title_label.pack(pady=10)

        self.text_area = tk.Text(self.root, height=15, width=70, font=FONT)
        self.text_area.pack(pady=10)
        self.text_area.tag_configure("title", font=TITLE_FONT)
        self.text_area.tag_configure("team", justify="right", font=TEAM_FONT)
        self.text_area.configure(state="disabled")

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.input_field = tk.Entry(self.input_frame, width=15, font=FONT)
        self.input_field.grid(row=0, column=0, padx=5)
        self.input_field.focus_set()

        self.submit_button = tk.Button(
            self.input_frame, text="Submit", command=self.submit_input, font=FONT
        )
        self.submit_button.grid(row=0, column=1, padx=5)

        self.remove_button = tk.Button(
            self.input_frame, text="Remove", command=self.remove_last_pkmn, font=FONT
        )
        self.remove_button.grid(row=0, column=2, padx=5)

        self.root.bind("<Return>", self.submit_input)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)

        self.tables = []
        self.table_titles = []
        for i in range(6):
            table_title = tk.Label(self.table_frame, text=f"Table {i+1}", font=FONT)
            table_title.grid(row=0, column=i, padx=5)
            self.table_titles.append(table_title)

            table = ttk.Treeview(
                self.table_frame,
                columns=("Type", "Attacking", "Defending"),
                show="headings",
                height=6,
            )
            table.grid(row=1, column=i, padx=5)
            self.tables.append(table)

            table.column("Type", anchor="w", width=62)
            table.column("Attacking", anchor="center", width=62)
            table.column("Defending", anchor="center", width=62)

            table.heading("Type", text="Type")
            table.heading("Attacking", text="Attacking")
            table.heading("Defending", text="Defending")

        # Add an empty new table below the existing ones
        self.final_table_frame = tk.Frame(self.root)
        self.final_table_frame.pack(pady=15)

        final_table_title = tk.Label(self.final_table_frame, text="Team", font=FONT)
        final_table_title.pack()

        self.final_table = ttk.Treeview(
            self.final_table_frame,
            columns=("Type", "Attacking", "Defending"),
            show="headings",
            height=10,
        )
        self.final_table.pack(expand=True)

        self.final_table.column("Type", anchor="center", width=62)
        self.final_table.column("Attacking", anchor="center", width=62)
        self.final_table.column("Defending", anchor="center", width=62)

        self.final_table.heading("Type", text="Type")
        self.final_table.heading("Attacking", text="Attacking")
        self.final_table.heading("Defending", text="Defending")

        # Bind selection event to select corresponding rows
        self.final_table.bind("<<TreeviewSelect>>", self.on_final_table_select)

    def __post_init__(self):
        self.print_to_text_area("Please enter a Pokémon\n", tag="title")
        self.root.mainloop()

    def submit_input(self, event=None):
        user_input = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.refresh_text_area()

        if self.is_sample:
            self.pkmn_list = [
                "arcanine",
                "zekrom",
                "excadrill",
                "kyurem",
                "scrafty",
                "archeops",
            ]
            self.update_table()

        if not self.handler.pkmn_is_valid(user_input) and user_input != "":
            self.print_to_text_area(f"Invalid input: {user_input}\n")

        else:
            if len(self.pkmn_list) == 6:
                if user_input != "":
                    self.print_to_text_area(
                        f"You entered: {user_input}, but the team is full\n"
                    )

            else:
                self.print_to_text_area(f"You entered: {user_input}\n")
                self.pkmn_list.append(user_input)
                self.update_table()

    def print_to_text_area(self, message, tag=""):
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, message, tag)
        self.text_area.configure(state="disabled")

    def refresh_text_area(self):
        self.text_area.configure(state="normal")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Please enter a Pokémon\n", "title")
        self.text_area.configure(state="disabled")

    def update_table(self):
        self.show_team_interactions()
        self.show_final_team_interactions()

    def show_team_interactions(self):
        for pkmn in self.pkmn_list:
            self.show_interactions(pkmn)

    def show_final_team_interactions(self):
        team_interactions = self.handler.get_team_interactions(self.pkmn_list)

        if len(self.pkmn_list) == 6:
            is_complete = self.handler.is_complete(team_interactions)
            self.print_to_text_area(f"Team interactions: {is_complete}\n")

        # first delete the old table rows
        for row in self.final_table.get_children():
            self.final_table.delete(row)

        # now insert the new ones
        for key, value in team_interactions.items():
            self.final_table.insert("", tk.END, values=(key, value[0], value[1]))

    def show_interactions(self, pkmn: str):
        index = self.pkmn_list.index(pkmn)
        interactions = self.handler.get_pkmn_interactions(pkmn)

        # Update the table title with the Pokémon name
        text = pkmn[0].upper() + pkmn[1:]
        self.table_titles[index].configure(text=text)

        # first delete the old table rows
        for row in self.tables[index].get_children():
            self.tables[index].delete(row)

        # now insert the new ones
        for key, value in interactions.items():
            self.tables[index].insert("", tk.END, values=(key, value[0], value[1]))

    def on_final_table_select(self, event):
        selected_items = self.final_table.selection()
        selected_types = [
            self.final_table.item(item, "values")[0] for item in selected_items
        ]

        for table in self.tables:
            table.selection_remove(table.selection())
            for row in table.get_children():
                type_value = table.item(row, "values")[0]
                if type_value in selected_types:
                    table.selection_add(row)
                    table.see(row)  # Ensure the selected row is visible

    def remove_last_pkmn(self):
        if self.pkmn_list:
            self.pkmn_list.pop()

            for table in self.tables:
                for row in table.get_children():
                    table.delete(row)

            for i, table_title in enumerate(self.table_titles):
                table_title.configure(text=f"Table {i + 1}")

            self.refresh_text_area()
            self.update_table()
