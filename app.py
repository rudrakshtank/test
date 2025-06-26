import streamlit as st
from symspellpy.symspellpy import SymSpell, Verbosity
import os

st.set_page_config(page_title="SymSpell Spell Checker")

sym_spell = SymSpell(max_dictionary_edit_distance=3)

dictionary_path = "frequency_dictionary_en_82_765.txt"
if not os.path.exists(dictionary_path):
    st.error("Dictionary file not found.")
else:
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    st.title("🔍 Spell Checker using SymSpell")

    user_input = st.text_input("Enter a misspelled word here:")
    if user_input:
        suggestions = sym_spell.lookup(user_input, Verbosity.CLOSEST, max_edit_distance=3)
        if suggestions:
            st.write("Suggestions:")
            for suggestion in suggestions:
                st.write("→", suggestion.term)
        else:
            st.write("No suggestions found.")
