import pygame
import sys
import numpy as np

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ và màu sắc
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
LINE_WIDTH = 2

# Số dòng và cột (15x15 cho Caro)
BOARD_ROWS = 15
BOARD_COLS = 15
SQUARE_SIZE = WIDTH // BOARD_ROWS

# Thiết lập cửa sổ game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Caro Game - Chế độ người chơi vs người chơi')

# Tạo bảng cờ
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Phông chữ cho thông báo
font_path = "Roboto-MediumItalic.ttf"  # Đường dẫn đến file font
custom_font = pygame.font.Font(font_path, 36)

# Vẽ bảng cờ Caro
def draw_lines():
    screen.fill(BG_COLOR)
    
    # Vẽ các đường ngang và dọc
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Đánh dấu X hoặc O lên bảng cờ
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), LINE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, O_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 3, LINE_WIDTH)

# Hiển thị thông báo
def display_message(message):
    # Làm sạch màn hình
    screen.fill(BG_COLOR)
    
    # Hiển thị thông điệp
    text = custom_font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Dừng màn hình trong 2 giây để người chơi có thể đọc thông báo

# Đánh dấu vào ô đã chọn
def mark_square(row, col, player):
    board[row][col] = player

# Kiểm tra xem ô đã được đánh chưa
def available_square(row, col):
    return board[row][col] == 0

# Kiểm tra điều kiện thắng (5 quân liên tiếp)
def check_win(player):
    # Kiểm tra hàng ngang
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player \
                and board[row][col + 3] == player and board[row][col + 4] == player:
                return True

    # Kiểm tra hàng dọc
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player \
                and board[row + 3][col] == player and board[row + 4][col] == player:
                return True

    # Kiểm tra đường chéo chính (\)
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player \
                and board[row + 3][col + 3] == player and board[row + 4][col + 4] == player:
                return True

    # Kiểm tra đường chéo phụ (/)
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player \
                and board[row - 3][col + 3] == player and board[row - 4][col + 4] == player:
                return True

    return False

# Kiểm tra xem bàn cờ đã đầy chưa
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Khởi tạo game
draw_lines()
player = 1  # Người chơi 1 là X
game_over = False

# Vòng lặp chính của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # tọa độ x của chuột
            mouseY = event.pos[1]  # tọa độ y của chuột

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()

                if check_win(player):
                    game_over = True
                    display_message(f'Người chơi {player} thắng!')

                elif is_board_full():
                    game_over = True
                    display_message('Hòa!')

                player = 3 - player  # Đổi lượt cho người chơi tiếp theo (1 -> 2, 2 -> 1)

            # Vẽ lại bảng cờ sau khi có thông báo
            draw_lines()
            draw_figures()

    pygame.display.update()
