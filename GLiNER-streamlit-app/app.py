import streamlit as st
from gliner import GLiNER
import random
from annotated_text import annotated_text

# Predefined list of colors
COLOR_LIST = [
    "#FFB6C1", "#B0E0E6", "#FAFAD2", "#FFDAB9", 
    "#E6E6FA", "#E0FFFF", "#F5DEB3", "#98FB98", 
    "#FFE4E1", "#D8BFD8"
]


# Function to assign random colors to entity types
def get_entity_colors(entities):
    unique_labels = set(ent['label'] for ent in entities)
    entity_colors = {label: random.choice(COLOR_LIST) for label in unique_labels}
    return entity_colors

# Function to render entities using st-annotated-text
def render_entities(text, entities):
    entity_colors = get_entity_colors(entities)
    annotated_text_list = []
    current_pos = 0

    for ent in entities:
        if current_pos < ent['start']:
            annotated_text_list.append(text[current_pos:ent['start']])
        annotated_text_list.append((text[ent['start']:ent['end']], ent['label']))
        current_pos = ent['end']

    if current_pos < len(text):
        annotated_text_list.append(text[current_pos:])

    annotated_text(*annotated_text_list)

# Load GLiNER model
@st.cache_resource
def load_model():
    return GLiNER.from_pretrained("gliner-community/gliner_small-v2.5")

model = load_model()

# Streamlit app layout
st.title("GLiNER Named Entity Recognition Demo")
st.write("Enter text and labels to extract named entities.")

# Input for the text
text_input = st.text_area("Enter Text:", "Cristiano Ronaldo plays for Al Nassr and the Portugal national team.")

# Input for the labels
labels_input = st.text_input("Enter Labels (comma separated):", "person, team, nationality")

# Convert the comma-separated labels into a list
labels = [label.strip() for label in labels_input.split(",")]

# Perform entity prediction
if st.button("Extract Entities"):
    if text_input and labels:
        entities = model.predict_entities(text_input, labels)
        st.write("### Annotated Text")
        render_entities(text_input, entities)
    else:
        st.write("Please enter both text and labels.")
