from ltn_mapping import *
import os
from ltn_mapping_colors import cnames

def main():
    # Gets user arguments one at a time TODO - add validation
    center_midi_value = int(input("""What would you like to set as your MIDI value for the center of the keyboard?
(Note: The "center" of the keyboard is defined as key 27 on board 3.)\n"""))
    
    steps_up_right = int(input("""What is the interval (in MIDI steps) between any given key and its upper-right neighbor?
(Note: The upper right neighbor is located at approximately 1'oclock when looking at the Lumatone
from a bird's eye view)\n"""))
    
    steps_right = int(input("""What is the interval (in MIDI steps) between any given key and its right neighbor?
(Note: The right neighbor is located at approximately 3'oclock when looking at the Lumatone
from a bird's eye view)\n"""))
    
    scale_steps = int(input("How many pitch classes will this mapping be used for?\n"))
    
    color_start_key = int(input("Which pitch class (enter a MIDI value) would you like to start your coloring with?\n"))
    
    # Assign colors
    color_map = {}
    for pitch in range(color_start_key, color_start_key + scale_steps):
        pitch_class_color = input(f"Enter color (name) for MIDI values {pitch} +- multiples of {scale_steps}: ")
        
        # TODO: add vaidation to check that pitch_class_color in cnames.keys()
        color_map[pitch % scale_steps] = pitch_class_color
    print(color_map)

    # Check if default path exists
    default_ltn_dir = os.path.expanduser("~/Documents/Lumatone Editor/Mappings/")
    ltn_dir = default_ltn_dir

    while (not os.path.exists(ltn_dir)):
        manual_input_dir = input(f"""No folder under the name {ltn_dir} found. Please enter the path
of your 'Mappings' folder under Lumatone Editor, or a different folder
in which to output your .ltn file.  """)
        
        ltn_dir = os.path.expanduser(manual_input_dir)

    # Finally, give your mapping a name
    filename = ""
    path_exists = True
    while path_exists:
        filename = input("What would you like to call your mapping?\n")
        if os.path.exists(os.path.join(ltn_dir, filename + ".ltn")):
            filename = input("A mapping under this name already exists. Please enter a new name: ")
        else:
            path_exists = False


    
    # Create un-colored layout
    LTN_layout = create_isomorphic_LTN_layout(steps_up_right, steps_right, scale_steps, center_midi_value)

    # Apply color mapping to layout
    assign_coloring_to_LTN(LTN_layout, color_map, scale_steps)

    # Create ltn file text
    ltn_file_text = create_ltn_file_text(LTN_layout)

    # Write out
    ltn_path = os.path.join(ltn_dir, filename + ".ltn")
    with open(ltn_path, "w") as ltn_file:
        print(f"Writing out mapping to {ltn_path}")
        ltn_file.write(ltn_file_text)

if __name__ == "__main__":
    main()
    