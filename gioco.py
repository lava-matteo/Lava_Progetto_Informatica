from ursina import * 
from ursina.prefabs.first_person_controller import *
from ursina.shaders import lit_with_shadows_shader, transition_shader

class Player(Entity):
    def __init__(self, position, rotation, **kwargs):
        self.controller = FirstPersonController(**kwargs)
        super().__init__(parent = self.controller)

        self.caduto = True

        self.controller.position = position
        self.controller.rotation = rotation

        self.cazzotto = Animation('animations/pugno.gif', scale = (2,1.2,10), filtering = None, autoplay = False, loop = False, parent = camera.ui, position = (0, -0.05))
        
        camera.fov = 115

        self.controller.cursor.texture = 'textures/crosshair'
        self.controller.cursor.color = (100, 100, 100, 1)

        self.jump = Audio('audio\Salto.mp3', loop = False, autoplay = False)
        self.run = Audio('audio\passi.mp3', loop = False, autoplay = False)
        self.walk = Audio('audio\passi_lenti.mp3', loop = False, autoplay = False)
        self.fall = Audio('audio\caduta.mp3', loop = False, autoplay = False)
        self.punch = Audio('audio\pugno.mp3', loop = False, autoplay = False, volume = 0.4)

        self.fists = Entity(parent = self.controller.camera_pivot)
        self.morelli = Entity(parent = self.controller.camera_pivot, scale = 0.15, position = Vec3(0.7, -0.3, 0.8), rotation= Vec3(0, -40, 30), model = 'models_compressed/bottiglia', texture = 'textures/morelli2', shader = transition_shader)
        

        self.oggetti = [self.fists, self.morelli]
        
        self.current_item = 0
        
        self.switch_weapon()
    
    def switch_weapon(self):
        for i,v in enumerate(self.oggetti):
            if i == self.current_item:
                v.visible = True
            else: 
                v.visible = False
    
    def input(self, key):
        try:
            self.current_item = int(key) -1
            self.cazzotto.finish()
            self.switch_weapon()
        except:
            pass
        
        if key == 'escape':
            pause.enabled = True

        if key == 'space':
            if not self.controller.jumping and not self.caduto:
                self.jump.play()

        if (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']) and self.controller.grounded and not held_keys['control'] and not held_keys['c']:
            if held_keys['shift']:
                Audio.stop(self.walk)
                if not self.run.playing:
                    self.run.play()
            elif not self.walk.playing:
                self.walk.play()    
            
        else:
            Audio.stop(self.walk)
            Audio.stop(self.run)
        if key == 'ù':
            exit()

        if key == 'r':
            self.controller.position = (0.6, 75, -28)
            self.controller.rotation = (0, 0, 0)

            satellitare_principale.clicked = False
            wireless_principale.clicked = False
            portone.locked = True

        if held_keys['shift'] and not held_keys['s']:
            self.controller.speed = 17
            if held_keys['w']:
                camera.fov = 120
        elif held_keys['control'] or held_keys['c']:
            self.controller.speed = 4
            self.controller.camera_pivot.y = 1
        else:
            self.controller.speed = 7
            self.controller.camera_pivot.y = 4
            camera.fov = 115

        if key == 'left mouse down':
            if self.current_item == 0:
                self.cazzotto.start()
                self.punch.play()
            
    def update(self):
        if self.controller.position.y < -10:
            self.controller.position = (0.6, 75, -28)
            self.controller.rotation = (0, 0, 0)
        # print(self.controller.position)
        # print(self.controller.rotation)
        
        if self.controller.grounded and self.caduto:
            self.fall.play()
            self.caduto = False
        if not self.controller.grounded:
            self.caduto = True
        
        if title_screen.enabled == True or pause.enabled == True:
            self.controller.enabled = False
            application.paused = True
        else:
            self.controller.enabled = True
            application.paused = False

        if self.controller.position.y > 98:
            self.controller.gravity = 0.4
            self.controller.jump_height = 7
            self.controller.jump_up_duration = 1
        else:
            self.controller.gravity = 2
            self.controller.jump_height = 3
            self.controller.jump_up_duration = .5

app = Ursina()


player = Player(position = (0.6, 75, -28), rotation = (0, 0, 0))

pivot = Entity()
AmbientLight(parent = pivot, y=2, z=3, shadows = True, rotation = (45, -45, 45))
DirectionalLight(parent = pivot, y=2, z=3, shadows = True, rotation = (45, -45, 45))

sky_texture = load_texture("textures/skybox.png")
Sky(texture=sky_texture)

app.run()