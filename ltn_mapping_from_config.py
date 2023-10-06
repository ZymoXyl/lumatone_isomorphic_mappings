import os
import click
import yaml
from ltn_mapping import *

def create_ltn_file(input_args: dict):
    # Create un-colored layout
    LTN_layout = create_isomorphic_LTN_layout(STEPS_UP_RIGHT=input_args['step_y'],
                                              STEPS_RIGHT=input_args['step_x'],
                                              SCALE_STEPS=len(input_args['colors'].keys()),
                                              CENTER_VALUE=input_args['center'])

    # Apply color mapping to layout
    assign_coloring_to_LTN(LTN_layout,
                           input_args['colors'],
                           len(input_args['colors'].keys()))

    # Create ltn file text
    ltn_file_text = create_ltn_file_text(LTN_layout)

    return ltn_file_text

def write_ltn_file(ltn_file_text, ltn_dir, filename):
    ltn_path = os.path.join(ltn_dir, filename + ".ltn")
    if os.path.exists(ltn_path):
        print("A .ltn file with this name already exists. Please choose a new name.")
        return
    else:
        with open(ltn_path, "w") as ltn_file:
            print(f"Writing out mapping to {ltn_path}")
            ltn_file.write(ltn_file_text)


@click.command()
@click.option('--config', default='piano_layout.yaml', help='Name of config file under configs/ directory')
@click.option('--output', default='piano_test', help="Output name of .ltn file (without suffix)")

def main(config, output):
    config_path = os.path.join(os.getcwd(), "configs", config)
    with open(config_path, "r") as txt:
        args = yaml.safe_load(txt)
    ltn_file_text = create_ltn_file(input_args=args)
    # Now look for Lumatone Editor files
    # First check if default path exists
    default_ltn_dir = os.path.expanduser("~/Documents/Lumatone Editor/Mappings/")
    ltn_dir = default_ltn_dir

    while (not os.path.exists(ltn_dir)):
        manual_input_dir = input(f"""No folder under the name {ltn_dir} found. Please enter the path
of your 'Mappings' folder under Lumatone Editor, or a different folder
in which to output your .ltn file.""")
        # Try the new directory
        ltn_dir = os.path.expanduser(manual_input_dir)

    write_ltn_file(ltn_file_text=ltn_file_text, ltn_dir=ltn_dir, filename=output)
    

if __name__ == '__main__':
    main()