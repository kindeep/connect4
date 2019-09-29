from display import *
import sys
import time


def move(num, controller):
    move = controller.click_exec(num)
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if move:
        display.add_to_animate(Ball(start_rect_click, curr_color, move[1], num))
    if move:
        return True
    else:
        return False


def ai_move(num):
    print("main, determined move: ", num)
    print("main, board before move: ", curr_game.grid.to_string())
    the_move = curr_game.execute_move(int(num))
    start_rect_click = pygame.Rect(*display.get_box(num, -1))
    if the_move:
        display.add_to_animate(Ball(start_rect_click, curr_color, the_move[1], num))
    if the_move:
        return True
    else:
        return False


curr_game = ConnectGame()

controller = Controller(curr_game)

display = Display(curr_game, controller)

ai = AIPlayer(curr_game)

# class ClickPlayer(Player):
#
#
# player1 = ClickPlayer(curr_game)
# player2 = AIPlayer(curr_game)

display.draw_loop()

ai_movee = False

while True:
    for event in pygame.event.get():
        if ai_movee:
            ai = AIPlayer(curr_game)
            start_time = time.time()
            ai_move(ai.determine_move())
            print("Time taken: ", time.time() - start_time)
            ai_movee = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            curr_color = Colors.get_tile_color(curr_game.turn_count.get_curr_turn())
            pos = pygame.mouse.get_pos()
            click_pos = display.resolve_click(*pos)
            if move(click_pos[0], controller):
                ai_movee = True

    display.faster_draw()
    # display.draw()
    # if display.to_animate():
    # display.draw_loop()
    pygame.display.update()
