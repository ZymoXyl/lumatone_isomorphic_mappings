# lumatone_isomorphic_mappings
Create .ltn files for isomorphic mappings for Lumatone

Basically, here's how it'll work:

You tell it which midi value to center on, how big your scale is (how many steps), and how many steps you want to change by as you go 1 o'clock and 3 o'clock from any key.

For each scale step (starting at a value of your choice), you assign to it a color.

The program computes and outputs a .ltn file with the isomorphic layout you've defined.

For instance:

scale_steps = 12, steps_up_right = 1, steps_right = 2, center = 65, color_start = 60 (middle C), color map = {0: white, 1: blue, 2: white, 3: blue, 4: white, 5: white, 6: blue, 7: white, 8: blue, 9: white, 10: blue, 11: white} will give you the default A_001 Bosanquet layout. You can easily recreate any of the other presets like this too.

Whenever I have to collapse the octave, I increment / decrement the MIDI channel, so the idea is that hopefully this makes it easy to work with VSTs to get the full range if you so desire 
