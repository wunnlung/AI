import random
import pygame
import numpy as np
import re

DEBUG = 0

# Parameters
population_size = 100
chromosome_length = 700
crossover_rate = 0.7
mutation_rate = 0.001
generations = 100
###### if we are loading in from the file, make this true
###### if starting from init_population, set it to false
fFile = True


# Initialize population
def init_population(pop_size, chromosome_length):
    return np.random.randint(3, size=(pop_size, chromosome_length))

# Fitness function
def fitness(chromosome):
    print("Checking fitness of ",chromosome)
    return play(pygame.display.set_mode((s_width,s_height)),chromosome)

#used to clear the training file (only used when starting from scratch)
def clearTraining():
    with open("training.txt", "w") as f:
        f.truncate(0)

#from file function
def fromFile():
    with open("fitness.txt", 'r') as f:
        file_content = f.read()
    matches = re.findall(r'\[([-\d\s]+)\]', file_content)
    all_chromosomes = [np.fromstring(match, dtype=int, sep=' ') for match in matches]
    return np.array(all_chromosomes)

#to file function
def toFile(s):
    f=open("fitness.txt", "w")
    for fit in s:
        f.write(str(fit))
    #this will get it to replace the current population with the next one
    f.close()

#file of all the fitnesses over time
def fitnessFile(s):
    try:
        #read last gen from file
        with open("training.txt", "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_generation = int(last_line.split(":")[1].split(",")[0].strip())
            else:
                last_generation = 0
    except FileNotFoundError:
        #if file doesn't exist start at gen 0
        last_generation = 0
    #add 1 to generation count
    current_generation = last_generation + 1
    best_fitness = max(s)
    #add the current generation count and best performance of the generation to the file
    with open("training.txt", "a") as f:
        f.write(f"Generation: {current_generation}, Best Fitness: {best_fitness}\n")


# Selection
def select(population):
    #updating the current population in the file
    toFile(population)
    fitnesses = np.array([fitness(individual) for individual in population])
    #adding the current populations fitness to 
    fitnessFile(fitnesses)
    print(fitnesses)
    #if every fitness in the list was 0
    if all([v==0 for v in fitnesses]):
        parents_indices = np.random.choice(np.arange(population_size), size=population_size, replace=True, p=np.full(population_size, 1/population_size))
    else:
        parents_indices = np.random.choice(np.arange(population_size), size=population_size, replace=True, p=fitnesses/fitnesses.sum())
    return population[parents_indices]

# Crossover
def crossover(parent1, parent2):
    if np.random.rand() < crossover_rate:
        point = np.random.randint(1, chromosome_length-1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    else:
        return parent1, parent2

# Mutation
def mutate(chromosome):
    for i in range(len(chromosome)):
        if np.random.rand() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Genetic Algorithm
def genetic_algorithm():
    print("in the ga")
    if fFile == False:
        clearTraining()
        population = init_population(population_size, chromosome_length)
    else :#fFile is true
        population = fromFile()
    for generation in range(generations):
        new_population = []
        selected = select(population)
        toFile(selected)
        for i in range(0, population_size, 2):
            parent1, parent2 = selected[i], selected[i+1]
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        population = np.array(new_population)



"""
10 x 20 grid
play_height = 2 * play_width

tetriminos:
    0 - S - green
    1 - Z - red
    2 - I - cyan
    3 - O - yellow
    4 - J - blue
    5 - L - orange
    6 - T - purple
"""

pygame.font.init()

# global variables

col = 10  # 10 columns
row = 20  # 20 rows
s_width = 800  # window width
s_height = 750  # window height
play_width = 300  # play window width; 300/10 = 30 width per block
play_height = 600  # play window height; 600/20 = 20 height per block
block_size = 30  # size of block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = './highscore.txt'
fontpath = './arcade.ttf'
fontpath_mario = './mario.ttf'

# shapes formats

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# index represents the shape
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# class to represent each of the pieces


class Piece(object):
    def __init__(self, x, y, shape, letter):
        self.x = x
        self.y = y
        self.shape = shape
        self.letter = letter
        self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
        self.rotation = 0  # chooses the rotation according to index


# initialise the grid
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # grid represented rgb tuples

    # locked_positions dictionary
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                grid[y][x] = color  # set grid position to color

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]  # get the desired rotated shape from piece

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    for i, line in enumerate(shape_format):  # i gives index; line gives string
        row = list(line)  # makes a list of char from string
        for j, column in enumerate(row):  # j gives index of char; column gives char
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # offset according to the input given with dot and zero

    return positions


# checks if current position of piece in grid is valid
def valid_space(piece, grid):
    # makes a 2D list of all the possible (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    # removes sub lists and puts (x,y) in one list; easier to search
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# check if piece is out of board
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# chooses a shape randomly from shapes list
def get_shape():
    choice = random.randint(0,6)
    return Piece(5, 0, shapes[choice], choice)


# draws text in the middle
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


# draws the lines of the grid for the game
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


# clear a row when it is filled
def clear_rows(grid, locked):
    # need to check if row is clear then shift every other row above down one
    increment = 0
    for i in range(len(grid) - 1, -1, -1):      # start checking the grid backwards
        grid_row = grid[i]                      # get the last row
        if (0, 0, 0) not in grid_row:           # if there are no empty spaces (i.e. black blocks)
            increment += 1
            # add positions to remove from locked
            index = i                           # row index will be constant
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]          # delete every locked element in the bottom row
                except ValueError:
                    continue

    # shift every row one step down
    # delete filled bottom row
    # add another empty row on the top
    # move down one step
    if increment > 0:
        # sort the locked list according to y value in (x,y) and then reverse
        # reversed because otherwise the ones on the top will overwrite the lower ones
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:                       # if the y value is above the removed index
                new_key = (x, y + increment)    # shift position to down
                locked[new_key] = locked.pop(key)

    return increment


