import pygame
import math
from random import randint


class NewGame():
    def __init__(self):
        pygame.init()

        self.load_images()
        
        self.width = 640
        self.height = 480

        self.speed = 2
        self.coin_speed = 1
        self.points = 0
        self.points_needed = 10
        self.door_appears = False
        self.lower_bound = self.height - self.robot.get_height()

        self.new_game()
        
        self.window = pygame.display.set_mode((self.width, self.height))
        
        pygame.display.set_caption("Falling Coins")

        self.game_font = pygame.font.SysFont("Arial", 24)

        self.main_loop()

    def load_images(self):
        self.robot = pygame.image.load('images/robot.png')
        self.coin = pygame.image.load('images/coin.png')
        self.monster = pygame.image.load('images/monster.png')
        self.door = pygame.image.load('images/door.png')
        

    def new_game(self):
        # starting positions of everything
        self.robot_x = self.width / 2
        self.robot_y = self.height - self.robot.get_height()
        
        self.points = 0
        self.level = 1

        self.coin_numbers = 7
        self.monster_numbers = 3
        self.door_numbers = 0
        
        

        self.coin_position = []
        self.monster_position = []
        self.door_position = []
        
        

        for i in range(self.coin_numbers):
            coin_x = randint(0, self.width - self.coin.get_width())
            coin_y = -randint(100, 1000)
            self.coin_position.append([coin_x, coin_y])

        self.right_side_monsters = randint(0, self.monster_numbers)
        for i in range(self.monster_numbers - self.right_side_monsters):
            monster_x = -randint(100, 2000)
            monster_y = self.height - self.monster.get_height()
            self.monster_position.append([monster_x, monster_y])

        for i in range(self.right_side_monsters):
            monster_x = randint(self.width + 100, 2000)
            monster_y = self.height - self.monster.get_height()
            self.monster_position.append([monster_x, monster_y])

        self.to_left = False
        self.to_right = False
        self.to_up = False

        self.clock = pygame.time.Clock()


    def move_robot(self, move_x):
        x = self.robot_x
        x += move_x
        if move_x < 0:            
            self.robot_x = max(0, x)
        else:
            self.robot_x = min(self.width - self.robot.get_width(), x)

    def jump_up(self):
        if self.robot_y > self.lower_bound - 160:
            self.robot_y -= 4

        if self.robot_y == self.lower_bound - 160:
            self.to_up = False

        
    def jump_down(self):
        if self.robot_y < self.lower_bound:
            self.robot_y += 4
        
    def robot_touched(self, thing, thing_x, thing_y):
        if thing_y + thing.get_height() >= self.robot_y and thing_y <= self.robot_y + self.robot.get_height():
            if thing_x + thing.get_width() >= self.robot_x and thing_x <= self.robot_x + self.robot.get_width():
                return True
        return False
    
    def robot_touched_door(self, door_x, door_y):
        if door_y == self.robot_y + self.robot.get_height():
            if self.robot_x + self.robot.get_width() >= door_x and self.robot_x <= door_x + self.door.get_width():
                return True
        return False
    

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    if self.robot_y == self.lower_bound:
                        self.to_up = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                
            if event.type == pygame.QUIT:
                exit()


    def draw_window(self):
        # rgb numbers for light blue background
        self.window.fill((54, 194, 206))

        self.window.blit(self.robot, (self.robot_x, self.robot_y))

        for i in range(self.coin_numbers):
            self.window.blit(self.coin, (self.coin_position[i][0], self.coin_position[i][1]))
        
        for j in range(self.monster_numbers):
            self.window.blit(self.monster, (self.monster_position[j][0], self.monster_position[j][1]))
        
        for i in range(self.door_numbers):
            self.window.blit(self.door, (self.door_position[i][0], self.door_position[i][1]))
        
        game_text = self.game_font.render("Points: " + str(self.points), True, (255, 0, 0))
        self.window.blit(game_text, (25, 25))

        if self.points < 1:
            game_text = self.game_font.render("Use Arrow Keys", True, (255, 0, 0))
            self.window.blit(game_text, (200, 25))

        game_text = self.game_font.render("Level:  " + str(self.level), True, (255, 0, 0))
        self.window.blit(game_text, (500, 25))

        pygame.display.flip()

    def check_action(self):
        for i in range(self.coin_numbers):
            if self.robot_touched(self.coin, self.coin_position[i][0], self.coin_position[i][1]):
                self.coin_position[i][1] = randint(0, self.width - self.coin.get_width())
                self.coin_position[i][1] = -randint(100, 1000)
                self.points += 1

                # for every multiplier of 10 the points reach level increases by 1
                if self.points % 10 == 0:
                    self.level += 1
                    # everytime level increases the coin discending speed increases
                    self.coin_speed += 0.1
                

        for i in range(self.monster_numbers):
            if self.robot_touched(self.monster, self.monster_position[i][0], self.monster_position[i][1]):
                exit()

        

        if self.points == self.points_needed:
            self.door_appears = True

            self.points_needed += 10

    def move_objects(self):

        for i in range(self.coin_numbers):
            self.coin_position[i][1] += self.coin_speed

            if self.coin_position[i][1] > self.height - self.coin.get_height():
                self.coin_position[i][1] = randint(0, self.width - self.coin.get_width())
                self.coin_position[i][1] = -randint(100, 3000)

        for j in range(self.monster_numbers - self.right_side_monsters):
            self.monster_position[j][0] += 1

            if self.monster_position[j][0] > self.width:
                self.monster_position[j][0] = -randint(100, 1000)

        for j in range(self.right_side_monsters):
            self.monster_position[j][0] -= 1

            if self.monster_position[j][0] < 0 - self.monster.get_width():
                self.monster_position[j][0] = randint(self.width + 100, 2000)

        

        if self.to_left:
            self.move_robot(-self.speed)

        if self.to_right:
            self.move_robot(self.speed)

        if self.to_up:       
            self.jump_up()
        else:
            self.jump_down()

        if self.door_appears:
            self.door_numbers += 1
            # the more points user has the more door appears
            # doors will add difficulty to see coins and increase difficuty
            door_x = randint(0, self.width - self.door.get_width() - 100)
            door_y = randint(100, self.height - self.door.get_height())
            self.door_position.append([door_x, door_y])
            self.door_appears = False
        
        if self.door_numbers > 0:
            for i in range(self.door_numbers):
                
                if self.door_position[i][1] == self.robot_y + self.robot.get_height():
                    if self.robot_x + self.robot.get_width() >= self.door_position[i][0] and self.robot_x <= self.door_position[i][0] + self.door.get_width():
                    
                        self.lower_bound = self.door_position[i][1] - self.robot.get_height()
                        print('lower bound:', self.lower_bound, "on door", i)
                        pygame.draw.line(self.window, (0, 255, 255), (0, self.door_position[i][1]), (640, self.door_position[i][1]), 2)
                else:
                    self.lower_bound = self.height - self.robot.get_height()
        

        self.clock.tick(60)

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.check_action()
            self.move_objects()

if __name__ == '__main__':
    NewGame()