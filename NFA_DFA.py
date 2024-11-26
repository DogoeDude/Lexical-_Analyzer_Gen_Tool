from FAdo.fa import *  # Import FAdo automata library
from RGX_NFA import regex_to_nfa  # Import regex-to-NFA function

def nfa_to_dfa(nfa):
    try:
        # Convert the NFA to DFA
        dfa = nfa.toDFA()
        
        # Minimize the DFA
        minimized_dfa = dfa.minimal()
        
        return minimized_dfa
    except Exception as e:
        print(f"Error during NFA to DFA conversion: {e}")
        return None

if __name__ == "__main__":
    # Example regex
    regex = "a(bc)*"
    
    # Generate NFA from regex
    nfa = regex_to_nfa(regex)
    
    if nfa:
        # Convert NFA to DFA
        dfa = nfa_to_dfa(nfa)
        
        if dfa:
            print("Minimized DFA Generated from NFA:")
            dfa.display()  # Display DFA details

            # DFA States
            print("DFA States:", dfa.States)
            print("DFA Initial State:", dfa.Initial)
            print("DFA Final States:", dfa.Final)
            print("DFA Transitions:")
            for state in dfa.delta:
                for symbol, next_state in dfa.delta[state].items():
                    print(f"{state} --{symbol}--> {next_state}")
        else:
            print("Failed to generate DFA.")
    else:
        print("Failed to generate NFA.")
