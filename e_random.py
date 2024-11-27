from tkinter import *
from tkinter import ttk, messagebox
from FAdo.fa import *  # FAdo automata library
from NFA_DFA import nfa_to_dfa  # Convert NFA to DFA
from RGX_NFA import regex_to_nfa  # Convert regex to NFA
from DFA_MIN import minimize_dfa  # Minimize DFA
import random

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer Generator Tool")
        self.root.geometry("600x500")
        self.minimized_dfa = None

        self.create_widgets()

    def create_widgets(self):
        # String Verification Section
        string_frame = Frame(self.root)
        string_frame.pack(pady=10, padx=10, fill="x")

        Label(string_frame, text="Input String:").grid(row=0, column=0, sticky=W, padx=5)
        self.string_entry = Entry(string_frame, width=30)
        self.string_entry.grid(row=0, column=1, padx=5)

        Button(string_frame, text="Check String", command=self.check_string).grid(row=0, column=2, padx=10)

        # Regex Input Section
        input_frame = Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        Label(input_frame, text="Regex:").grid(row=0, column=0, sticky=W, padx=5)
        self.regex_entry = Entry(input_frame, width=30)
        self.regex_entry.grid(row=0, column=1, padx=5)

        Label(input_frame, text="Max Length (Enumerated):").grid(row=1, column=0, sticky=W, padx=5)
        self.max_length_entry = Entry(input_frame, width=10)
        self.max_length_entry.grid(row=1, column=1, sticky=W, padx=5)
        self.max_length_entry.insert(0, "10")

        Label(input_frame, text="Max Steps (Random):").grid(row=2, column=0, sticky=W, padx=5)
        self.max_steps_entry = Entry(input_frame, width=10)
        self.max_steps_entry.grid(row=2, column=1, sticky=W, padx=5)
        self.max_steps_entry.insert(0, "10")

        Label(input_frame, text="Num Random Strings:").grid(row=3, column=0, sticky=W, padx=5)
        self.num_strings_entry = Entry(input_frame, width=10)
        self.num_strings_entry.grid(row=3, column=1, sticky=W, padx=5)
        self.num_strings_entry.insert(0, "5")

        # Buttons Section
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        Button(button_frame, text="Generate Strings", command=self.generate_strings).grid(row=0, column=0, padx=10)
        Button(button_frame, text="Show Graph", command=self.display_graph).grid(row=0, column=1, padx=10)

        # Output Section
        output_frame = Frame(self.root)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        Label(output_frame, text="Enumerated Strings:").grid(row=0, column=0, sticky=W, padx=5)
        self.enumerated_list = Listbox(output_frame, height=10)
        self.enumerated_list.grid(row=1, column=0, padx=5, sticky=N + S + E + W)

        Label(output_frame, text="Random Strings:").grid(row=0, column=1, sticky=W, padx=5)
        self.random_list = Listbox(output_frame, height=10)
        self.random_list.grid(row=1, column=1, padx=5, sticky=N + S + E + W)

        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_columnconfigure(1, weight=1)

        unaccepted_frame = Frame(root)
        unaccepted_frame.pack(pady=10, padx=10, fill="both", expand=True)

        Label(unaccepted_frame, text="Unaccepted Strings:").pack(anchor=W, padx=5)
        unaccepted_list = Listbox(unaccepted_frame, height=10)
        unaccepted_list.pack(padx=5, pady=5, fill="both", expand=True)

    def process_regex(self, regex, max_length, max_steps, num_strings):
        try:
            nfa = regex_to_nfa(regex)
            dfa = nfa_to_dfa(nfa)
            self.minimized_dfa = minimize_dfa(dfa)
            enumerated = self.enumerate_strings(self.minimized_dfa, max_length)
            randoms = self.generate_random_strings(self.minimized_dfa, max_steps, num_strings)
            return enumerated, randoms
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {e}")
            return None, None

    def enumerate_strings(self, dfa, max_length):
        results = []
        queue = [(dfa.Initial, "")]
        while queue:
            state, string = queue.pop(0)
            if state in dfa.Final:
                results.append(string)
            if len(string) < max_length:
                for symbol in dfa.Sigma:
                    next_state = dfa.delta[state].get(symbol)
                    if next_state:
                        queue.append((next_state, string + symbol))
        return results

    def generate_random_strings(self, dfa, max_steps, num_strings):
        random_strings = []
        while len(random_strings) < num_strings:
            state, generated = dfa.Initial, ""
            for _ in range(max_steps):
                if state in dfa.Final and random.random() < 0.5:
                    random_strings.append(generated)
                    break
                valid_transitions = [(s, dfa.delta[state][s]) for s in dfa.Sigma if s in dfa.delta[state]]
                if not valid_transitions:
                    break
                symbol, state = random.choice(valid_transitions)
                generated += symbol
        return random_strings

    def generate_strings(self):
        regex = self.regex_entry.get()
        max_length = int(self.max_length_entry.get())
        max_steps = int(self.max_steps_entry.get())
        num_strings = int(self.num_strings_entry.get())
        enumerated, randoms = self.process_regex(regex, max_length, max_steps, num_strings)

        self.enumerated_list.delete(0, END)
        self.random_list.delete(0, END)
        for string in enumerated:
            self.enumerated_list.insert(END, string)
        for string in randoms:
            self.random_list.insert(END, string)

    def check_string(self):
        if not self.minimized_dfa:
            messagebox.showerror("Error", "No DFA available.")
            return
        input_string = self.string_entry.get()
        state = self.minimized_dfa.Initial
        for symbol in input_string:
            state = self.minimized_dfa.delta[state].get(symbol)
            if state is None:
                messagebox.showinfo("Result", "String not accepted.")
                return
        if state in self.minimized_dfa.Final:
            messagebox.showinfo("Result", "String accepted!")
        else:
            messagebox.showinfo("Result", "String not accepted.")

    def display_graph(self):
        if self.minimized_dfa:
            self.minimized_dfa.display()
        else:
            messagebox.showerror("Error", "No DFA available.")


if __name__ == "__main__":
    root = Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()
