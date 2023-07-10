import pygame, sys

def surrounded_property(x, y, turn, list_property, board_size):
    direction = [0, 0]
    sided_square = False
    for y_sur in range(y-1,y+2):
        y_sur = min(y_sur, board_size[0]-1)
        y_sur = max(y_sur, 0)
        if list_property[y_sur][x] == str(turn) and y_sur!=y:
            sided_square = True
            direction = [0,  int((y - y_sur)/abs(y-y_sur))]
    for x_sur in range(x-1, x+2):
        x_sur = min(x_sur, board_size[0]-1)
        x_sur = max(x_sur, 0)
        if list_property[y][x_sur] == str(turn) and x_sur!=x:
            sided_square = True
            direction = [int((x-x_sur)/abs(x-x_sur)), 0]
    return sided_square, direction


def create_buttons(coord_buttons, button_color, button_text, click, mx, my, win, font):
    buttons = []
    button_ind = None
    click = False
    for n_button in range(len(coord_buttons)):
        coord = coord_buttons[n_button]
        buttons += [pygame.Rect(coord)]
        button = buttons[n_button]
        pygame.draw.rect(win, button_color, button)
        text = button_text[n_button]
        draw_text_centered(text, font, (0, 0, 0), win, coord[0]+coord[2]/2, coord[1]+coord[3]/2)
        if button.collidepoint((mx, my)) and click:
            button_ind = n_button
            click = True
    return button_ind, click


def draw_text_centered(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    x -= textobj.get_width()/2
    y -= textobj.get_height()/2
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_text_top_left(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def conf_menu(screen, mx, my, conf_text, window_x, window_y, language):
    clock = pygame.time.Clock()
    black = (0, 0, 0)
    x = mx
    y = my
    font_conf = pygame.font.SysFont(None, 20)
    if y > (window_y-90):
        y = window_y-90
    if x>(window_x-100):
        x = window_x-100
    coord_conf = (x, y, 100, 30)
    coord_pass = (x, y+30, 100, 30)
    coord_canc = (x, y+60, 100, 30)
    canc_button = pygame.Rect(coord_canc)
    confirm_button = pygame.Rect(coord_conf)
    pass_button = pygame.Rect(coord_pass)
    run = True
    click = False
    confirm = False
    conf_pass = False
    while run:
        clock.tick(30)
        click = False
        mx, my = pygame.mouse.get_pos()
        return_key = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    return_key = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.draw.rect(screen, (100, 100, 100), confirm_button)
        pygame.draw.rect(screen, (100, 100, 100), pass_button)
        pygame.draw.rect(screen, (100, 100, 100), canc_button)
        pygame.draw.rect(screen, (0, 0, 0), confirm_button, 2)
        pygame.draw.rect(screen, (0, 0, 0), pass_button, 2)
        pygame.draw.rect(screen, (0, 0, 0), canc_button, 2)
        draw_text_centered(conf_text, font_conf, black, screen, x+50, y+15)
        if language == 'Spanish':
            draw_text_centered("Pasar", font_conf, black, screen, x+50, y+45)
            draw_text_centered("Cancelar", font_conf, black, screen, x+50, y+75)
        elif language == 'English':
            draw_text_centered("Pass", font_conf, black, screen, x+50, y+45)
            draw_text_centered("Cancel", font_conf, black, screen, x+50, y+75)
        pygame.display.update()
        if return_key:
            confirm = True
            run = False
        if click:
            if confirm_button.collidepoint((mx, my)):
                confirm = True
            if pass_button.collidepoint((mx, my)):
                conf_pass = True
            run = False
    return confirm, conf_pass