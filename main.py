# -*- coding: utf-8 -*-
from __future__ import annotations

import pygame
from pygame.locals import *


def main():
    pygame.init()  # 初期化
    screen_width = 1306
    screen_height = 653
    pygame.display.set_mode((screen_width, screen_height), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption("Pygame Test")  # ウィンドウタイトル
    background = pygame.image.load("image/sakaiura.JPG").convert_alpha()  # 背景画像の指定
    rectangle_background = background.get_rect()  # 画像を含む長方形オブジェクト
    player = Player(screen_width / 2, screen_height / 2, screen_width, screen_height)

    running: bool = True
    while running:
        pressed_key = pygame.key.get_pressed()
        player.update(pressed_key)
        screen.fill((0, 0, 0, 0))  # 背景色の指定。RGBのはず
        screen.blit(background, rectangle_background)  # 背景画像の描画
        pygame.time.wait(10)  # 更新間隔。多分ミリ秒
        screen.blit(player.surface, player.rectangle)  # キャラの描画
        pygame.display.flip()  # 画面を更新

        for event in pygame.event.get():  # 終了処理
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

    pygame.quit()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super(Player, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        surface_tmp = pygame.image.load("image/赤丸.png").convert_alpha()  # キャラ画像の指定
        self.surface = pygame.transform.scale(surface_tmp, (50, 50)).convert_alpha()  # Surfaceオブジェクト: コスチューム
        self.rectangle = self.surface.get_rect()  # コスチュームが描かれる長方形オブジェクト
        self.rectangle.center = (x, y)  # キャラ座標を中心に

    def update(self, pressed_key):
        if pressed_key[K_LEFT]:
            self.rectangle.move_ip(-3, 0)
        if pressed_key[K_RIGHT]:
            self.rectangle.move_ip(3, 0)
        if pressed_key[K_UP]:
            self.rectangle.move_ip(0, -3)
        if pressed_key[K_DOWN]:
            self.rectangle.move_ip(0, 3)

        # スクリーンから出そうになったら止める
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > self.screen_width:
            self.rectangle.right = self.screen_width
        if self.rectangle.top <= 0:
            self.rectangle.top = 0
        if self.rectangle.bottom >= self.screen_height:
            self.rectangle.bottom = self.screen_height


if __name__ == "__main__":
    main()