# draws the upcoming piece
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))

    # pygame.display.update()


# draws the content of the window
def draw_window(surface, grid, score=1, last_score=1):
    surface.fill((0, 0, 0))  # fill the surface with black

    pygame.font.init()  # initialise font
    font = pygame.font.Font(fontpath_mario, 65)
    label = font.render('TETRIS', 1, (255, 255, 255))  # initialise 'Tetris' text with white

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))  # put surface on the center of the window

    # current score
    font = pygame.font.Font(fontpath, 30)
    label = font.render('SCORE   ' + str(score) , 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x, start_y + 200))

    # last score
    label_hi = font.render('HIGHSCORE   ' + str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    # draw content of the grid
    for i in range(row):
        for j in range(col):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # draw vertical and horizontal grid lines
    draw_grid(surface)

    # draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)

    # pygame.display.update()


# update the score txt file with high score
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# get the high score from the file
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # reads all the lines and puts in a list
        score = int(lines[0].strip())   # remove \n

    return score

############################################################################
def find_max_height(grid):
    temp = []
    for i in grid:
        temp.append(sum(i))
    temp.reverse()
    hl = np.nonzero(temp)[0]
    if len(hl) > 0:
        return hl[-1]+1
    else:
        return 0

def count_holes(grid):
    num_holes = 0
    hole_locations = []

    for x in range(len(grid[0])):
        hole_found = False  # Flag to track if a hole is found in this column
        for y in range(len(grid)):
            if grid[y][x] == 0:
                # Check if the empty space is not accessible from the top
                accessible_from_top = False
                for i in range(y):
                    if grid[i][x] == 1:
                        accessible_from_top = True
                        break
                
                if not accessible_from_top:
                    # Check if the empty space is surrounded on all other sides
                    if (y == len(grid) - 1 or grid[y + 1][x] == 1) and \
                       (x == 0 or grid[y][x - 1] == 1) and \
                       (x == len(grid[0]) - 1 or grid[y][x + 1] == 1):
                        num_holes += 1
                        hole_locations.append((x, y))
                        hole_found = True

        # If a hole is found in this column, reset the flag to False
        if hole_found:
            hole_found = False

    return num_holes, hole_locations



#########################################################################################

def play(window, chromosome):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    piece_control = True
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    #game speed is directly coorelated to fall_speed
    #lower is faster
    fall_speed = 0.0001
    level_time = 0
    score = 1
    last_score = get_max_score()
    sub_chrom = []
    if DEBUG:  print(chromosome)

    def execute(sub_chrom):
        gene = sub_chrom[0]
        if DEBUG:  print("Gene = ",gene)
        if gene == 0:
            if DEBUG:  print("Moving Left")
            current_piece.x -= 1  # move x position left
            if not valid_space(current_piece, grid):
                current_piece.x += 1 
        elif gene == 1:
            if DEBUG:  print("Moving Right")
            current_piece.x += 1  # move x position right
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
        else:
            if DEBUG:  print("Turning")
            current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
            if not valid_space(current_piece, grid):
                current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)


    while run:
        # need to constantly make new grid as locked positions always change
        grid = create_grid(locked_positions)

