from collections import deque
from time import ticks_us, ticks_diff
from driving_functions import *
direction = 1
drive(0, start_speed['left'],0,start_speed['right'], 1)

led_onboard = machine.Pin(25, Pin.OUT)
led_onboard.value(1)
stop(1.5)
led_onboard.value(0)

#open('maze_file.txt', 'w').close()
maze_file = open("maze_file.txt", "a+")
maze_file.write("The Collected Maze:\n\n")
speed_time = float(open('config.txt','r').readline())
open('config.txt','r').close()

def drive_until_intersection():
    global direction,visited
    start = ticks_us()
    drive(0, start_speed['left'],0,start_speed['right'], 0.1)
    while True:
        if sensors['left'].value() or sensors['right'].value():
            break
        elif not sensors['forward'].value():
            break
    stop(1)
    end = ticks_us()
    diff = ticks_diff(end,start)
    blocks = round(diff/speed_time/149)
    new_paths = []
    for i in range(4):
        if check_sensor(i):
            new_paths.append(i)
    for i in range(blocks):
        mouse_pos[1] += neighbors[direction][1]
        mouse_pos[0] += neighbors[direction][0]
        colect_maze(mouse_pos[1],mouse_pos[0])
        if mouse_pos[1]<1:
            mouse_pos[1] = 1
        if mouse_pos[0] <1:
            mouse_pos[0] = 1
        visited.append(mouse_pos)
    
    current_direction = direction
    for i in new_paths:
        direction = i
        colect_maze(mouse_pos[1]+neighbors[direction][1],mouse_pos[0]+neighbors[direction][0])
    direction = current_direction
    print(new_paths)
collected_maze = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
def colect_maze(x, y):
  global collected_maze
  add_row = []
  for count in range(len(collected_maze[0])):
      add_row.append(0)

  if direction == 0 and y == 0:
    collected_maze.insert(0,add_row)
    y = 1
  elif direction == 2 and y == len(collected_maze)-1:
    collected_maze.insert(-1,add_row)
  elif direction == 1 and x == len(collected_maze[0])-1:
    for i in collected_maze:
      i.insert(-1,0)
    collected_maze[y][-2]=1
  elif direction == 3 and x == 0:
    x = 1
    for i in collected_maze:
      i.insert(0,0)
  collected_maze[y][x] = 1
  maze_file = open("maze_file.txt", "a+")
  maze_file.write('\nstack '+str(stack)+'\nmousepos'+str(mouse_pos)+'\ncurrent'+str(current)+'\ndirection'+str(direction)+'\n')
  for i in collected_maze:
      maze_file.write(str(i)+"\n") 
  maze_file.write("\n")
  maze_file.close()


def turn_to(destination):
  global direction
  num_turns = abs(direction - destination)
  if direction > destination:
    for count in range(num_turns):
        turn('left')
        sleep(1)
        pass
    pass
  elif direction < destination:
    for count in range(num_turns):
        turn('right')
        sleep(1)
        pass
    pass
  else:
    pass
  direction = destination

#turn_to(2)

def go_to(start, end):
  y1 = start[0]
  x1 = start[1]
  y2 = end[0]
  x2 = end[1]
  if x2 == x1:
    if y2 == y1:
      return direction
    elif y2 > y1:
      return 2
    else:
      return 0
  else:
    if x2 > x1:
      return 1
    else:
      return 3
def go_through(path):
    global visited,stack,mouse_pos
    for pos in path:
        #sleep(0.5)
        xpos = pos[1]
        ypos = pos[0]
        turn_to(go_to(mouse_pos, [ypos, xpos]))
        mouse_pos = [ypos, xpos]
        if mouse_pos in stack:
          visited.append(mouse_pos)
          stack.remove(mouse_pos)
        move('forward block',1)
        colect_maze(xpos,ypos)
    
def check_sensor(check_dir):
    sensors_list = ['forward','right','','left']
    sensor_num = (check_dir-direction)%4
    if sensor_num == 2:
        return
    return sensors[sensors_list[sensor_num]].value()

def bfs(start, end, maze):
  bfs_visited = []
  bfs_queue = deque((),500)
  bfs_visited.append(start)
  bfs_queue.append(start)
  path = []
  while len(bfs_queue) > 0:
    visiting = bfs_queue.popleft()
    if visiting == end:
      break
    for i in neighbors:
      x = visiting[1] + i[1]
      y = visiting[0] + i[0]
      if [y, x] in bfs_visited:
        continue
      if not maze[y][x]:
        continue
      bfs_visited.append([y, x])
      bfs_queue.append([y, x])
      path.append([[y, x], visiting])
  shortest_path = [end]
  
  find_queue = deque((),3000)
  find_queue.append(end)
  while len(find_queue)!=0:
      find = find_queue.popleft()
      for i in path:
          if i[0] == find:
              shortest_path.insert(0, i[0])
              find_queue.append(i[1])
  return shortest_path

visited = [[0, 0]]
path_so_far = [[1, 1]]
start_pos = [1, 1]
stack = [start_pos]
neighbors = [[-1, 0],[0, 1], [1, 0], [0, -1]]
mouse_pos = start_pos
while len(stack) > 0:
  current = stack.pop()
  y = current[0]
  x = current[1]
  visited.append([y, x])
  go_through(bfs(mouse_pos, current, collected_maze))
  drive_until_intersection()
  print('intersectoin!!')
  sleep(3)
  for i in range(len(neighbors)):
    new_y = mouse_pos[0] + neighbors[i][0]
    new_x = mouse_pos[1] + neighbors[i][1]
    if check_sensor(i) and not [new_y, new_x] in visited and [new_y,new_x] not in stack:
      stack.append([new_y, new_x])
      print([new_y, new_x])
      #original_dir = direction
      #direction = go_to(mouse_pos, [new_y, new_x])
      #colect_maze(new_x, new_y)
      #direction = original_dir
maze_file.close()
print("The collected maze:")
for i in collected_maze:
    print(i)
turn_to(go_to(mouse_pos, start_pos))
mouse_pos = start_pos
sleep(2)
shortest_path = bfs(start_pos, end_pos, collected_maze)
print("The shortest path:")
print(shortest_path)
for pos in shortest_path:
  sleep(0.1)
  xpos = pos[1]
  ypos = pos[0]
  turn_to(go_to(mouse_pos, [ypos, xpos]))
  mouse_pos = [ypos, xpos]