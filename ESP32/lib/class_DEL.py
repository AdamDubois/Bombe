import asyncio
import neopixel
import Config

class DEL:
    def __init__(self, pin=Config.LED_STRIP_PIN, led_count=Config.LED_STRIP_COUNT, brightness=0.5):
        self.led_count = led_count
        self.current_animation = None  # Référence à la tâche d'animation en cours
        self.interrupt_flag = False    # Flag pour interrompre l'animation
        self.current_color = (0, 0, 0) # Couleur actuelle

        # objet NeoPixel
        self.pixels = neopixel.NeoPixel(
            pin,
            led_count,
            brightness=brightness,
            auto_write=False,
            pixel_order=neopixel.GRB  # bande WS2812 standard
        )

    def set_all(self, color):
        """Définir la couleur de tous les LEDs (synchrone)"""
        self.current_color = color
        for i in range(self.led_count):
            self.pixels[i] = color
        self.pixels.show()

    def eteindre(self):
        """Éteindre tous les LEDs"""
        self.set_all((0, 0, 0))

    async def interrupt_current_animation(self):
        """Interrompt l'animation en cours"""
        if self.current_animation and not self.current_animation.done():
            self.interrupt_flag = True
            self.current_animation.cancel()
            try:
                await self.current_animation
            except asyncio.CancelledError:
                pass
            print("Animation interrompue")

    async def flash_async(self, color, flash_count=1, wait_ms=200):
        """Flash asynchrone avec possibilité d'interruption"""
        try:
            for i in range(flash_count):
                if self.interrupt_flag:
                    break
                    
                self.set_all(color)
                await asyncio.sleep(wait_ms / 1000)
                
                if self.interrupt_flag:
                    break
                    
                self.eteindre()
                await asyncio.sleep(wait_ms / 1000)
        except asyncio.CancelledError:
            print("Flash interrompu")
            raise

    async def heartbeat_async(self, color, wait_ms=40):
        """Heartbeat asynchrone avec possibilité d'interruption"""
        # Mémoriser la luminosité actuelle
        old_brightness = self.pixels.brightness
        
        try:
            # montée
            for b in range(0, 255, 10):
                if self.interrupt_flag:
                    break
                self.pixels.brightness = b / 255
                self.set_all(color)
                await asyncio.sleep(wait_ms / 1000)

            # descente
            for b in range(255, -1, -10):
                if self.interrupt_flag:
                    break
                self.pixels.brightness = b / 255
                self.set_all(color)
                await asyncio.sleep(wait_ms / 1000)

            # Restaurer la luminosité d'origine
            self.pixels.brightness = old_brightness
            
        except asyncio.CancelledError:
            # Restaurer la luminosité d'origine même en cas d'interruption
            self.pixels.brightness = old_brightness
            print("Heartbeat interrompu")
            raise

    async def JayLeFou_async(self, color=(255, 0, 0)):
        """Animation JayLeFou asynchrone avec possibilité d'interruption"""
        self.interrupt_flag = False
        
        try:
            # 10 battements rapides
            for i in range(10):
                if self.interrupt_flag:
                    print(f"Animation JayLeFou interrompue au battement {i+1}/10")
                    break
                await self.heartbeat_async(color)

            # Gros flash final (seulement si pas interrompu)
            if not self.interrupt_flag:
                await self.flash_async(color, flash_count=2)
                
        except asyncio.CancelledError:
            print("JayLeFou interrompu")
            raise
        finally:
            self.interrupt_flag = False

    async def start_animation(self, color):
        """Démarre une nouvelle animation (interrompt la précédente si nécessaire)"""
        # Interrompre l'animation en cours
        await self.interrupt_current_animation()
        
        # Démarrer la nouvelle animation
        self.current_animation = asyncio.create_task(self.JayLeFou_async(color))
        return self.current_animation
    
    async def rainbow_cycle_async(self, wait_ms=20, iterations=5):
        """Animation Rainbow Cycle asynchrone avec possibilité d'interruption"""
        self.interrupt_flag = False
        
        try:
            for j in range(256 * iterations):
                if self.interrupt_flag:
                    print("Animation Rainbow Cycle interrompue")
                    break
                for i in range(self.led_count):
                    pixel_index = (i * 256 // self.led_count) + j
                    self.pixels[i] = self.wheel(pixel_index & 255)
                self.pixels.show()
                await asyncio.sleep(wait_ms / 1000)
                
        except asyncio.CancelledError:
            print("Rainbow Cycle interrompu")
            raise
        finally:
            self.interrupt_flag = False

    def wheel(self, pos):
        """Génère des couleurs rainbow en fonction de la position (0-255)"""
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    async def start_rainbow_animation(self, wait_ms=20, iterations=5):
        """Démarre une animation rainbow (interrompt la précédente si nécessaire)"""
        # Interrompre l'animation en cours
        await self.interrupt_current_animation()
        
        # Démarrer la nouvelle animation rainbow
        self.current_animation = asyncio.create_task(self.rainbow_cycle_async(wait_ms, iterations))
        return self.current_animation

    def set_solid_color(self, color):
        """Définir une couleur fixe (interrompt toute animation)"""
        if self.current_animation and not self.current_animation.done():
            self.interrupt_flag = True
        self.set_all(color)