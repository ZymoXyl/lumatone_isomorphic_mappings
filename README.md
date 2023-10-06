# lumatone_isomorphic_mappings
Create .ltn files for isomorphic mappings for Lumatone

# How to use
Create a config (.yaml) file under the configs/ folder in this repository. Follow the syntax of the piano_layout.yaml file. Here's what each line in the file means:

- `center` specifies which MIDI key to assign to the center of the keyboard. The "center" of the keyboard is defined as key 27 on board 2 (0-indexed).
- `step_x` specifies how many MIDI steps to move up in the "x" direction, which is approximately 3'oclock from a bird's eye view. This can be set to a negative value to move down.
- `step_y` specifies how many MIDI steps to move in the "y" direction, which is approximately 1'oclock from a bird's eye view.
- `start_pitch_class` will define which pitch class (given by MIDI value) to start the coloring with. To start coloring at the center of the keyboard, set this the same as `center`
- `colors` defines the color layout, and also the number of scale degrees that are implicit in the layout (which affects wrap-arounds for the MIDI value assignment). Starting at 0, define a color for each pitch class up to (number of scale degrees - 1). Make sure to indent each color line as in piano_layout.yaml

To run this script, go to the terminal, cd to the repository folder, and type `python ltn_mapping_from_config.py --config (your config file) --output (your output file)` where (your config file) is the name (not path) of your config file, with suffix, and (your output file) is the desired name of your output .ltn file, without suffix. By default, the script will save to the Mappings/ folder under Documents/Lumatone Editor . If that isn't found, it will prompt you to enter the output location.
