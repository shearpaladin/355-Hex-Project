import pygame as pg
import sys
from os import path
from math import sqrt
from consts import *
from funcs import *
from Button import *

class Game:
    def __init__(self, size):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.size = size
        self.setTileSize()
        self.state = [[0 for _ in range(self.size)] for __ in range(self.size)]
        self.origin = Point(W/2 - (H/2-50)/sqrt(3), 50)
        self.move = 1
        self.started = False
        self.sound_state = True

    def loadData(self):
        '''load all the data (images, files, etc)'''
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder, 'images')
        sound_folder = path.join(game_folder, 'sounds')

        #------------------IMAGES------------------
        self.pause_img = pg.image.load(path.join(image_folder, PAUSE_IMG)).convert_alpha()
        self.back_img = pg.image.load(path.join(image_folder, BACK_IMG)).convert_alpha()
        self.up_img = pg.image.load(path.join(image_folder, UP_IMG)).convert_alpha()
        self.down_img = pg.image.load(path.join(image_folder, DOWN_IMG)).convert_alpha()

        #------------------SOUND--------------------
        self.tick_sound = pg.mixer.Sound(path.join(sound_folder, TICK_SOUND))
        self.tick_sound_channel = pg.mixer.Channel(1)
        self.click_sound = pg.mixer.Sound(path.join(sound_folder, CLICK_SOUND))
        self.click_sound_channel = pg.mixer.Channel(2)

    def setTileSize(self):
        self.tile_size = 4*(H/2-50)/3/sqrt(3)/(self.size-1)

    def coords(self, r, c):
        '''translates grid coordinates to real coordinates'''
        x = self.origin.x + c*3/2*self.tile_size
        y = self.origin.y + (c+2*r)*self.tile_size*sqrt(3)/2
        return int(x), int(y)

    def tick(self, pos):
        '''is called if mouse pressed, changes the state of the game'''
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if inHex(pos, x, y, self.tile_size) and self.state[r][c] != 2\
                                                    and self.state[r][c] != 1:
                    if self.sound_state:
                        self.tick_sound_channel.play(self.tick_sound)
                    self.state[r][c] = self.move
                    self.move = 3-self.move

    '''
    def highlight(self, pos):
        #highlights the hexagon that is under the mouse
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if self.state[r][c] == 0 and inHex(pos, x, y, self.tile_size):
                    self.state[r][c] = self.move + 2
                elif self.state[r][c] > 2 and not inHex(pos, x, y, self.tile_size):
                    self.state[r][c] = 0
    '''

    def showGrid(self):
        '''shows hexagonal grid as well as players moves and destination sides'''
        # draw bounds

        A = (self.origin.x-self.tile_size, self.origin.y-self.tile_size*sqrt(3))
        B = (self.origin.x-self.tile_size/2*(1-3*self.size),\
             self.origin.y+self.tile_size*sqrt(3)/2*(self.size-2)+self.tile_size*sqrt(3)/6)
        C = (self.origin.x-self.tile_size/2*(1-3*self.size), self.origin.y+self.tile_size*sqrt(3)/2*(2*self.size+self.size-1))
        D = (self.origin.x-self.tile_size, self.origin.y+self.tile_size*sqrt(3)*(self.size-1/2)-self.tile_size*sqrt(3)/6)
        M = ((A[0]+B[0])/2, (B[1]+C[1])/2)
        pg.draw.polygon(self.screen, RED, [A, B, M])
        pg.draw.polygon(self.screen, RED, [C, D, M])
        pg.draw.polygon(self.screen, BLUE, [B, C, M])
        pg.draw.polygon(self.screen, BLUE, [D, A, M])

        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)

                if self.state[r][c] == 1:
                    drawHex(self.screen, RED, BLACK, (x, y), self.tile_size)
                elif self.state[r][c] == 2:
                    drawHex(self.screen, BLUE, BLACK, (x, y), self.tile_size)
                else:
                    drawHex(self.screen, WHITE, BLACK, (x, y), self.tile_size)
                '''
                elif self.state[r][c] == 3:
                    drawHex(self.screen, LIGHTRED, BLACK, (x, y), self.tile_size)
                elif self.state[r][c] == 4:
                    drawHex(self.screen, LIGHTBLUE, BLACK, (x, y), self.tile_size)
                '''

    def checkWin(self):
        return game_status(self.state)

    def shadow(self):
        shadow = pg.Surface((W, H))
        shadow.set_alpha(200)
        self.screen.blit(shadow, (0, 0))

    def startScreen(self):
        '''shows start screen, returns True if the game has started'''
        start = True
        # initializing buttons
        play = Button((W/2, 2*H/3), 80, 'Play')
        settings = Button((W/2, H-75), 50, 'Settings')
        buttons = [play, settings]
        while start:
            # sticking to fps
            self.clock.tick(FPS)
            # --------------------EVENTS---------------------
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # if exit button is pressed
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if mouse is pressed check button overlapping
                    if play.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.__init__(self.size)
                        self.started = True
                        return True
                    if settings.triggered(channel=self.click_sound_channel,
                                          sound=self.click_sound,
                                          playing=self.sound_state):
                        start = self.settingsScreen()
            # highlight buttons
            for button in buttons:
                button.highlighted()
            # --------------------STUFF-----------------------
            self.screen.fill(WHITE)
            textOut(self.screen, 'HEX', 200, ORANGE, (W/2, H/3))
            # show buttons
            for button in buttons:
                button.show(self.screen)
            # double processing
            pg.display.flip()

    def settingsScreen(self):
        '''shows the rules of the game, returns True if the "back" button was hit'''
        start = True
        # initializing buttons
        back = Button((30, 30), 50, img=self.back_img)
        up = Button((2*W/3+60, H/2-25), 50, img=self.up_img)
        down = Button((2*W/3+60, H/2+25), 50, img=self.down_img)
        sound_state = 'On' if self.sound_state else 'Off'
        sound_switch = Button((2*W/3-50, H/2+120), 50, sound_state, col=DARKRED)
        buttons = [back, up, down, sound_switch]
        while start:
            # sticking to fps
            self.clock.tick(FPS)
            # --------------------EVENTS---------------------
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # if exit button is pressed
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if mouse is pressed check button overlapping
                    if back.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        return True
                    if up.triggered(channel=self.click_sound_channel,
                                    sound=self.click_sound,
                                    playing=self.sound_state):
                        self.size = min(MAX_BOARD_SIZE, self.size+1)
                    if down.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.size = max(MIN_BOARD_SIZE, self.size-1)
                    if sound_switch.triggered(channel=self.click_sound_channel,
                                              sound=self.click_sound,
                                              playing=self.sound_state):
                        if sound_switch.text == 'On':
                            self.sound_state = False
                            sound_switch.text = 'Off'
                        else:
                            self.sound_state = True
                            sound_switch.text = 'On'
            # highlight buttons
            for button in buttons:
                button.highlighted()
            # --------------------STUFF-----------------------
            self.screen.fill(WHITE)
            textOut(self.screen, 'Settings', 100, ORANGE, (W/2, H/4))
            textOut(self.screen, 'Board size:', 50, BLACK, (W/3, H/2))
            textOut(self.screen, self.size, 50, BLACK, (2*W/3, H/2))
            textOut(self.screen, 'Sound:', 50, BLACK, (W/3, H/2+120))
            # show buttons
            for button in buttons:
                button.show(self.screen)
            # double processing
            pg.display.flip()

    def pauseScreen(self):
        '''shows pause screen, returns True if the game was resumed'''
        start = True
        # initializing buttons
        resume = Button((W/2, H/3), 80, 'Resume', col=ORANGE)
        home = Button((W/2, H/2), 50, 'Home', col=WHITE)
        buttons = [home, resume]
        while start:
            # sticking to fps
            self.clock.tick(FPS)
            # --------------------EVENTS---------------------
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # if exit button is pressed
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if mouse is pressed check button overlapping
                    if home.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.started = False
                        return True
                    if resume.triggered(channel=self.click_sound_channel,
                                        sound=self.click_sound,
                                        playing=self.sound_state):
                        return True
            # highlight buttons
            for button in buttons:
                button.highlighted()
            # --------------------STUFF-----------------------
            # show buttons
            self.showGrid()
            self.shadow()
            for button in buttons:
                button.show(self.screen)
            # double processing
            pg.display.flip()

    def GOScreen(self, winner):
        '''shows game over screen, returns True if any key is hit'''
        go = True
        home = Button((W/2, 2*H/3), 50, 'Home', col=WHITE)
        while go:
            # sticking to fps
            self.clock.tick(FPS)
            # --------------------EVENTS---------------------
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # if exit button is pressed
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if mouse is pressed check button overlapping
                    if home.triggered(channel=self.click_sound_channel,
                                      sound=self.click_sound,
                                      playing=self.sound_state):
                        self.started = False
                        return True
            home.highlighted()
            # --------------------STUFF-----------------------
            self.showGrid()
            self.shadow()
            textOut(self.screen, 'GAME OVER', 80, ORANGE, (W/2, H/3))
            if winner == 2:
                textOut(self.screen, 'Blue won', 60, BLUE, (W/2, H/2))
            else:
                textOut(self.screen, 'Red won', 60, RED, (W/2, H/2))
            home.show(self.screen)
            # double processing
            pg.display.flip()
