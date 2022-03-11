import pygame
import math
from queue import PriorityQueue
from queue import Queue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # set up the display, the actual display, how big the display etc
pygame.display.set_caption("Path Finding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#use the hamilton  

#this keep track of cubes/nodes, where it is (aka position) need to know color, neighbors, 
class Node: #visualization tool, or the little cubes
    #width = how wide is the node or cube
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width #actual coor are x not row
        self.y = col * width
        #why do this? need to keep track of coordinate position, ex 50 cubes, so 800/50 = 16 thats the width of each cube
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self): return self.row, self.col

    #the boolean question if they are what they are
    def is_visited(self): return self.color == RED
    def is_in_queue(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start_here(self): return self.color == ORANGE
    def is_end_here(self): return self.color == TURQUOISE
    
    def reset(self): self.color = WHITE
    
    #updating the color to match if they were ...
    def update_visited(self): self.color = RED 
    def update_in_queue(self): self.color = GREEN
    def update_barrier(self): self.color = BLACK
    def update_start_here(self): self.color = ORANGE
    def update_end_here(self): self.color = TURQUOISE

    #our actual path
    def update_path(self): self.color = PURPLE

    #draw node on screen, win-nya yg pygame display set thing, win is where u wanna draw this
    def draw(self, win):
        #how u wanna draw rectangle, position etc, 0,0 is top left
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #check up down left right, if barrier, cant add to the node neighbor
    def update_neighbors(self, grid):
        self.neighbors = []
        #check if curr row is less that total row cuz or gk keluar the bounds, we gon add row down, aka 1 down a row
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])


    def __lt__(self, other): #lt is less than when we compare 2 spots
        return False

#manhattan distance, the L distance or the x + y distance, p is also a coordinate
def h(p1, p2): #dist b/w point 1 and point2
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.update_path()
        draw()

def astar_algorithm(draw, grid, start, end):
    #draw() is called
    count = 0 #keep track of when we insert item to queue to break ties if f score same
    pq = PriorityQueue()
    #add start node with original f score 1st param,3rd param is node itself
    pq.put((0, count, start))
    came_from = {}
    #same as for row in grid: for node in row
    #key for every spot of gscore
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    pq_hash = {start} #can check if sth is in priority queue

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = pq.get()[2]   #open set stores f,count and node and we just want the node
        pq_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.update_end_here()
            return True

        #considering the neighbor
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #cuz its +1 neighbor
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                #check if neighbor is in the PQ
                if neighbor not in pq_hash:
                    count += 1
                    pq.put((f_score[neighbor], count, neighbor))
                    pq_hash.add(neighbor)
                    neighbor.update_in_queue()
        draw()

        #if curr node looked at is not start then we considered it
        if current != start:
            current.update_visited()

    return False

#what data structure to hold all the nodes to make the grid, to traverse the nodes --> a list, not a 2d array
#grid generation
def make_grid(rows, width):
    grid = []
    gap = width // rows #gives the width of each cube
    for i in range(rows):
        grid.append([]) #creating 2D rows
        for j in range(rows):
            node = Node(i,j,gap,rows) #create a (aka 1) square
            grid[i].append(node)
    return grid

#draw the horizontal line
#literal grid lines, if u dont understnad, switch color maybe u wud get it
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
                                    #start line, end line
        pygame.draw.line(win, GREY, (0, i*gap),(width, i*gap))
        for j in range(rows):
             pygame.draw.line(win, GREY, (j*gap,0),( j*gap, width))

#main draw func, drawing everything
def draw(win, grid, rows, width):
    win.fill(WHITE) #fill everything with 1 color 
    for row in grid:
        for node in row:
            node.draw(win) #line 57, it draws the cube its own color at that coordinate

    draw_grid(win, rows, width)
    pygame.display.update()

#take mouse position to figure out where we are at coordinates wise (what node we are clicking at)
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    #take coor and divide by width of each node
    row = y // gap
    col = x // gap
    return row, col

#collision checks, using the methods
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True
    #loop thru all events that happen, ex, someone pressed the amount, check gitu
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #if user press down on left mouse 
            if pygame.mouse.get_pressed()[0]:
                #gets coordinate
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) #the actual spot in our 2D list
                node = grid[row][col]
                #why elif? remember this is 1 key pressed
                if not start and node != end:
                    start = node
                    start.update_start_here()

                elif not end and node != start:
                    end = node
                    end.update_end_here()

                elif node != start and node != end:
                    node.update_barrier()

            #right mouse, if middle is 1
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None
            
            #if press space, and not yet run algo then always check the neighbors
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    #run algorithm
                    #update neighbors of node class
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    #basically calling the draw func as an argument
                    astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c: #clear screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)



