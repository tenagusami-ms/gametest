from __future__ import annotations

import random

import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, RLEACCEL


def main():
    """
    メイン関数
    """
    pygame.mixer.init()  # pygame音源ミキサ初期化
    pygame.init()  # pygame初期化
    clock = pygame.time.Clock()
    screen_width = 1300  # 画面幅
    screen_height = 700  # 画面高さ
    pygame.display.set_mode((screen_width, screen_height), 0, 32)  # 画面セット
    screen = pygame.display.get_surface()  # スクリーンのSurfaceオブジェクト
    pygame.display.set_caption("Pygame Test")  # ウィンドウタイトル
    background = pygame.image.load("image/sakaiura.JPG").convert_alpha()  # 背景画像の指定
    background.set_colorkey((255, 255, 255), RLEACCEL)
    rectangle_background = background.get_rect()  # 画像を含む長方形オブジェクト

    add_enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(add_enemy, 250)
    player = Player(screen_width // 2, screen_height // 2, screen_width, screen_height)
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    pygame.mixer.music.load("sound/ImpactBall_BGM.mp3")
    pygame.mixer.music.play(loops=-1)
    collision_sound = pygame.mixer.Sound("sound/bound.mp3")

    running: bool = True
    while running:
        pressed_key = pygame.key.get_pressed()
        player.update(pressed_key)
        enemies.update()
        screen.fill((0, 0, 0, 0))  # 背景色の指定。RGBのはず
        screen.blit(background, rectangle_background)  # 背景画像の描画

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()  # 画面を更新
        clock.tick(30)

        if pygame.sprite.spritecollideany(player, enemies):
            collision_sound.play()
            player.kill()
            running = False

        for event in pygame.event.get():  # 終了処理
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == add_enemy:
                new_enemy = Enemy(screen_width, screen_height)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    pygame.quit()  # pygame終了
    pygame.mixer.quit()  # ミキサ終了


class Player(pygame.sprite.Sprite):
    """
    プレーヤーのスプライト
    """
    def __init__(self, x, y, screen_width, screen_height):
        """
        コンストラクタ

        Args:
            x (int): スプライトの初期x座標
            y (int): スプライトの初期y座標
            screen_width (int): スクリーン幅
            screen_height (int): スプリーン高さ
        """
        super(Player, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        surface_tmp = pygame.image.load("image/赤丸.png").convert_alpha()  # キャラ画像の指定
        self.surf = pygame.transform.scale(surface_tmp, (50, 50)).convert_alpha()  # Surfaceオブジェクト: コスチューム
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()  # コスチュームが描かれる長方形オブジェクト
        self.rect.center = (x, y)  # キャラ座標を中心に
        self.speed = 5

    def update(self, pressed_key) -> None:
        """
        スプライトの動きのコントロール
        Args:
            pressed_key: 押したキーのオブジェクト
        """
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, self.speed)

        # スクリーンから出そうになったら止める
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height


class Enemy(pygame.sprite.Sprite):
    """
    敵のスプライト
    """
    def __init__(self, screen_width, screen_height):
        """
        コンストラクタ
        """
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = self.surf.get_rect(
            center=(random.randint(self.screen_width + 20, self.screen_width + 100),
                    random.randint(0, self.screen_height)))
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    main()
