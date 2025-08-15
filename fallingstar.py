import pygame
import random
import time
import os
import sys  # ✅ Import sys for safe quitting

pygame.init()

# window for the game
width = 800
height = 500
win = pygame.display.set_mode((width, height))

transparent_surface = pygame.Surface((550, 300), pygame.SRCALPHA)
transparent_surface.fill((10, 10, 10, 210))


# name of the game
pygame.display.set_caption("Raising Stars")

#icon for the game window
icon = pygame.image.load("assets/images/game_icon.png")
icon = pygame.transform.scale(icon,(100,100))
pygame.display.set_icon(icon)

# background image for menu
menubg = pygame.image.load("assets/images/menu_back.jpg")
menubg = pygame.transform.scale(menubg, (width, height))

# background image
bgimg = pygame.image.load("assets/images/background.jpg")
bgimg = pygame.transform.scale(bgimg, (width, height))

# background image for score page
scorebg = pygame.image.load("assets/images/score_bg.jpg")
scorebg = pygame.transform.scale(scorebg, (width, height))

# lifeline powerup images
heartimg = pygame.image.load("assets/images/heart_powerup.png")
heartimg = pygame.transform.scale(heartimg, (40, 40))

# menu click sound loading
click = pygame.mixer.Sound("assets/sounds/click.mp3")

#hit sound loading
hit_player = pygame.mixer.Sound("assets/sounds/hit.mp3")

# coin collet sound loading
collect = pygame.mixer.Sound("assets/sounds/collect.mp3")

# background sound
pygame.mixer.music.load("assets/sounds/theme.mp3")

# font to show on screen
font = pygame.font.Font(None, 30)

# credits
def credits():
    win.fill("black")
    creator = font.render("Created By HAIDER KHAN!", 3, "green")
    creds = font.render("Thanks for playing!", 2, "White")
    win.blit(creator, (width / 2 - 130, height / 2 - 50))
    win.blit(creds, (width / 2 - 100, height / 2 - 0))
    pygame.display.update()
    pygame.time.delay(2000)

