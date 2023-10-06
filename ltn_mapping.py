import numpy as np
# Defaults and constants
CENTER_VALUE = 69
CENTER_BOARD = 2
CENTER_POSITION = 27
SCALE_STEPS = 12
# LTN sections have rows with counts described by the following
LTN_BOARD_ROW_SIZES = [2, 5, 6, 6, 6, 6, 6, 6, 6, 5, 2]
MIDI_MIN = 0
MIDI_MAX = 127
CENTER_CHANNEL = 5
STEPS_UP_RIGHT = 2
STEPS_RIGHT = 1

# List of valid coordinates on LTNBOARD
LTN_BOARD_VALID_COORDINATES = []
for row in range(len(LTN_BOARD_ROW_SIZES)):
    # Compute valid columns row by row
    valid_cols = []
    # The special (offset) cases are rows 9 and 10
    if row == 9:
        valid_cols += [2 * i + 3 for i in range(LTN_BOARD_ROW_SIZES[row])]
    elif row == 10:
        valid_cols += [2 * i + 8 for i in range(LTN_BOARD_ROW_SIZES[row])]
    else:
        # Row with 6 keys; if even start at 0 and count by 2, if odd start by 1 and count 2
        if row % 2 == 0:
            valid_cols += [2 * i for i in range(LTN_BOARD_ROW_SIZES[row])]
        else:
            valid_cols += [2 * i + 1 for i in range(LTN_BOARD_ROW_SIZES[row])]
    
    # Append coordinates
    LTN_BOARD_VALID_COORDINATES += [(row, col) for col in valid_cols]


def coords_to_position_number(row, column):
    # If the coords aren't valid, we'll return -1
    if not (row, column) in LTN_BOARD_VALID_COORDINATES:
        return -1
    
    # Otherwise, we start by reverse engineering the remainder
    remainder = column
    # Reverse adjustments for offset rows
    if row == 9:
        remainder -= 2
    if row == 10:
        remainder -= 8
    
    if row % 2 == 1:
        remainder -= 1
    
    remainder /= 2

    # Now check if remainder is valid before continuing (if not return -1)
    if (row < 0 or row > 10):
        return -1
    elif remainder >= LTN_BOARD_ROW_SIZES[row]:
        return -1
    
    row_position = np.insert(np.cumsum(LTN_BOARD_ROW_SIZES), 0, [0])[row]
    return int(row_position + remainder)

