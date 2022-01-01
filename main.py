import os
import pygame
import random

pygame.init()

# 색
background_color = (252, 246, 245)
mine_color = (123, 154, 204)
line_color = (120, 122, 145)

# 폰트
tile_font = pygame.font.Font(None, 50)

# 스크린
display_info = pygame.display.Info()
screen_width = display_info.current_w * 0.6
screen_height = display_info.current_h * 0.8
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("지뢰찾기")

# fps
clock = pygame.time.Clock()
fps = 30

# 폴더 경로 지정
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

def getImage(file):
    return pygame.image.load(os.path.join(image_path, file))

# 이미지
tile_image = getImage("tile.png")
tile_selected_image = getImage("tile_selected.png")
tile_opened_image = getImage("tile_opened.png")
mine_image = getImage("mine.png")
flag_image = getImage("flag.png")

# 길이
mine_width, mine_height = mine_image.get_rect().size
flag_width, flag_height = flag_image.get_rect().size

mine_size = 50
line_size = 3
tile_size = mine_size + line_size

# 지뢰
mine_count = 20
tile_width, tile_height = (12, 10)

board = [[{"flag": 0, "count": 0, "mine": False} for _ in range(tile_width)] for _ in range(tile_height)]
board_left = (screen_width - tile_width * tile_size) / 2
board_top = (screen_height - tile_height * tile_size) / 2

running = True

def getBoard(x, y):
    return board[y][x]

def addMineCount(x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x + i >= 0 and x + i < tile_width and y + j >= 0 and y + j < tile_height:
                tile = getBoard(x + i, y + j)
                tile["count"] += 1

def setRandomMine():
    for _ in range(mine_count):
        while True:
            x = random.randrange(0, tile_width)
            y = random.randrange(0, tile_height)
            tile = getBoard(x, y)
            if not tile["mine"]:
                tile["mine"] = True
                addMineCount(x, y)
                break

def openTile(x, y):
    if x >= 0 and x < tile_width and y >= 0 and y < tile_height:
        tile = getBoard(x, y)
        if tile["flag"] == 0:
            tile["flag"] = 1
            if tile["count"] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if x + i >= 0 and x + i < tile_width and y + j >= 0 and y + j < tile_height and x != x + i or y != y + j:
                            openTile(x + i, y + j)
                        
def flagTile(x, y):
    tile = getBoard(x, y)
    if tile["flag"] == 0:
        tile["flag"] = 2
    elif tile["flag"] == 2:
        tile["flag"] = 0

def onTileClicked(button):
    mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
    x = int((mouse_x_pos - board_left) // tile_size)
    y = int((mouse_y_pos - board_top) // tile_size)
    if button == 1:
        openTile(x, y)
    elif button == 3:
        flagTile(x, y)

def showMines():
    for x in range(tile_width):
        for y in range(tile_height):
            tile = getBoard(x, y)
            if tile["mine"]:
                mine_x_pos = board_left + (tile_size - mine_width) / 2 + x * tile_size
                mine_y_pos = board_top + (tile_size - mine_height) / 2 + y * tile_size
                screen.blit(mine_image, (mine_x_pos, mine_y_pos))

def showFlag(x, y):
    flag_x_pos = board_left + (tile_size - flag_width) / 2 + x * tile_size
    flag_y_pos = board_top + (tile_size - flag_height) / 2 + y * tile_size
    screen.blit(flag_image, (flag_x_pos, flag_y_pos)) 

def showCount(x, y):
    tile = getBoard(x, y)
    if tile["count"] != 0:
        count = tile_font.render(str(tile["count"]), True, (0, 0, 0))
        count_width, count_height = count.get_rect().size
        count_x_pos = board_left + (tile_size - count_width) / 2 + x * tile_size
        count_y_pos = board_top + (tile_size - count_height) / 2 + y * tile_size
        
        screen.blit(count, (count_x_pos, count_y_pos))

def drawBoard():
    for height in range(tile_height):
        for width in range(tile_width):
            screen.blit(tile_image, (board_left + width*(mine_size + line_size), board_top + height*(mine_size + line_size)))

def drawLine():
    for height in range(1, tile_height):
        pygame.draw.line(screen, line_color, (board_left, board_top + height*(mine_size + line_size) - 2), (board_left + tile_width*(mine_size + line_size) - 4, board_top + height*(mine_size + line_size) - 2), line_size)
    for width in range(1, tile_width):
        pygame.draw.line(screen, line_color, (board_left + width*(mine_size + line_size) - 2, board_top), (board_left + width*(mine_size + line_size) - 2, board_top + tile_height*(mine_size + line_size) - 4), line_size)
    
def drawMouseOverTile():
    mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
    x = int((mouse_x_pos - board_left) // tile_size)
    y = int((mouse_y_pos - board_top) // tile_size)

    if x >= 0 and x < tile_width and y >= 0 and y < tile_height:  
        screen.blit(tile_selected_image, (board_left + x * tile_size, board_top + y * tile_size))
    

def event():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            onTileClicked(event.button)

def checkMine(x, y):
    tile = getBoard(x, y)
    if tile["mine"]:
        pygame.draw.rect(screen, (255, 0, 0), (board_left + x * tile_size, board_top + y * tile_size, mine_size, mine_size))
        showMines()
    else:
        screen.blit(tile_opened_image, (board_left + x * tile_size, board_top + y * tile_size))
        showCount(x, y)

def checkTileFlags():
    for x in range(tile_width):
        for y in range(tile_height):
            tile = getBoard(x, y)
            flag = tile["flag"]
            if flag == 1:
                checkMine(x, y)
            if flag == 2:
                showFlag(x, y)


setRandomMine()

while running:
    dt = clock.tick(fps)

    screen.fill(background_color)
    drawBoard()
    drawLine()
    
    drawMouseOverTile()
    
    checkTileFlags()
    
    event()

    pygame.display.update()

pygame.quit()