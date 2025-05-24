import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, font

# Use an absolute path and check before appending sys.path
import os
sys_path = os.path.abspath("./")
if sys_path not in sys.path:
    sys.path.append(sys_path)
from src.conf.models import ClientRecord, AirlineRecord, FlightRecord


def create_tab_buttons(parent, add_cmd, edit_cmd, del_cmd, exit_cmd=None):
    """Creates tab-level buttons for CRUD operations."""
    f = ttk.Frame(parent)
    f.pack(fill="x", pady=4, padx=8, anchor="w")
    ttk.Button(f, text="Add", command=add_cmd).pack(side="left", padx=4)
    ttk.Button(f, text="Edit Selected", command=edit_cmd).pack(side="left", padx=4)
    ttk.Button(f, text="Delete Selected", command=del_cmd).pack(side="left", padx=4)
    if exit_cmd is not None:
        ttk.Button(f, text="Exit", command=exit_cmd).pack(side="left", padx=25)


def create_client_table(parent):
    columns = (
        "id", "name", "address_line1", "address_line2", "address_line3",
        "city", "state", "zip_code", "country", "phone_number"
    )
    table = ttk.Treeview(parent, columns=columns, show="headings", selectmode='browse')
    for col in columns:
        table.heading(col, text=col.replace("_", " ").title())
        table.column(col, width=100, anchor="w")
    table.pack(expand=1, fill="both", padx=6, pady=(6, 0))
    return table


def create_airline_table(parent):
    columns = ("id", "company_name")
    table = ttk.Treeview(parent, columns=columns, show="headings", selectmode='browse')
    for col in columns:
        table.heading(col, text=col.replace("_", " ").title())
        table.column(col, width=180, anchor="w")
    table.pack(expand=1, fill="both", padx=6, pady=(6, 0))
    return table


def create_flight_table(parent):
    columns = ("client_id", "airline_id", "flight_date", "start_city", "end_city")
    table = ttk.Treeview(parent, columns=columns, show="headings", selectmode='browse')
    for col in columns:
        table.heading(col, text=col.replace("_", " ").title())
        table.column(col, width=120, anchor="w")
    table.pack(expand=1, fill="both", padx=6, pady=(6, 0))
    return table