class LTNKey:
    def __init__(self, board, position, MIDI_KEY, color = "000000", channel: int = CENTER_CHANNEL):
        self.board = board
        self.position = position
        assert self.position >= 0
        self.position_row = int(np.argmax(self.position < np.cumsum(LTN_BOARD_ROW_SIZES)))
        self.MIDI_KEY = MIDI_KEY
        self.color = color
        self.channel = channel
    
        def position_remainder_and_column(self):
            # Even numbered rows will have even numbered columns; odd-numbered rows will have odd-numbered columns
            remainder = int(self.position - np.cumsum(np.insert(LTN_BOARD_ROW_SIZES, 0, [0]))[self.position_row])

            column = 2 * remainder
            
            # Adjustment for odd columns
            if self.position_row % 2 == 1:
                column += 1

            #  Make adjustments in special cases where position row is 9 or 10
            if self.position_row == 9:
                column += 2
            if self.position_row == 10:
                column += 8
            
            return int(remainder), int(column)
        
        self.position_remainder, self.position_column = position_remainder_and_column(self)

    def __repr__(self):
        return f"LTNKey({self.board}, {self.position}, {self.MIDI_KEY})"

    def neighbors(self):
        """
        Return list of length 6 denoting a key's neighbors (each neighbor is a key) starting from the upper right neighbor and going clockwise.
        If a neighbor doesn't exist then that slot will be None
        """
        neighbors = []

        # First neighbor (upper-right)
        neighbors.append((self.board, coords_to_position_number(self.position_row - 1, self.position_column + 1)))

        # Second neighbor (right)
        neighbors.append((self.board, coords_to_position_number(self.position_row, self.position_column + 2)))

        # Third neighbor (lower right)
        neighbors.append((self.board, coords_to_position_number(self.position_row + 1, self.position_column + 1)))

        # Fourth neighbor (lower left)
        neighbors.append((self.board, coords_to_position_number(self.position_row + 1, self.position_column - 1)))

        # Fifth neighbor (left)
        neighbors.append((self.board, coords_to_position_number(self.position_row, self.position_column - 2)))

        # Sixth neighbor (upper-left)
        neighbors.append((self.board, coords_to_position_number(self.position_row - 1, self.position_column - 1)))

        # Handle edge cases: neighbors from left board
        
        # If column is 0 then we have 3 neighbors to the left on board - 1 (except when row = 0 then we have no upper left neighbor and row = 8 will have no lower left)
        # The direct left neighbor's row will always 2 more than the row of self, and the remainder will be maxed out
        if self.position_column == 0:
            # Row 8 col 0 will have no lower left neighbor
            if self.position_row == 8:
                neighbors[3] = (self.board - 1, -1)
            else:
                neighbors[3] = (self.board - 1, np.cumsum(LTN_BOARD_ROW_SIZES)[self.position_row + 3] - 1)

            neighbors[4] = (self.board - 1, np.cumsum(LTN_BOARD_ROW_SIZES)[self.position_row + 2] - 1)

            if self.position_row == 0:
                neighbors[5] = (self.board - 1, -1)
            else:
                neighbors[5] = (self.board - 1, np.cumsum(LTN_BOARD_ROW_SIZES)[self.position_row + 1] - 1)


        # If column is 1 then we have 1 neighbor to the left on another board ... always (keep in mind row 9 has no key at column 1)
        if self.position_column == 1:
            neighbors[4] = (self.board - 1, np.cumsum(LTN_BOARD_ROW_SIZES)[self.position_row + 2] - 1)

        
        # Neighbors from the right board - something is buggy here

        if self.position_remainder == LTN_BOARD_ROW_SIZES[self.position_row] - 1:
            # Even rows will have 1 neighbor, odd rows 3
            if self.position_row % 2 == 0 & self.position_row != 0:
                neighbors[1] = (self.board + 1, np.cumsum(np.insert(LTN_BOARD_ROW_SIZES, 0, [0]))[self.position_row - 2])
            
            if self.position_row % 2 == 1:
                if self.position_row != 1:
                    neighbors[0] = (self.board + 1, np.cumsum(np.insert(LTN_BOARD_ROW_SIZES, 0, [0]))[self.position_row - 3])
                    neighbors[1] = (self.board + 1, np.cumsum(np.insert(LTN_BOARD_ROW_SIZES, 0, [0]))[self.position_row - 2])
                    neighbors[2] = (self.board + 1, np.cumsum(np.insert(LTN_BOARD_ROW_SIZES, 0, [0]))[self.position_row - 1])

        return neighbors

# Make necessary octave adjustments to keys that go under 0 or above 127 (want to switch channels as well)
def collapse_to_MIDI_range(key: LTNKey, scale_steps: int):
    """
    Collapses a key's midi value to the range [0, 127], keeping the pitch class the same, by subtracting from the value.
    With each subtraction of scale_steps, we add 1 to the MIDI channel so that we can set each channel to be one equave up
    from the previous to get the full range. When we add to the midi value, we subtract 1 from the channel.

    E.g. if scale_steps = 12
    """
    if key.MIDI_KEY > MIDI_MAX:
        while key.MIDI_KEY > MIDI_MAX:
            key.MIDI_KEY -= scale_steps
            key.channel += 1
    elif key.MIDI_KEY < MIDI_MIN:
        while key.MIDI_KEY < MIDI_MIN:
            key.MIDI_KEY += scale_steps
            key.channel += 1

