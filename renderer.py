import pygame
import sys

class Renderer:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
    LANE_LENGTH = 10
    LANE_WIDTH = 40
    CAR_SIZE = 32
    INTERSECTION_SIZE = 200
    STEP = 60  # Distance between cars on lane

    # Define colors
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    RED = (255, 0, 0)
    GREEN = (0, 230, 0)
    YELLOW = (255, 215, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (90, 90, 90)
    BLUE = (0, 0, 255)

    def __init__(self, car_grid=None, state=0):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Four-way Traffic Intersection")
        self.clock = pygame.time.Clock()
        self.car_grid = car_grid if car_grid is not None else [
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],  # North
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],  # East
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],  # South
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 1],  # West
        ]
        self.state = state
        self.draw(self.car_grid, self.state)

    def draw_roads(self):
        # Vertical
        pygame.draw.rect(self.screen, self.DARK_GRAY, (
            self.SCREEN_WIDTH//2 - self.LANE_WIDTH, 0, self.LANE_WIDTH*2, self.SCREEN_HEIGHT))
        # Horizontal
        pygame.draw.rect(self.screen, self.DARK_GRAY, (
            0, self.SCREEN_HEIGHT//2 - self.LANE_WIDTH, self.SCREEN_WIDTH, self.LANE_WIDTH*2))
        # Intersection
        pygame.draw.rect(self.screen, self.GRAY, (
            self.SCREEN_WIDTH//2 - self.INTERSECTION_SIZE//2,
            self.SCREEN_HEIGHT//2 - self.INTERSECTION_SIZE//2,
            self.INTERSECTION_SIZE,
            self.INTERSECTION_SIZE,
        ))

    def draw_traffic_lights(self, state):
        offset = 90
        light_size = 32
        positions = [
            (self.SCREEN_WIDTH//2 - self.LANE_WIDTH-light_size, self.SCREEN_HEIGHT//2 - self.INTERSECTION_SIZE//2 - offset),  # North
            (self.SCREEN_WIDTH//2 + self.INTERSECTION_SIZE//2 + offset - light_size, self.SCREEN_HEIGHT//2 - light_size-self.LANE_WIDTH),  # East
            (self.SCREEN_WIDTH//2  + self.LANE_WIDTH, self.SCREEN_HEIGHT//2 + self.INTERSECTION_SIZE//2 + offset - light_size),  # South
            (self.SCREEN_WIDTH//2 - self.INTERSECTION_SIZE//2 - offset, self.SCREEN_HEIGHT//2 +self.LANE_WIDTH)  # West
        ]
        light_states = [
            state ==0,  # North-South green, East-West red
            state ==1,  # East-West green, North-South red
            state ==2,  # South same as North
            state ==3,  # West same as East
        ]
        for i in range(4):
            pygame.draw.rect(self.screen, self.BLACK, (*positions[i], light_size, light_size))
            color = self.GREEN if light_states[i] else self.RED
            pygame.draw.circle(self.screen, color,
                               (positions[i][0]+light_size//2, positions[i][1]+light_size//2),
                               light_size//3)

    def draw_cars(self, grid):
        mid_x, mid_y = self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2
        for lane, cars in enumerate(grid):
            for idx, present in enumerate(cars):
                if not present:
                    continue
                if lane == 0:  # North - going down
                    x = mid_x - self.CAR_SIZE//2
                    y = mid_y - self.INTERSECTION_SIZE//2 - (idx+1)*self.STEP
                elif lane == 1:  # East - going left
                    x = mid_x + self.INTERSECTION_SIZE//2 + idx*self.STEP
                    y = mid_y - self.CAR_SIZE//2
                elif lane == 2:  # South - going up
                    x = mid_x - self.CAR_SIZE//2
                    y = mid_y + self.INTERSECTION_SIZE//2 + idx*self.STEP
                elif lane == 3:  # West - going right
                    x = mid_x - self.INTERSECTION_SIZE//2 - (idx+1)*self.STEP
                    y = mid_y - self.CAR_SIZE//2
                pygame.draw.rect(self.screen, self.BLUE, (x, y, self.CAR_SIZE, self.CAR_SIZE))

    def draw(self, car_grid=None, state=None):
        pygame.event.pump()
        if car_grid is not None:
            self.car_grid = car_grid
        if state is not None:
            self.state = state
        self.screen.fill(self.WHITE)
        self.draw_roads()
        self.draw_traffic_lights(self.state)
        self.draw_cars(self.car_grid)
        pygame.display.flip()

    def update_car_grid(self, grid, action):
        self.car_grid = grid
        self.state = action
        self.draw(self.car_grid, self.state)

    def run(self):
        running = True
        traffic_timer = 0
        self.state = 0  # 0/1: NS green, 2/3: EW green, (basic 2-phase)
        self.draw(self.car_grid, self.state)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            traffic_timer += 1
            if traffic_timer > 120:
                self.state = (self.state + 1) % 4
                traffic_timer = 0
            self.draw(self.car_grid, self.state)
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()
