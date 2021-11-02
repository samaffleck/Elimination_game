import pygame
import random

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

W = 600
win = pygame.display.set_mode((W, W))
pygame.display.set_caption("Elimination game")
pygame.init()


class Node:

	# Node object represents each square on the game and can have a state of 1 or 0.

    def __init__(self, row, col, width, total_rows):
        self.row = row # Row number 
        self.col = col # Column number
        self.x = row * width # x coordinate of the node
        self.y = col * width # y coordinate of the node
        self.neighbours = [] # List of all orthoganlly adjacent neighbours
        self.width = width # Size of the square's side
        self.total_rows = total_rows # Total number of rows in the game

        # Each node is initialised with a 50% chance of being in state 1
        rand = random.random()
        if rand >= 0.5:
            self.state = 1
            self.colour = WHITE
        else:
            self.state = 0
            self.colour = BLACK

    def draw(self, win):
    	# This updates the nodes colour and draws it on the screen
        if self.state == 1:
            self.colour = WHITE
        else:
            self.colour = BLACK
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
    	# update neighbours stores all of the neighbours of a node
        self.neighbours = []
        if self.row < self.total_rows - 1:  # Down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0:  # Up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1:  # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0:  # Left
            self.neighbours.append(grid[self.row][self.col - 1])


def make_grid(rows, width):
	# All nodes will be stored in a square matrix of size rows x rows 
    grid = []
    gap = width // rows 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
	# draw grid draws on grey lines to seperate the squares
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


def draw(win, grid, rows, width):
	# Updates the window
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
	# Returns the row number and column number of the mouse when clicked
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def no_animation(ROWS, width):

	# This function is a brute force algorithm that randomly selects nodes until the game ends

    batches = 10 # Number of games
    for game in range(batches):
        grid = make_grid(ROWS, width)  # Make a new grid
        running = True
        number_of_hits = 0 # Stores the number of turns taken
        for row in grid:
            for node in row:
                node.update_neighbours(grid)

        while running:
            rand_row = random.choice(grid)
            rand_node = random.choice(rand_row)
            if rand_node.state == 1:
                number_of_hits += 1
                rand_node.state = 0
                for adj_node in rand_node.neighbours:
                    if adj_node.state == 0:
                        adj_node.state = 1
                    else:
                        adj_node.state = 0

            count = 0
            # Check if all of the nodes in the grid are off
            for row in grid:
                for node in row:
                    count += node.state
            if count == 0:
                running = False # Finises this game and moves onto the next
                print("Game number: ", game, " took ", number_of_hits, " hits!")


def animation(grid, ROWS, width, win):
    number_of_hits = 0
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                for row in grid:
                    for node in row:
                        node.update_neighbours(grid)
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                if node.state == 1:
                    number_of_hits += 1
                    node.state = 0
                    for adj_node in node.neighbours:
                        if adj_node.state == 0:
                            adj_node.state = 1
                        else:
                            adj_node.state = 0

        count = 0
        for row in grid:
            for node in row:
                count += node.state
        if count == 0:
            run = False

    pygame.quit()
    print("Number of hits: ", number_of_hits)


def main(win, W):
	# Initialise the games parameters
    ROWS = 3
    grid = make_grid(ROWS, W)

    animation(grid, ROWS, W, win) # Displays the game

    #no_animation(ROWS, W) # Brute force method


main(win, W)
