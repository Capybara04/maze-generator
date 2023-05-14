import random
import pygame

# ktao pygame
pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
size = (701, 701)
# ktao cửa sổ trò chơi
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Generator")
# ktao biến và hso
done = False  # biến kiểm tra xem chương trình đã kết thúc chưa.
clock = pygame.time.Clock()
width = 25
cols = int(size[0] / width)
rows = int(size[1] / width)  # số lượng cột và hàng trong mê cung
stack = []  # ngăn xếp dùng để lưu trữ các ô đã được ghé thăm.


class Cell():
    def __init__(self, x, y):
        global width
        self.x = x * width
        self.y = y * width
        self.visited = False  # biểu thị xem ô đã được ghé thăm hay chưa
        self.current = False  # biểu thị xem ô đó đang được xem là ô hiện tại hay không
        self.walls = [True, True, True, True]  # biểu thị xem ô có tường ở các hướng  top , right , bottom , left
        # neighbors
        self.neighbors = []  # danh sách các ô hàng xóm chưa được ghé thăm.
        # các biến tham chiếu đến ô hàng xóm theo các hướng.
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        # ô tiếp theo sẽ được ghé thăm.
        self.next_cell = 0

    def draw(self):
        #Nếu ô là ô hiện tại, vẽ một hình chữ nhật màu đỏ tại vị trí của ô.
        if self.current:
            pygame.draw.rect(screen, RED, (self.x, self.y, width, width))
        #Nếu ô đã được ghé thăm, vẽ một hình chữ nhật màu trắng tại vị trí của ô và vẽ các tường xung quanh ô nếu có.
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))
            if self.walls[0]:
                pygame.draw.line(screen, RED, (self.x, self.y), ((self.x + width), self.y), 1)  # top
            if self.walls[1]:
                pygame.draw.line(screen, RED, ((self.x + width), self.y), ((self.x + width), (self.y + width)), 1)  # right
            if self.walls[2]:
                pygame.draw.line(screen, RED, ((self.x + width), (self.y + width)), (self.x, (self.y + width)), 1)  # bottom
            if self.walls[3]:
                pygame.draw.line(screen, RED, (self.x, (self.y + width)), (self.x, self.y), 1)  # left

    def checkNeighbors(self):
        #tính toán vị trí của các ô láng giềng trong mê cung dựa trên vị trí của ô hiện tại
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        # Nếu ô láng giềng chưa được thăm sẽ được thêm vào ds láng giềng
        if self.top != 0:
            if self.top.visited == False:
                self.neighbors.append(self.top)
        if self.right != 0:
            if self.right.visited == False:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if self.bottom.visited == False:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if self.left.visited == False:
                self.neighbors.append(self.left)
        # Nếu ds láng giềng ko rỗng thì chọn ngẫu nhiên 1 hàng xóm để đi tiếp
        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0, len(self.neighbors))]
            return self.next_cell
        else:
            return False

# Hàm xoá tường sử dụng để loại bỏ các tường giữa hai ô liền kề
def removeWalls(current_cell, next_cell):
    # Tính vị trí khác biệt current_cell và next_cell theo chiều ngang (x) và chiều dọc (y).
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)

    if x == -1:  # right of current
        # Tường bên phải của current_cell sẽ bị loại bỏ và tường bên trái của next_cell cũng bị loại bỏ.
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1:  # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1:  # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1:  # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False

# Tạo một biến danh sách hai chiều để lưu trữ các ô trong mê cung.
grid = []
for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x, y))
current_cell = grid[0][0]
next_cell = 0
# Vòng lặp chính
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(GREY)
    # Đánh dấu ô hiện tại đã thăm
    current_cell.visited = True
    current_cell.current = True
    # Vẽ tất cả các ô trong mê cung
    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw()
    # Kiểm tra và trả về các ô láng giềng chưa được thăm
    next_cell = current_cell.checkNeighbors()
    # Nếu láng giềng chưa được thăm
    if next_cell != False:
        current_cell.neighbors = []
        stack.append(current_cell)
        removeWalls(current_cell, next_cell)
        current_cell.current = False
        current_cell = next_cell
    # Nếu không có láng giềng chưa được thăm kiểm tra stack
    elif len(stack) > 0:
        current_cell.current = False
        current_cell = stack.pop()
    # Nếu stack rỗng là chúng ta đã hoàn thành mê cung
    elif len(stack) == 0:
        grid = []
        for y in range(rows):
            grid.append([])
            for x in range(cols):
                grid[y].append(Cell(x, y))
        current_cell = grid[0][0]
        next_cell = 0
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
