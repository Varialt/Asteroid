from pygame.transform import rotate
from shot import Shot
import circleshape, pygame, constants

class Player(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = constants.PLAYER_RADIUS, rotation: int = 0) -> None:
        super().__init__(x, y, radius)
        self.rotation = rotation
        self.shoot_timer = 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

    def rotate(self,dt):
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shoot_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shoot_timer > 0:
            return
        else:
            self.shoot_timer = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
            pew = Shot(self.position.x,self.position.y)
            unit_vector = pygame.Vector2(0, 1)
            rotated_vector = unit_vector.rotate(self.rotation)
            rotated_with_speed_vector = rotated_vector * constants.PLAYER_SHOOT_SPEED
            pew.velocity += rotated_with_speed_vector