def create_isomorphic_LTN_layout(
    STEPS_UP_RIGHT: int = STEPS_UP_RIGHT,
    STEPS_RIGHT: int = STEPS_RIGHT,
    SCALE_STEPS: int = SCALE_STEPS,
    CENTER_VALUE: int = CENTER_VALUE,
    CENTER_CHANNEL: int = CENTER_CHANNEL,
    

    # Probably won't need to change
    CENTER_BOARD: int = CENTER_BOARD,
    CENTER_POSITION: int = CENTER_POSITION
):
    # Going in the same order as LTNKey.neighbors()
    NEIGHBOR_STEP_ADJUSTMENTS = np.array([
    STEPS_UP_RIGHT,
    STEPS_RIGHT,
    STEPS_RIGHT - STEPS_UP_RIGHT,
    0 - STEPS_UP_RIGHT,
    0 - STEPS_RIGHT,
    STEPS_UP_RIGHT - STEPS_RIGHT
    ])
    
    # Initialize the LTN layout as 5 boards with 56 keys
    LTN = [[None for i in range(56)] for j in range(5)]

    CENTER_KEY = LTNKey(CENTER_BOARD, CENTER_POSITION, CENTER_VALUE, CENTER_CHANNEL)

    LTN[2][27] = CENTER_KEY
    # BOUNDARY gives us the list of keys that have been populated but whose boundary has not yet been checked or necessarily populated
    BOUNDARY = [CENTER_KEY]

    # Temporary boundary while handling a key's neighbors
    BOUND2 = []

    """
    FILO queue for populating the LTN keyboard. We start with our center key, whose value is given. As we add it to the keyboard,
    we add its neighbor keys to BOUNDARY. We then pop the first key in BOUNDARY, and check if it has already been populated.
    If not, we add populate it and add its neighbors to BOUNDARY. We continue in this way until BOUNDARY is empty.
    """
    while(len(BOUNDARY) > 0):
        # Key whose boundary we're going to populate
        current_key = BOUNDARY.pop(0)
        current_neighbors = current_key.neighbors()
        # Find values for all midi keys
        current_neighbors_midi_keys = current_key.MIDI_KEY + NEIGHBOR_STEP_ADJUSTMENTS

        for i in range(len(current_neighbors)):
            n = current_neighbors[i] #(board, position)

            # If invalid position, then skip this neighbor - This should, however, never happen since we've added the check
            # for valid coordinates in coords_to_position_number
            if(n[0] < 0 or n[0] > 4 or n[1] < 0 or n[1] > 55):
                continue
        
            # Elif LTN[board, position] is not yet popualted:
            elif LTN[n[0]][n[1]] == None:
                # Then both update LTN and add the neighbor to the boundary (we'll keep in a temp list for now)
                Key = LTNKey(n[0], n[1], current_neighbors_midi_keys[i])
                LTN[n[0]][n[1]] = Key
                BOUND2.append(Key)
        
            # If LTN[board, position] is already populated then it's either currently in BOUNDARY or has already been handled
    
        BOUNDARY += BOUND2
        # reset BOUND2
        BOUND2 = []
    
    # Collapse MIDI values
    for board in LTN:
        for key in board:
            collapse_to_MIDI_range(key, SCALE_STEPS)

    return LTN

# Now we've got the midi values, let's assign color
def assign_coloring_to_LTN(LTN_LAYOUT: np.ndarray,
                           regular_color_mapping: dict,
                           scale_size: int = SCALE_STEPS,
                           ):
    """
    Takes in a dict of {int: hex_str} for int in range(SCALE_STEPS). StartKey will indicate which key gets the assignment
    of regular_color_mapping[0]
    """

    assert set(regular_color_mapping.keys()) == set(range(scale_size))

    # Iterate thru each key in LTN
    for Board in LTN_LAYOUT:
        for key in Board:
            value_mod_scale_size = key.MIDI_KEY % scale_size
            key.color = regular_color_mapping[value_mod_scale_size]

def rgb_to_hex(red, green, blue):
    return '{:02X}{:02X}{:02X}'.format(red, green, blue).lower()

def create_ltn_file_text(LTN: np.ndarray):
    # Create .ltn file

    ltn_file = ""

    for i in range(len(LTN)):
        board = LTN[i]
        ltn_file += f"[Board{i}]\n"
        for k in board:
            if k is not None:
                ltn_file += f"Key_{k.position}={k.MIDI_KEY}\nChan_{k.position}={k.channel}\nCol_{k.position}={k.color}\n"
    
    return ltn_file