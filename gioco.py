from ursina import * 
from ursina.prefabs.first_person_controller import *
from ursina.shaders import lit_with_shadows_shader, transition_shader

class Menu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)

        self.ignore_paused = True

        self.mappa_sistemi = Button(text = 'Comunicazione wireless e satellitare', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.8, 0.1), position = (0, 0.15), parent = self)
        self.mappa_tps = Button(text = 'Immagini e tabelle', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.8, 0.1), position = (0, 0), parent = self)
        self.esci = Button(text = 'Esci', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.8, 0.1), position = (0, -0.15), parent = self)

        self.mappa_sistemi.on_click = self.sistemi_premuto
        self.mappa_tps.on_click = self.tps_premuto
        self.esci.on_click = self.esci_premuto

        self.enabled = True

    def sistemi_premuto(self):
        self.enabled = False
        
        porte = [porta_principale, porta_principale_wireless, porta_principale_satellitare, porta_wireless_1, porta_wireless_2, portone]
        for i in porte:
            i.enabled = True
            i.porta.enabled = True
        
        satellitare_principale.clicked = False
        wireless_principale.clicked = False
        portone.locked = True

        application.paused = False

    def esci_premuto(self):
        exit()

    def tps_premuto(self):
        pass
        

class Pausa(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)

        self.ignore_paused = True
        self.enabled = False

        self.continua = Button(text = 'Continua', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.4, 0.1), position = (0, 0.15), parent = self)
        self.riavvia = Button(text = 'Riavvia', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.4, 0.1), position = (0, 0), parent = self)
        self.torna_al_menu = Button(text = 'Torna al menu', color = (25, 25, 25), pressed_color = (255, 255, 255, 255), scale = (0.4, 0.1), position = (0, -0.15), parent = self)

        self.continua.on_click = self.resume
        self.riavvia.on_click = self.restart
        self.torna_al_menu.on_click = self.main_menu

    def resume(self):
        self.enabled = False
        application.paused = False

    def restart(self):
        self.enabled = False
        player.controller.position = (0.6, 75, -28)
        player.controller.rotation = (0, 0, 0)

        satellitare_principale.clicked = False
        wireless_principale.clicked = False
        portone.locked = True
        
        porte = [porta_principale, porta_principale_wireless, porta_principale_satellitare, porta_wireless_1, porta_wireless_2, portone]
        for i in porte:
            i.enabled = True
            i.porta.enabled = True
        
        application.paused = False

    def main_menu(self):
        self.enabled = False
        player.controller.position = (0.6, 75, -28)
        player.controller.rotation = (0, 0, 0)
        title_screen.enabled = True
        
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

class porta(Entity):
    def __init__(self, name, model, scale, color, texture, collider, position, rotation, locked, **kwargs):        
        super().__init__(**kwargs)
        
        self.name = name
        self.model = model
        self.color = color
        self.scale = scale
        self.collider = collider
        self.position = position
        self.rotation = rotation
        self.texture = texture
        self.locked = locked

        self.door = Audio('audio/door.mp3', loop = False, autoplay = False, volume = 0.3)

        self.visible = True

        self.porta = Entity(name = self.name, model = self.model, color = self.color, texture = self.texture, scale = self.scale, collider = self.collider, position = self.position, rotation = self.rotation)
    
    def punched(self):
        self.door.play()
        self.porta.enabled = False
        self.enabled = False

    def punch(self):
        hit_info = raycast(camera.world_position, camera.forward, distance=3)
        if hit_info.hit and hit_info.entity.name == self.name:
            self.punched()
    def input(self, key):
        if key == 'left mouse down' and not self.locked:
            invoke(self.punch, delay = 0.3)

    def update(self):
        if self.locked or self.name != "portone":
            self.porta.texture = self.texture
        else:
            self.porta.texture = "portone_aperto"

app = Ursina()

window.title = 'spatial ma più meglio assai'
window.fullscreen = True
window.exit_button.visible = False
window.fps_counter.enabled = False

title_screen = Menu(parent = camera.ui)

mappa = Entity(model = 'models_compressed/mappa_definitiva1', scale = 20, texture = 'textures/texture_mappa', collider = 'mesh', position = (0, 0, 0), shader = lit_with_shadows_shader) 
tappo_sopra = Entity(model = 'cube', scale = Vec3(30, 0.1, 30), color = (0, 0, 0, 255), collider = 'mesh', position = (0, 84.4487, -21), shader = lit_with_shadows_shader) 

wireless = Entity(model = 'models_compressed/stanza wireless', scale = 20, texture = 'textures/wireless', collider = 'mesh', position = (-40, 0, 0), shader = lit_with_shadows_shader) 
satellitare = Entity(model = 'models_compressed/stanza satellitare', scale = 6, texture = 'textures/mappa_satellite', collider = 'mesh', position = (0, 100, 0), shader = lit_with_shadows_shader) 



porta_principale = porta(name = 'porta_principale', model = 'cube', scale = Vec3(3.4,8,0.5), color = (255, 255, 255, 255), texture = 'textures/porta', collider = 'box', position = (0.65, 4, -17.5), rotation = (0, 0, 0), locked = False)
porta_principale_wireless = porta(name = 'porta_principale_wireless', model = 'cube', scale = Vec3(3.38,7.8,0.5), color = (255, 255, 255, 255), texture = 'textures/porta', collider = 'box', position = (-13.93, 4, -6.55), rotation = (0, -90, 0), locked = False)
porta_principale_satellitare = porta(name = 'porta_principale_satellitare', model = 'cube', scale = Vec3(3.38,7.8,0.5), color = (255, 255, 255, 255), texture = 'textures/porta', collider = 'box', position = (15.1, 4, -6.6), rotation = (0, 90, 0), locked = False)
porta_wireless_1 = porta(name = 'porta_wireless_1', model = 'cube', scale = Vec3(2.9,7,0.5), color = (255, 255, 255, 255), texture = 'textures/porta', collider = 'box', position = (-39.74, 3.5, -19.22), rotation = (0, -90, 0), locked = False)
porta_wireless_2 = porta(name = 'porta_wireless_2', model = 'cube', scale = Vec3(2.9,7,0.5), color = (255, 255, 255, 255), texture = 'textures/porta', collider = 'box', position = (-44.25, 3.5, -4.76), rotation = (0, 0, 0), locked = False)
portone = porta(name = 'portone', model = 'cube', scale = Vec3(10.4,15,1), color = (255, 255, 255, 255), texture = 'textures/portone_chiuso', collider = 'box', position = (0.74, 7.5, 1.54), rotation = (0, 0, 0), locked = True)



player = Player(position = (0.6, 75, -28), rotation = (0, 0, 0))

pivot = Entity()
AmbientLight(parent = pivot, y=2, z=3, shadows = True, rotation = (45, -45, 45))
DirectionalLight(parent = pivot, y=2, z=3, shadows = True, rotation = (45, -45, 45))

sky_texture = load_texture("textures/skybox.png")
Sky(texture=sky_texture)

app.run()