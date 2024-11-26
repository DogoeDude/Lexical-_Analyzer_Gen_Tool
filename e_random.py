from tkinter import *
from tkinter import ttk, messagebox
from FAdo.fa import *  # FAdo automata library
from NFA_DFA import nfa_to_dfa  # Convert NFA to DFA
from RGX_NFA import regex_to_nfa  # Convert regex to NFA
from DFA_MIN import minimize_dfa  # Minimize DFA
import random

def enumerate_strings(dfa, max_length):
    results = []
    queue = [(dfa.Initial, "")]  # (current state, current string)

    while queue:
        current_state, current_string = queue.pop(0)
        if current_state in dfa.Final:
            results.append(current_string)
        if len(current_string) < max_length:
            for symbol in dfa.Sigma:
                next_state = dfa.delta[current_state].get(symbol, None)
                if next_state is not None:
                    queue.append((next_state, current_string + symbol))
    return results

def generate_random_strings(dfa, max_steps, num_strings=5):
    random_strings = []
    while len(random_strings) < num_strings:
        current_state = dfa.Initial
        generated_string = ""
        while len(generated_string) < max_steps:
            if current_state in dfa.Final and random.random() < 0.5:
                random_strings.append(generated_string)
                break
            valid_transitions = [
                (symbol, dfa.delta[current_state][symbol])
                for symbol in dfa.Sigma
                if symbol in dfa.delta[current_state]
            ]
            if not valid_transitions:
                break
            symbol, next_state = random.choice(valid_transitions)
            generated_string += symbol
            current_state = next_state
        if current_state in dfa.Final and generated_string not in random_strings:
            random_strings.append(generated_string)
    return random_strings


def process_regex(regex, max_length, max_steps, num_strings):
    global minimized_dfa
    nfa = regex_to_nfa(regex)
    if not nfa:
        messagebox.showerror("Error", "Failed to generate NFA from regex.")
        return None
    dfa = nfa_to_dfa(nfa)
    if not dfa:
        messagebox.showerror("Error", "Failed to convert NFA to DFA.")
        return None
    minimized_dfa = minimize_dfa(dfa)
    if not minimized_dfa:
        messagebox.showerror("Error", "Failed to minimize DFA.")
        return None
    enumerated = enumerate_strings(minimized_dfa, max_length)
    randoms = generate_random_strings(minimized_dfa, max_steps, num_strings)
    return enumerated, randoms

def generate_strings():
    regex = regex_entry.get()
    max_length = int(max_length_entry.get())
    max_steps = int(max_steps_entry.get())
    num_strings = int(num_strings_entry.get())
    try:
        enumerated, randoms = process_regex(regex, max_length, max_steps, num_strings)
        enumerated_list.delete(0, END)
        random_list.delete(0, END)
        for string in enumerated:
            enumerated_list.insert(END, string)
        for string in randoms:
            random_list.insert(END, string)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def display_graph():
    if minimized_dfa:
        minimized_dfa.display()
    else:
        messagebox.showerror("Error", "No DFA available to display.")


# Initialize GUI
root = Tk()
root.title("Lexical Analyzer Generator Tool")
root.geometry("600x400")

# Input Section
input_frame = Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")

Label(input_frame, text="Regex:").grid(row=0, column=0, sticky=W, padx=5)
regex_entry = Entry(input_frame, width=30)
regex_entry.grid(row=0, column=1, padx=5)

Label(input_frame, text="Max Length (Enumerated):").grid(row=1, column=0, sticky=W, padx=5)
max_length_entry = Entry(input_frame, width=10)
max_length_entry.grid(row=1, column=1, sticky=W, padx=5)

Label(input_frame, text="Max Steps (Random):").grid(row=2, column=0, sticky=W, padx=5)
max_steps_entry = Entry(input_frame, width=10)
max_steps_entry.grid(row=2, column=1, sticky=W, padx=5)

Label(input_frame, text="Num Random Strings:").grid(row=3, column=0, sticky=W, padx=5)
num_strings_entry = Entry(input_frame, width=10)
num_strings_entry.grid(row=3, column=1, sticky=W, padx=5)

# Buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

generate_button = Button(button_frame, text="Generate Strings", command=generate_strings)
generate_button.grid(row=0, column=0, padx=10)

graph_button = Button(button_frame, text="Show Graph", command=display_graph)
graph_button.grid(row=0, column=1, padx=10)

# Output Section
output_frame = Frame(root)
output_frame.pack(pady=10, padx=10, fill="both", expand=True)

Label(output_frame, text="Enumerated Strings:").grid(row=0, column=0, sticky=W, padx=5)
enumerated_list = Listbox(output_frame, height=10)
enumerated_list.grid(row=1, column=0, padx=5, sticky=N + S + E + W)

Label(output_frame, text="Random Strings:").grid(row=0, column=1, sticky=W, padx=5)
random_list = Listbox(output_frame, height=10)
random_list.grid(row=1, column=1, padx=5, sticky=N + S + E + W)

output_frame.grid_rowconfigure(1, weight=1)
output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_columnconfigure(1, weight=1)

# Main loop
root.mainloop()
