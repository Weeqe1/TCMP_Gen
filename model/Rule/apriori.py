import csv
import re
import tkinter as tk
from tkinter import filedialog
from Rule.utils import *

# GUI
class fil_and_opt:
    def __init__(self, master):
        self.master = master
        master.title("TCMFG")

        # Input box1
        self.label1 = tk.Label(master, text="Set minimum support：")
        self.label1.grid(row=0, column=0, sticky="w")
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=0, column=1)

        # Input box2
        self.label2 = tk.Label(master, text="Set minimum confidence：")
        self.label2.grid(row=1, column=0, sticky="w")
        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=1, column=1)

        # Submit button
        self.button1 = tk.Button(master, text="submit", command=self.execute_data)
        self.button1.grid(row=2, column=0, columnspan=2, pady=10)

        # Display Results
        self.result_label = tk.Label(master, text="Association_rules：")
        self.result_label.grid(row=3, column=0, sticky="w")
        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2)

        # Set Text Box Properties
        self.result_text.configure(state='disabled', font=("Courier", 11))
        self.result_text.tag_configure("header", font=("Courier", 11, "bold"), justify='center')

    def open_file(self):
        file_path = filedialog.askopenfilename(title="select a .csv file", filetypes=[("CSV files", "*.csv")])

        if file_path:
            return file_path
        else:
            self.label.configure(text="counter a error!")

    def execute_data(self):

        def extract_strings(nested_list):
            flat_list = []
            for sublist in nested_list:
                for item in sublist:
                    if isinstance(item, str):
                        flat_list.append(item)
            return list(set(flat_list))

        def save_selected_items():
            global ecp
            ecp = [listbox.get(i) for i in listbox.curselection()]
            window.destroy()

        def select_all_items():
            listbox.select_set(0, tk.END)

        min_antecedent_support = float(self.entry1.get())
        min_consequent_support = float(self.entry1.get())
        min_confidence = float(self.entry2.get())

        with open(self.open_file(), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data_list = []
            for row in reader:
                data_row = []
                for cell in row:
                    pattern = re.compile(r'\(.*?\)')
                    cell = re.sub(pattern, '', cell)
                    cell = cell.strip('\ufeff \t\n\r')
                    if cell.strip():
                        data_row.append(cell.strip())
                data_list.append(data_row)

        frequent_itemsets = apri(data_list, min_antecedent_support)

        window = tk.Toplevel()
        window.title("Choose filter elements")
        window.geometry("600x600")

        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
        listbox.pack(fill=tk.BOTH, expand=True)

        ecp_elements = extract_strings(frequent_itemsets)

        for item in ecp_elements:
            listbox.insert(tk.END, item)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        select_all_button = tk.Button(window, text="Select All", command=select_all_items)
        select_all_button.pack()

        save_button = tk.Button(window, text="Save", command=save_selected_items)
        save_button.pack()
        window.wait_window()

        new_dic = delete_dict(ecp, frequent_itemsets)

        frequent_itemsets_df = pd.DataFrame(new_dic.items(), columns=['itemsets', 'support'])

        min_threshold = min_confidence

        filtered_df = association_filtered(
            association_rules(
                frequent_itemsets_df, min_threshold, metric="confidence"
            ), min_antecedent_support, min_consequent_support
        )

        result_str = filtered_df.to_string(index=False)
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result_str)
        self.result_text.configure(state='disabled')

        columns = "\n".join(filtered_df.columns.tolist())
        self.result_text.tag_add("header", "1.0", "1.end")
        self.result_text.insert("2.0", columns + "\n")
        self.result_text.tag_add("center", "2.0", "2.end")

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, filtered_df.to_string(index=False))

        frequent_itemsets_df.to_csv('data/out/frequent_itemsets.csv', encoding='gbk', index=False)
        filtered_df.to_csv('data/out/association_rules.csv', encoding='gbk', index=False)

if __name__ == '__main__':
    root = tk.Tk()
    gui = fil_and_opt(root)
    root.mainloop()