class TravelAgentGUI:
    """Main application GUI for managing clients, airlines, and flights."""

    def __init__(self, record_manager, storage_manager):
        self.search_tab_update_results_table = None
        self.search_results_table = None
        self.search_tab = None
        self.flight_table = None
        self.airline_table = None
        self.client_table = None
        self.flight_tab = None
        self.airline_tab = None
        self.tabs = None
        self.client_tab = None
        self.record_manager = record_manager
        self.storage_manager = storage_manager

        # Loading records as dict of lists
        records = self.storage_manager.load_records()
        self.record_manager.set_records(records)

        self.root = tk.Tk()
        self.root.title("Travel Agent Record Management System")
        self.root.geometry("900x500")
        self.root.minsize(900, 500)
        self.set_theme()
        self.create_tabs()
        self.create_menu()
        self.refresh_all_tables()
        exit_font = font.Font(family="Arial", size=14, weight="bold")
        exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self.exit_application,
            bg="red",
            fg="white",
            font=exit_font,
        )
        exit_button.pack(pady=10, anchor="ne")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)


    def set_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        self.root.option_add('*Font', 'Arial 12')

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.client_tab = ttk.Frame(self.tabs)
        self.airline_tab = ttk.Frame(self.tabs)
        self.flight_tab = ttk.Frame(self.tabs)
        self.search_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.client_tab, text="Clients")
        self.tabs.add(self.airline_tab, text="Airlines")
        self.tabs.add(self.flight_tab, text="Flights")
        self.tabs.add(self.search_tab, text="Search")
        self.tabs.pack(expand=1, fill="both", padx=10, pady=10)

        self.client_table = create_client_table(self.client_tab)
        self.airline_table = create_airline_table(self.airline_tab)
        self.flight_table = create_flight_table(self.flight_tab)

        create_tab_buttons(self.client_tab, self.add_client, self.edit_selected_client, self.delete_selected_client, self.exit_application)
        create_tab_buttons(self.airline_tab, self.add_airline, self.edit_selected_airline, self.delete_selected_airline, self.exit_application)
        create_tab_buttons(self.flight_tab, self.add_flight, self.edit_selected_flight, self.delete_selected_flight, self.exit_application)

        self.create_search_tab_ui()

        # Auto-refresh search tab table upon switching to it
        def on_tab_changed(event):
            current_tab = event.widget.select()
            tab_text = event.widget.tab(current_tab, "text")
            if tab_text.lower() == "search":
                if hasattr(self, "search_tab_update_results_table") and self.search_tab_update_results_table:
                    self.search_tab_update_results_table()
        self.tabs.bind("<<NotebookTabChanged>>", on_tab_changed)

    def create_search_tab_ui(self):
        record_types = ["client", "airline", "flight"]
        fields = {
            "client": [
                "id", "name", "address_line1", "address_line2", "address_line3",
                "city", "state", "zip_code", "country", "phone_number"
            ],
            "airline": [
                "id", "company_name"
            ],
            "flight": [
                "client_id", "airline_id", "flight_date", "start_city", "end_city"
            ]
        }

        controls = ttk.Frame(self.search_tab)
        controls.pack(fill="x", pady=(15, 1), padx=25, anchor="n")

        ttk.Label(controls, text="Type:").pack(side="left", padx=(0, 5))
        type_var = tk.StringVar(value=record_types[0])
        cmb_type = ttk.Combobox(controls, values=record_types, textvariable=type_var, state="readonly", width=12)
        cmb_type.pack(side="left", padx=3)

        ttk.Label(controls, text="Field:").pack(side="left", padx=(20, 5))
        field_var = tk.StringVar(value=fields[record_types[0]][0])
        cmb_field = ttk.Combobox(controls, values=fields[record_types[0]], textvariable=field_var, state="readonly", width=18)
        cmb_field.pack(side="left", padx=3)

        ttk.Label(controls, text="Value:").pack(side="left", padx=(20, 5))
        entry_value = ttk.Entry(controls, width=18)
        entry_value.pack(side="left", padx=3)

        btn_search = ttk.Button(controls, text="Search")
        btn_search.pack(side="left", padx=(16, 0))

        results_frame = ttk.LabelFrame(self.search_tab, text="Results")
        results_frame.pack(fill="both", expand=True, padx=25, pady=16)
        self.search_results_table = None

        def update_results_table(rows=None):
            for widget in results_frame.winfo_children():
                widget.destroy()
            current_type = type_var.get()
            columns = fields[current_type]
            table = ttk.Treeview(results_frame, columns=columns, show="headings", selectmode='none')
            for col in columns:
                table.heading(col, text=col.replace("_", " ").title())
                table.column(col, width=120, anchor="center")
            table.pack(expand=1, fill="both", padx=7, pady=8)
            self.search_results_table = table
            if rows:
                for row in rows:
                    table.insert("", "end", values=[row.get(col, "") for col in columns])

        self.search_tab_update_results_table = update_results_table  # allow refresh externally

        update_results_table()
        def on_type_change(*_):
            current_type = type_var.get()
            cmb_field['values'] = fields[current_type]
            field_var.set(fields[current_type][0])
            update_results_table()
        type_var.trace_add("write", on_type_change)

        def do_search():
            table_rows = []
            current_type = type_var.get()
            selected_field = field_var.get()
            search_v = entry_value.get().strip().lower()
            for record in self.record_manager.display_records(current_type):
                rec_val = str(record.get(selected_field, "")).lower()
                if search_v and search_v not in rec_val:
                    continue
                table_rows.append(record)
            update_results_table(table_rows)
            if not table_rows:
                messagebox.showinfo("No Results", "No records match your search.", parent=self.root)
        btn_search.config(command=do_search)
        entry_value.bind("<Return>", lambda e: do_search())

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save_all_records, accelerator="Cmd+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_application, accelerator="Cmd+Q")
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        self.root.bind("<Command-s>", lambda e: self.save_all_records())
        self.root.bind("<Command-q>", lambda e: self.exit_application())

    def save_all_records(self):
        self.storage_manager.save_records(self.record_manager.records)

    # --------- Client CRUD ---------
    def add_client(self):
        self.show_client_form()

    def edit_selected_client(self):
        sel = self.client_table.selection()
        if not sel:
            messagebox.showinfo("Edit Client", "Please select a client to edit.", parent=self.root)
            return
        values = self.client_table.item(sel[0], "values")
        self.show_client_form(initial=values)

    def delete_selected_client(self):
        sel = self.client_table.selection()
        if not sel:
            messagebox.showinfo("Delete Client", "Please select a client to delete.", parent=self.root)
            return
        values = self.client_table.item(sel[0], "values")
        try:
            client_id = int(values[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid client selection.", parent=self.root)
            return
        answer = messagebox.askyesno("Confirm Delete", f"Delete client with ID={client_id} ({values[1]})?", parent=self.root)
        if answer:
            self.record_manager.delete_record("client", client_id)
            self.save_all_records()
            self.refresh_all_tables()
            self.root.focus_force()

    def show_client_form(self, initial=None):
        form = tk.Toplevel(self.root)
        form.title("Add Client" if initial is None else "Edit Client")
        fields = [
            ("ID", int),
            ("Name", str),
            ("Address Line 1", str),
            ("Address Line 2", str),
            ("Address Line 3", str),
            ("City", str),
            ("State", str),
            ("Zip Code", str),
            ("Country", str),
            ("Phone Number", str)
        ]
        entries = {}

        for idx, (label, typ) in enumerate(fields):
            ttk.Label(form, text=f"{label}:").grid(row=idx, column=0, sticky="w", pady=2, padx=8)
            ent = ttk.Entry(form, width=30)
            ent.grid(row=idx, column=1, pady=2, padx=8)
            if initial:
                ent.insert(0, initial[idx])
            if idx == 0 and initial is not None:
                ent.config(state="readonly")
            entries[label] = ent

        def validate_fields():
            for label, typ in fields:
                val = entries[label].get().strip()
                if not val:
                    return False
                if typ is int and not val.isdigit():
                    return False
            return True

        def on_submit(event=None):
            if not validate_fields():
                messagebox.showwarning("Validation", "Please fill all fields correctly.", parent=form)
                return
            try:
                vals = [entries[f[0]].get().strip() for f in fields]
                obj = ClientRecord(
                    int(vals[0]), vals[1], vals[2], vals[3], vals[4], vals[5], vals[6],
                    vals[7], vals[8], vals[9]
                )
                if initial:
                    self.record_manager.update_record("client", int(vals[0]), obj.to_dict())
                else:
                    self.record_manager.create_record(obj)
                self.storage_manager.save_records(self.record_manager.records)
                self.refresh_all_tables()
                form.destroy()
                self.root.focus_force()
            except Exception as e:
                messagebox.showwarning("Error", f"Error: {e}", parent=form)
        btn_text = "Update" if initial else "Add"
        action_btn = ttk.Button(form, text=btn_text, command=on_submit)
        action_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)
        form.bind("<Return>", on_submit)
        form.bind("<Escape>", lambda e: form.destroy())
        form.focus_set()
        form.grab_set()
        self.center_toplevel(form)

    # --------- Airline CRUD ---------
    def add_airline(self):
        self.show_airline_form()

    def edit_selected_airline(self):
        sel = self.airline_table.selection()
        if not sel:
            messagebox.showinfo("Edit Airline", "Please select an airline to edit.", parent=self.root)
            return
        values = self.airline_table.item(sel[0], "values")
        self.show_airline_form(initial=values)

    def delete_selected_airline(self):
        sel = self.airline_table.selection()
        if not sel:
            messagebox.showinfo("Delete Airline", "Please select an airline to delete.", parent=self.root)
            return
        values = self.airline_table.item(sel[0], "values")
        try:
            airline_id = int(values[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid airline selection.", parent=self.root)
            return
        company_name = values[1]
        answer = messagebox.askyesno("Confirm Delete", f"Delete airline ID={airline_id} ({company_name})?", parent=self.root)
        if answer:
            self.record_manager.delete_record("airline", airline_id)
            self.save_all_records()
            self.refresh_all_tables()
            self.root.focus_force()


    def show_airline_form(self, initial=None):
        form = tk.Toplevel(self.root)
        form.title("Add Airline" if initial is None else "Edit Airline")
        fields = [
            ("ID", int),
            ("Company Name", str)
        ]
        entries = {}
        for idx, (label, typ) in enumerate(fields):
            ttk.Label(form, text=f"{label}:").grid(row=idx, column=0, sticky="w", pady=2, padx=8)
            ent = ttk.Entry(form, width=30)
            ent.grid(row=idx, column=1, pady=2, padx=8)
            if initial:
                ent.insert(0, initial[idx])
            if idx == 0 and initial is not None:
                ent.config(state="readonly")
            entries[label] = ent

        def validate_fields():
            for label, typ in fields:
                val = entries[label].get().strip()
                if not val:
                    return False
                if typ is int and not val.isdigit():
                    return False
            return True

        def on_submit(event=None):
            if not validate_fields():
                messagebox.showwarning("Validation", "Please fill all fields.", parent=form)
                return
            try:
                airline = AirlineRecord(int(entries["ID"].get()), entries["Company Name"].get().strip())
                if initial:
                    self.record_manager.update_record("airline", airline.id, airline.to_dict())
                else:
                    self.record_manager.create_record(airline)
                self.save_all_records()
                self.refresh_all_tables()
                form.destroy()
                self.root.focus_force()
            except Exception as e:
                messagebox.showwarning("Error", f"Error: {e}", parent=form)
        btn_text = "Update" if initial else "Add"
        action_btn = ttk.Button(form, text=btn_text, command=on_submit)
        action_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)
        form.bind("<Return>", on_submit)
        form.bind("<Escape>", lambda e: form.destroy())
        form.focus_set()
        form.grab_set()
        self.center_toplevel(form)

   # --------- Flight CRUD ---------
    def add_flight(self):
        self.show_flight_form()

    def edit_selected_flight(self):
        sel = self.flight_table.selection()
        if not sel:
            messagebox.showinfo("Edit Flight", "Please select a flight to edit.", parent=self.root)
            return
        values = self.flight_table.item(sel[0], "values")
        self.show_flight_form(initial=values)

    def delete_selected_flight(self):
        sel = self.flight_table.selection()
        if not sel:
            messagebox.showinfo("Delete Flight", "Please select a flight to delete.", parent=self.root)
            return
        row = self.flight_table.item(sel[0], "values")
        msg = (
            f"Delete flight with Client ID: {row[0]}, Airline ID: {row[1]}, "
            f"Date: {row[2]}, {row[3]} - {row[4]} ?"
        )
        answer = messagebox.askyesno("Confirm Delete", msg, parent=self.root)
        if answer:
            composite = {
                "client_id": int(row[0]),
                "airline_id": int(row[1]),
                "flight_date": row[2],
                "start_city": row[3],
                "end_city": row[4]
            }
            self.record_manager.delete_record("flight", composite)
            self.save_all_records()
            self.refresh_all_tables()
            self.root.focus_force()

    def show_flight_form(self, initial=None):
        form = tk.Toplevel(self.root)
        form.title("Add Flight" if initial is None else "Edit Flight")
        fields = [
            ("Client_ID", int),
            ("Airline_ID", int),
            ("Date (YYYY-MM-DD)", str),
            ("Start City", str),
            ("End City", str)
        ]
        entries = {}
        for idx, (label, typ) in enumerate(fields):
            ttk.Label(form, text=f"{label}:").grid(row=idx, column=0, sticky="w", pady=2, padx=8)
            ent = ttk.Entry(form, width=30)
            ent.grid(row=idx, column=1, pady=2, padx=8)
            if initial:
                ent.insert(0, initial[idx])
            if idx in (0, 1) and initial is not None:
                ent.config(state="readonly")
            entries[label] = ent

        def validate_fields():
            try:
                _cd = entries["Client_ID"].get().strip()
                _ad = entries["Airline_ID"].get().strip()
                _dt = entries["Date (YYYY-MM-DD)"].get().strip()
                if not _cd or not _ad or not _dt: return False
                if not _cd.isdigit() or not _ad.isdigit(): return False
                datetime.strptime(_dt, "%Y-%m-%d")
                if not entries["Start City"].get().strip() or not entries["End City"].get().strip(): return False
                return True
            except Exception:
                return False

        def on_submit(event=None):
            if not validate_fields():
                messagebox.showwarning("Validation", "Please enter all fields correctly.", parent=form)
                return
            try:
                client_id = int(entries["Client_ID"].get())
                airline_id = int(entries["Airline_ID"].get())
                flight_date = entries["Date (YYYY-MM-DD)"].get().strip()
                start_city = entries["Start City"].get().strip()
                end_city = entries["End City"].get().strip()
                flight = FlightRecord(client_id, airline_id, flight_date, start_city, end_city)
                flight_dict = flight.to_dict()
                if initial:
                    composite = {
                        "client_id": int(initial[0]),
                        "airline_id": int(initial[1]),
                        "flight_date": initial[2],
                        "start_city": initial[3],
                        "end_city": initial[4],
                    }
                    self.record_manager.update_record("flight", composite, flight_dict)
                else:
                    self.record_manager.create_record(flight)
                self.save_all_records()
                self.refresh_all_tables()
                form.destroy()
                self.root.focus_force()
            except Exception as e:
                messagebox.showwarning("Error", f"Error: {e}", parent=form)
        btn_text = "Update" if initial else "Add"
        action_btn = ttk.Button(form, text=btn_text, command=on_submit)
        action_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)
        form.bind("<Return>", on_submit)
        form.bind("<Escape>", lambda e: form.destroy())
        form.focus_set()
        form.grab_set()
        self.center_toplevel(form)

    # ------- Table Refresh -------
    def refresh_all_tables(self):
        self.refresh_table(self.client_table, "client")
        self.refresh_table(self.airline_table, "airline")
        self.refresh_table(self.flight_table, "flight")

    def refresh_table(self, table, type_name):
        for item in table.get_children():
            table.delete(item)
        records = self.record_manager.display_records(type_name)
        for record in records:
            if type_name == "client":
                table.insert(
                    "", "end",
                    values=(record.get("id"), record.get("name"), record.get("address_line1"),
                            record.get("address_line2"), record.get("address_line3"), record.get("city"),
                            record.get("state"), record.get("zip_code"), record.get("country"),
                            record.get("phone_number")))
            elif type_name == "airline":
                table.insert(
                    "", "end",
                    values=(record.get("id"), record.get("company_name")))
            elif type_name == "flight":
                table.insert(
                    "", "end",
                    values=(record.get("client_id"), record.get("airline_id"), record.get("flight_date"),
                            record.get("start_city"), record.get("end_city")))

            # Optionally, else: log or handle unexpected types if needed

    def exit_application(self):
        self.save_all_records()
        self.root.destroy()

    def run(self):
        """Starts the GUI event loop."""
        self.root.mainloop()

    def center_toplevel(self, toplevel):
        """Centers a toplevel window on the screen."""
        toplevel.update_idletasks()
        w = toplevel.winfo_width()
        h = toplevel.winfo_height()
        ws = toplevel.winfo_screenwidth()
        hs = toplevel.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        toplevel.geometry(f'+{x}+{y}')