# credits screen
def credits_on_click():
    credits = True
    while credits:
        win.blit(scorebg, (0, 0))
        creator = font.render("Created By HAIDER KHAN!", 3, "green")
        creds = font.render("Thanks for playing!", 2, "White")
        go_back = font.render("Press Backspace to return to menu", 2, "Red")
        win.blit(creator, (width / 2 - 130, height / 2 - 50))
        win.blit(creds, (width / 2 - 100, height / 2 - 0))
        win.blit(go_back, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # ✅ Safe exit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    click.play()
                    credits = False
                    pygame.time.delay(200)
                    break
        pygame.display.update()

def on_screen(player, stars, time, lives):
    time_text = font.render(f"Time: {round(time)}s", 1, "white")
    lives_text = font.render(f"Lives left: {lives}", 2, "White")

    

    win.blit(time_text, (20, 20))
    win.blit(lives_text, (20, 45))
    pygame.draw.rect(win, "blue", player)
    for star in stars[:]:
        pygame.draw.circle(win, "red", star.center, 20)

#get path for saving records
def get_score_path():
    # Get a safe, writable path for storing user data
    user_dir = os.getenv('APPDATA') or os.path.expanduser("~")
    score_dir = os.path.join(user_dir, "RaisingStars")
    os.makedirs(score_dir, exist_ok=True)  # create folder if not exists
    return os.path.join(score_dir, "highscore.txt")

# score handling
def load_highscore():
    try:
        with open(get_score_path(), "r") as file:
            return float(file.read())
    except:
        return 0.0

def save_highscore(score):
    try:
        with open(get_score_path(), "w") as file:
            file.write(str(score))
    except Exception as e:
        print("Failed to save highscore:", e)

def score():
    within_score = True
    while within_score:
        win.blit(scorebg, (0, 0))
        highscore = load_highscore()
        menu_high = font.render("High Score:", 2, "white")
        scores = font.render(f"{round(highscore)}s", 2, "green")
        win.blit(menu_high, (width / 2 - 100, height / 2 - 30))
        win.blit(scores, (width / 2 + 40, height / 2 - 30))
        return_menu = font.render(f"🔙 Press backspace to return to menu", 2, "red")
        win.blit(return_menu, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    click.play()
                    within_score = False
                    pygame.time.delay(200)
                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # ✅ Safe exit
        pygame.display.update()

# powerup render
def powerup(x, y):
    win.blit(heartimg, (x, y))

#pause menu
def pause(player, stars, current_time, no_of_hits):
    pygame.mixer.music.pause()
    pause_start = time.time()
#    win.fill("black")
    on_screen(player, stars, current_time, no_of_hits)
    paused = True
    while paused:
        
        win.blit(transparent_surface, (130, 100))

        #options
        menu_option1 = font.render(f"Press Enter to Unpause game", 2, "red")
        menu_option2 = font.render(f"Press E to Return to Menu", 2, "red")

        win.blit(menu_option1, (width / 2 - 140, height / 2 - 50))
        win.blit(menu_option2, (width / 2 - 125, height / 2))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    click.play()
                    paused = False
                    break

                if event.key == pygame.K_e:
                    click.play()
                    pygame.time.delay(500)
                    main()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # ✅ Safe exit
        
        #on_screen(player, stars, current_time, no_of_hits)
        pygame.display.flip()
        pygame.display.update()

    new_time = time.time() - pause_start
    pygame.mixer.music.unpause()
    return new_time
                



# menu
def main():
    credits()
    menu = True
    while menu:
        win.blit(menubg, (0, 0))
        menu_option1 = font.render(f"Press S to start game", 2, "yellow")
        menu_option2 = font.render(f"Press R to view HighScore", 2, "yellow")
        menu_option3 = font.render(f"Press C to view Credits", 2, "yellow")
        menu_option4 = font.render(f"Press Q to Quit game", 2, "yellow")

        win.blit(menu_option1, (width / 2 - 100, height / 2 - 80))
        win.blit(menu_option2, (width / 2 - 120, height / 2 - 30))
        win.blit(menu_option3, (width / 2 - 110, height / 2 + 20))
        win.blit(menu_option4, (width / 2 - 100, height / 2 + 70))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    click.play()
                    game()
                    break
                if event.key == pygame.K_r:
                    click.play()
                    pygame.time.delay(200)
                    score()
                    break
                if event.key == pygame.K_c:
                    click.play()
                    pygame.time.delay(200)
                    credits_on_click()
                    break
                if event.key == pygame.K_q:
                    click.play()
                    pygame.time.delay(200)
                    pygame.quit()
                    sys.exit()  # ✅ Safe exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # ✅ Safe exit
        pygame.display.update()

def game():
    #pygame.mixer.music.play(-1)
    FPS = 60
    start_time = time.time()
    ply_width = 30
    ply_height = 50
    ply_vel = 0
    player = pygame.Rect(width / 2, 500 - ply_height, ply_width, ply_height)

    stars = []
    star_width = 20
    star_height = 30
    star_vel = 10
    star_count = 0
    star_increment = 2000
    no_of_hits = 3
    hit = False
    life_x = random.randint(-10, 810)
    life_y = -40
    life_vel = 5

    clock = pygame.time.Clock()

    pausegame = font.render(f"Press ESC to Pause game", 2, "yellow")
    
    run = True
    while run:

        current_time = time.time() - start_time
        star_count += clock.tick(FPS)
        win.blit(bgimg, (0, 0))

        
        win.blit(pausegame,(530,20))

        if star_count >= star_increment:
            for _ in range(3):
                star_x = random.randint(-20, 820 - star_width)
                star = pygame.Rect(star_x, -star_height, star_width, star_height)
                stars.append((star))
            star_count = 0
            star_increment = max(400, star_increment - 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()  # ✅ Safe exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ply_vel = -5
                if event.key == pygame.K_RIGHT:
                    ply_vel = 5
                
                #for pause menu
                if event.key == pygame.K_ESCAPE:
                    click.play()
                    pause_duration = pause(player, stars, current_time, no_of_hits)
                    start_time += pause_duration

        player.x += ply_vel
        player.x = max(5, min(player.x, 765))

        for star in stars[:]:
            star.y += star_vel
            if star.y >= 530:
                stars.remove(star)
            if star.y + star.height >= player.y and star.colliderect(player):
                hit_player.play()
                stars.remove(star)
                no_of_hits -= 1
                if no_of_hits == 0:
                    pygame.time.delay(1000)
                    hit = True

        if hit:
            pygame.mixer.music.stop()
            win.blit(transparent_surface, (130, 100))
            highscore = load_highscore()
            if current_time > highscore:
                save_highscore(current_time)
                new_high = font.render(f"New High Score! {round(current_time)}", 1, "green")
                win.blit(new_high, (width / 2 - 85, height / 2 + 40))
            over = font.render(f"YOU LOST!", 1, "red")
            score_txt = font.render(f"You survived for {round(current_time)}s", 1, "white")
            win.blit(over, (width / 2 - 50, height / 2 - 40))
            win.blit(score_txt, (width / 2 - 90, height / 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return

        life_y += life_vel
        if life_y >= height:
            life_x = random.randint(0, width - 40)
            life_y = -4000

        if pygame.Rect(life_x, life_y, 40, 40).colliderect(player):
            collect.play()
            no_of_hits += 1
            life_x = random.randint(0, width - 40)
            life_y = -200

        powerup(life_x, life_y)
        on_screen(player, stars, current_time, no_of_hits)
        pygame.display.update()

    pygame.quit()
    sys.exit()  # ✅ Final safety exit

if __name__ == "__main__":
    main()
