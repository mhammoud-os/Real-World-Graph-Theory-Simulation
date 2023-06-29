import pygame
from time import sleep
from random import randint

pygame.init()
SCREEN = pygame.display.set_mode((3000, 3200))
pygame.display.set_caption('Hello World!')
maze = []
#maze_width = int(input("What is the width of this random maze: "))
#maze_height = int(input("What is the height of this random maze: "))
maze_width =  20
maze_height= 20
square_size = 15

wall_row=[]
for width in range(maze_width+2):
  wall_row.append(3)
maze.append(wall_row)
for height in range(maze_height):
    row = [3]
    for width in range(maze_width):
      row.append(0)
    row.append(3)
    maze.append(row)
maze.append(wall_row)
    
def draw_maze(maze_map, offset_x, offset_y, square_size):
    for y in range(len(maze_map)):
        for x in range(len(maze_map[y])):
            if maze_map[y][x] ==0:
                fill_color = (235, 235, 240)
            elif maze_map[y][x] ==1:
                fill_color=(211,211,211)
            elif maze_map[y][x] ==2:
                fill_color=(173, 216, 230)
            else:
                fill_color = (0, 0, 0)
            pygame.draw.rect(SCREEN, fill_color,
                             (x * square_size + offset_x, y * square_size +
                              offset_y, square_size - 1, square_size - 1))


def draw_window():
    SCREEN.fill((255, 255, 255))
    draw_maze(maze, 10, 10, square_size)
    pygame.display.update()

def random_dfs(y, x):
    global maze
    draw_window()
    if maze[y][x] >= 3 or maze[y][x] == 2:
        return
    maze[y][x] = 2
    neighbors = [[y - 1, x], [y, x + 1], [y + 1, x], [y, x - 1]]
    for i in neighbors:
      if maze[i[0]][i[1]] == 2:
        continue
      if maze[i[0]][i[1]] == 1:
        maze[i[0]][i[1]] += 2
      else:maze[i[0]][i[1]] += 1
    
    for i in range(20): 
      blocked_paths = 0
      for i in neighbors:
        value=maze[i[0]][i[1]]
        if value >= 3 or value ==2:
          blocked_paths+=1
      if blocked_paths == 4:
        break
      direction = randint(0, 3)
      if maze[neighbors[direction][0]][neighbors[direction][1]] >=3 or maze[neighbors[direction][0]][neighbors[direction][1]] ==2:
        continue
      random_dfs(neighbors[direction][0], neighbors[direction][1])
    return
random_dfs(1, 1)

for y in range(len(maze)):
  for x in range(len(maze[y])):
    if  maze[y][x] == 1 or maze[y][x] ==2 :
      maze[y][x] = 1
    else:
      maze[y][x] = 0
for i in maze:
  print(i)
while True:
  start_pos = [randint(1,len(maze)-2),1]
  end_pos = [randint(1,len(maze)-2),len(maze[0])-2] 
  if maze[start_pos[0]][start_pos[1]] == 1 and maze[end_pos[0]][end_pos[1]] == 1:
    break
print(start_pos,end_pos)
file = open("random_maze.txt", "w")
file.write(str(start_pos)+'\n'+str(end_pos)+"\n"+str(maze))
file.flush()

