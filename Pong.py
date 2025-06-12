import pygame

pygame.init()

window_width, window_height = 1540, 800 #1920, 1080 == seperate monitor #1540, 800 == laptop screen
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

pygame.mixer.music.load('Background_Music_Pong.mp3') # make sure the file is in the same folder
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

locationX = window_width / 2
locationY = window_height / 2
ball_speed_x = 5
ball_speed_y = 1
ball_acceleration = 0.01
y_paddle1 = window_height / 2 - 50
y_paddle2 = window_height / 2 - 50
font = pygame.font.Font(None, 74)
score1 = 0
score2 = 0

def Basic_Ball_Movement(locationX, locationY, ball_speed_x, ball_speed_y, ball_acceleration, score1, score2):
    pygame.draw.ellipse(window, (255, 255, 255), (locationX, locationY, 25, 25))
    locationX += ball_speed_x
    locationY += ball_speed_y
    if locationX >= window_width:
        score1 += 1
        locationX = window_width / 2
        locationY = window_height / 2
        ball_speed_x = 5
        ball_speed_y = 1
    elif locationX <= 0:
        score2 += 1
        locationX = window_width / 2
        locationY = window_height / 2
        ball_speed_x = 5
        ball_speed_y = 1
    else:
        ball_speed_x += ball_acceleration if ball_speed_x > 0 else -ball_acceleration
        ball_speed_y += ball_acceleration if ball_speed_y > 0 else -ball_acceleration
    return locationX, locationY, ball_speed_x, ball_speed_y, score1, score2


# Game loop
running = True
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))
    
    locationX, locationY, ball_speed_x, ball_speed_y, score1, score2 = Basic_Ball_Movement(locationX, locationY, ball_speed_x, ball_speed_y, ball_acceleration, score1, score2)
        
    # Check for collision with paddles
    ball_rect = pygame.Rect(locationX, locationY, 25, 25)
    paddle1_rect = pygame.Rect(window_width - 25, y_paddle1, 25, 125)
    paddle2_rect = pygame.Rect(0, y_paddle2, 25, 125)

    if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
        ball_speed_x = -ball_speed_x  # Reverse the horizontal direction

    

    # Check for collision with top and bottom walls
    if locationY <= 25 or locationY >= (window_height - 50):
        ball_speed_y = -ball_speed_y  # Reverse the vertical direction

    # Draw yellow lines at the top and bottom edges
    pygame.draw.line(window, (255, 255, 0), (0, 0), (window_width, 0), 25)
    pygame.draw.line(window, (255, 255, 0), (0, window_height - 12.5), (window_width, window_height - 12.5), 25)
    
    # Basic Paddles Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] and y_paddle2 > 0:
        y_paddle2 -= 10
    if keys[pygame.K_s] and y_paddle2 < window_height - 125:
        y_paddle2 += 10
    if keys[pygame.K_ESCAPE]:
        running = False
    # AI for paddle1
    if locationY < y_paddle1 + 62.5 and y_paddle1 > 0:
        y_paddle1 -= 10
    if locationY > y_paddle1 + 62.5 and y_paddle1 < window_height - 125:
        y_paddle1 += 10
            
    paddle1_rect.y = y_paddle1
    paddle2_rect.y = y_paddle2
    pygame.draw.rect(window, (0, 255, 0), paddle1_rect)
    pygame.draw.rect(window, (255, 0, 0), paddle2_rect)

    # Render scores
    score_text1 = font.render(str(score1), True, (255, 255, 255))
    score_text2 = font.render(str(score2), True, (255, 255, 255))

    # Display scores
    window.blit(score_text1, (50, window_height - 100))
    window.blit(score_text2, (window_width - 100, window_height - 100))

    # If the difference in scores is 5, game over
    if abs(score1 - score2) >= 5:
        if score1 > score2:
            game_over = font.render("You Win!", True, (255, 255, 255))
        else:
            game_over = font.render("GAME OVER", True, (255, 255, 255))
        window.fill((0, 0, 0))
        window.blit(game_over, (window_width/2 - game_over.get_width()/2, window_height/2 - game_over.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before quitting
        running = False
    
    pygame.display.flip()