####################################################################
        #not that efficient, the game still runs at the same speed tho   
        
        # Create an empty list to hold the converted grid
        binary_grid = []
        for i in grid:
            row_binary = []
            for j in i:
                if j == (0, 0, 0):
                    row_binary.append(0)
                else:
                    row_binary.append(1)
            binary_grid.append(row_binary)
        #print(binary_grid)
        #if DEBUG: print("Number of Holes: " + str(count_holes(binary_grid)))
        #if DEBUG: print("Max Height: "+ str(find_max_height(binary_grid)))

        

####################################################################
        #print(grid)
        #able to print grid, returns massive list with 0's as empty, and 255 as filled spots. Able to constantly get
        #actually I lied, I think the 255 has to do with the color. It prints out a list of each square, and what color it contains.

        # helps run the same on every computer
        # add time since last tick() to fall_time
        fall_time += clock.get_rawtime()  # returns in milliseconds
        level_time += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time/1000 > 5:    # make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15:   # until fall speed is 0.15
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move x position left
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move x position right
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)


        ####### AI FUNCTIONS #######
        def find_center_of_gap(binary_list):
            max_length = 0
            current_length = 0
            start_index = -1
            for i, value in enumerate(binary_list):
                if value == 0:
                    if current_length == 0:
                        start_index = i  # Start of a new sequence
                    current_length += 1
                else:
                    if current_length > max_length:
                        max_length = current_length
                        max_start = start_index
                    current_length = 0

            # Check if the last sequence is the longest one
            if current_length > max_length:
                max_length = current_length
                max_start = start_index

            # Calculate the center
            if max_length == 0:
                return None  # No zeros in the list
            center = max_start + (max_length - 1) // 2
            return center



        ######AI INJECTION######

        #Parse the grid into a 2D binary list                
        parsed_grid = []
        for row in grid:
            parsed_row = []
            for square in row:
                if square == (0, 0, 0):
                    parsed_row.append(0)
                else:
                    parsed_row.append(1)
            parsed_grid.append(parsed_row)
       
        center = find_center_of_gap(parsed_grid[-1])

        if DEBUG: print("Executing chromosome...")
        if DEBUG: print(current_piece.letter)
        #GA AI behavior
        if len(sub_chrom) == 0 and piece_control == True:
            match current_piece.letter:
                case 0:
                    match center:
                        case 0:
                            sub_chrom = chromosome[:10]
                        case 1:
                            sub_chrom = chromosome[10:20]
                        case 2:
                            sub_chrom = chromosome[20:30]
                        case 3:
                            sub_chrom = chromosome[30:40]
                        case 4:
                            sub_chrom = chromosome[40:50]
                        case 5:
                            sub_chrom = chromosome[50:60]
                        case 6:
                            sub_chrom = chromosome[60:70]
                        case 7:
                            sub_chrom = chromosome[70:80]
                        case 8:
                            sub_chrom = chromosome[80:90]
                        case 9:
                            sub_chrom = chromosome[90:100]
                        
                case 1:
                    match center:
                        case 0:
                            sub_chrom = chromosome[100:110]
                        case 1:
                            sub_chrom = chromosome[110:120]
                        case 2:
                            sub_chrom = chromosome[120:130]
                        case 3:
                            sub_chrom = chromosome[130:140]
                        case 4:
                            sub_chrom = chromosome[140:150]
                        case 5:
                            sub_chrom = chromosome[150:160]
                        case 6:
                            sub_chrom = chromosome[160:170]
                        case 7:
                            sub_chrom = chromosome[170:180]
                        case 8:
                            sub_chrom = chromosome[180:190]
                        case 9:
                            sub_chrom = chromosome[190:200]
                
                case 2:
                    match center:
                        case 0:
                            sub_chrom = chromosome[200:210]
                        case 1:
                            sub_chrom = chromosome[210:220]
                        case 2:
                            sub_chrom = chromosome[220:230]
                        case 3:
                            sub_chrom = chromosome[230:240]
                        case 4:
                            sub_chrom = chromosome[240:250]
                        case 5:
                            sub_chrom = chromosome[250:260]
                        case 6:
                            sub_chrom = chromosome[260:270]
                        case 7:
                            sub_chrom = chromosome[270:280]
                        case 8:
                            sub_chrom = chromosome[280:290]
                        case 9:
                            sub_chrom = chromosome[290:300] 
                        
                case 3:
                    match center:
                        case 0:
                            sub_chrom = chromosome[300:310]
                        case 1:
                            sub_chrom = chromosome[310:320]
                        case 2:
                            sub_chrom = chromosome[320:330]
                        case 3:
                            sub_chrom = chromosome[330:340]
                        case 4:
                            sub_chrom = chromosome[340:350]
                        case 5:
                            sub_chrom = chromosome[350:360]
                        case 6:
                            sub_chrom = chromosome[360:370]
                        case 7:
                            sub_chrom = chromosome[370:380]
                        case 8:
                            sub_chrom = chromosome[380:390]
                        case 9:
                            sub_chrom = chromosome[390:400]
                
                case 4:
                    match center:
                        case 0:
                            sub_chrom = chromosome[400:410]
                        case 1:
                            sub_chrom = chromosome[410:420]
                        case 2:
                            sub_chrom = chromosome[420:430]
                        case 3:
                            sub_chrom = chromosome[430:440]
                        case 4:
                            sub_chrom = chromosome[440:450]
                        case 5:
                            sub_chrom = chromosome[450:460]
                        case 6:
                            sub_chrom = chromosome[460:470]
                        case 7:
                            sub_chrom = chromosome[470:480]
                        case 8:
                            sub_chrom = chromosome[480:490]
                        case 9:
                            sub_chrom = chromosome[490:500]
                
                case 5:
                    match center:
                        case 0:
                            sub_chrom = chromosome[500:510]
                        case 1:
                            sub_chrom = chromosome[510:520]
                        case 2:
                            sub_chrom = chromosome[520:530]
                        case 3:
                            sub_chrom = chromosome[530:540]
                        case 4:
                            sub_chrom = chromosome[540:550]
                        case 5:
                            sub_chrom = chromosome[550:560]
                        case 6:
                            sub_chrom = chromosome[560:570]
                        case 7:
                            sub_chrom = chromosome[570:580]
                        case 8:
                            sub_chrom = chromosome[580:590]
                        case 9:
                            sub_chrom = chromosome[590:600]
                
                case 6:
                    match center:
                        case 0:
                            sub_chrom = chromosome[600:610]
                        case 1:
                            sub_chrom = chromosome[610:620]
                        case 2:
                            sub_chrom = chromosome[620:630]
                        case 3:
                            sub_chrom = chromosome[630:640]
                        case 4:
                            sub_chrom = chromosome[640:650]
                        case 5:
                            sub_chrom = chromosome[650:660]
                        case 6:
                            sub_chrom = chromosome[660:670]
                        case 7:
                            sub_chrom = chromosome[670:680]
                        case 8:
                            sub_chrom = chromosome[680:690]
                        case 9:
                            sub_chrom = chromosome[690:700]

        if len(sub_chrom) > 0:
            if DEBUG:  print("Executing ",sub_chrom)
            execute(sub_chrom)
            if DEBUG:  print(piece_control)
            sub_chrom = sub_chrom[1:]
        if len(sub_chrom) == 0: piece_control = False


        #Simple AI behavior
        #Move the piece to the center of the gap closest to the top
        ''' for row in parsed_grid:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
            if(sum(row) > 0):
                #print("Current Piece Position: " + str(current_piece.x))
                if find_center_of_gap(row) > current_piece.x:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif find_center_of_gap(row) < current_piece.x:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                #print("Center of gap: " + str(find_center_of_gap(row)))
                break
        '''      
                
        #Random AI behavior
        """ rand_val = random.randint(0, 4)
        if rand_val == 0:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
        elif rand_val == 1:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
        elif rand_val == 2:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
        elif rand_val == 3:
            current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
            if not valid_space(current_piece, grid):
                current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape) """

        ########################

        piece_pos = convert_shape_format(current_piece)
####################################################################
        #print here
        #print("Current piece: " + str(current_piece) + "Pos: " + str(piece_pos))

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:  # if the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color       # add the key and value in the dictionary
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10    # increment score by 10 for every row cleared
            update_score(score)
            piece_control = True

            if last_score < score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle('You Lost', 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.quit()

    return score

genetic_algorithm()
