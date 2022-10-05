import pygame
import data

pygame.init()



class StaticPicture(pygame.sprite.Sprite) :

    def __init__(self, image:str|pygame.Surface, size:tuple[int,int]|None, **kwargs) :
        super().__init__()

        if isinstance(image, str) :
            self.image = pygame.image.load(image).convert_alpha()
        elif isinstance(image, pygame.Surface) :
            self.image = image
        if size is not None :
            pygame.transform.scale(self.image, size)

        self._size = size 
        self._kwargs = kwargs
        self.rect = self.image.get_rect(**kwargs)

    
    def modify(self, image:str|pygame.Surface = None, size:tuple[int,int] = None, **kwargs):
        newPath = image or self.image
        newSize = size or self._size
        newKwargs = kwargs or self._kwargs
        
        self.__init__(newPath, newSize, newKwargs)
        



class Text(pygame.sprite.Sprite) :

    def __init__(self, text:str, font:pygame.font.Font, color:str | tuple[int,int,int], bgColor:str|tuple[int,int,int]|None, **kwargs):
        super().__init__()

        text_surf = font.render(text, False, color)
        if bgColor != None :
            backGround = pygame.Surface((int(text_surf.get_width() * 1.1), int(text_surf.get_height() * 1.1)))
            backGround.fill(bgColor)
            backGround.blit(text_surf, text_surf.get_rect(center = (backGround.get_width() // 2, backGround.get_height() // 2)))
            self.image = backGround
        else :
            self.image = text_surf

        self.rect = self.image.get_rect(**kwargs)
        self._font = font
        self._text = text 
        self._color = color 
        self._bgColor = bgColor
        self._kwargs = kwargs
    

    def modify(self, text:str = None, font:pygame.font.Font = None, color:str|tuple[int,int,int] = None, bgColor:str|tuple[int,int,int]|None = None, **kwargs) :
        newText = text or self._text
        newFont = font or self._font
        newColor = color or self._color
        newBgColor = bgColor or self._bgColor
        newKwargs = kwargs or self._kwargs

        self.__init__(newText, newFont, newColor, newBgColor, **newKwargs)



class ScoreText(Text) :

    def update(self) :
        self.modify(str(data.score))
        




class Player(pygame.sprite.Sprite) :

    def __init__(self, path:str, ground:int, size:tuple[int,int]) :
        super().__init__()
        self._ground = ground
        self.image = pygame.transform.scale(pygame.image.load(path), size).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (50, ground))
        self._moveStep = (0,0)
        self.jump_sound = pygame.mixer.Sound("./jump_sound.mp3")
        self.jump_sound.set_volume(0.5)
    

    def player_input(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self._ground :
            self._moveStep = (self._moveStep[0], self._moveStep[1] - 20)
            self.jump_sound.play()

    

    def move(self) :
        self.rect = self.rect.move(self._moveStep)
        if self.rect.bottom > self._ground :
            self.rect.bottom = self._ground
        elif self.rect.bottom < self._ground :
            self._moveStep = (self._moveStep[0], self._moveStep[1] + 1)
    
    
    def update(self) :
        self.player_input()
        self.move()

    
    def reset(self) :
        self._moveStep = (0,0)
        self.rect.bottom = self._ground




class Enemy(pygame.sprite.Sprite) :

    def __init__(self, path:str, height:int, speed:int, size:tuple[int,int]) :
        super().__init__()
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(path).convert_alpha(), size), True, False)
        self.rect = self.image.get_rect(midbottom = (pygame.display.get_window_size()[0] + self.image.get_width(), height))
        self._moveStep = (-speed, 0)
    

    def move(self) :
        self.rect = self.rect.move(self._moveStep)
    

    def update(self) :
        self.move()
        self.destroy()

    
    def destroy(self) :
        if self.rect.right <= 0 :
            self.kill()




class Button(pygame.sprite.Sprite) :

    def __init__(
        self, 
        text:str = "Botton", 
        font:pygame.font.Font = pygame.font.Font(None,30), 
        textColor:str|tuple[int,int,int] = "white",
        backgroundColor:str|tuple[int,int,int]|None = "black",
        **kwargs
        ) :

        self._text = font.render(text, False, textColor)
        self.image = pygame.Surface((int(self._text.get_width() * 1.1), int(self._text.get_height() * 1.1)))
        self.image.fill(backgroundColor)
        self.image.blit(self._text, self._text.get_rect(center = (self.image.get_width() // 2, self.image.get_height() // 2)))
        self.rect = self.image.get_rect(**kwargs)



    def isClicked(self) -> bool :

        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        if pressed[0] and self.rect.collidepoint(pos) :
            return True 
        
        return False

    
    def draw(self, target:pygame.Surface) :
        target.blit(self.image, self.rect)