from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import math
import os

class Generator:
    def __init__(self):
        self.default_bg = os.path.join(os.path.dirname(__file__), 'assets', 'card.png')
        self.online     = os.path.join(os.path.dirname(__file__), 'assets', 'online.png')
        self.offline    = os.path.join(os.path.dirname(__file__), 'assets', 'offline.png')
        self.idle       = os.path.join(os.path.dirname(__file__), 'assets', 'idle.png')
        self.dnd        = os.path.join(os.path.dirname(__file__), 'assets', 'dnd.png')
        self.streaming  = os.path.join(os.path.dirname(__file__), 'assets', 'streaming.png')
        self.font1      = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')
        self.font2      = os.path.join(os.path.dirname(__file__), 'assets', 'font2.ttf')
        self.UbuntuB    = os.path.join(os.path.dirname(__file__), 'assets', 'Ubuntu-Medium.ttf')
        self.UbuntuR    = os.path.join(os.path.dirname(__file__), 'assets', 'Ubuntu-Regular.ttf')
        
        
    def generate_profile(self, bg_image:str=None, profile_image:str=None, level:int=1, current_xp:int=0, user_xp:int=20, next_xp:int=100, user_position:int=1, user_name:str='Shahriyar#9770', user_status:str='online'):
        if not bg_image:
            card = Image.open(self.default_bg).convert("RGBA")
        else:
            bg_bytes = BytesIO(requests.get(bg_image).content)
            card = Image.open(bg_bytes).convert("RGBA")

            width, height = card.size
            if width == 900 and height == 238:
                pass
            else:
                x1 = 0
                y1 = 0
                x2 = width
                nh = math.ceil(width * 0.264444)
                y2 = 0

                if nh < height:
                    y1 = (height / 2) - 119
                    y2 = nh + y1

                card = card.crop((x1, y1, x2, y2)).resize((900, 238))

        profile_bytes = BytesIO(requests.get(profile_image).content)
        profile = Image.open(profile_bytes)
        profile = profile.convert('RGBA').resize((200, 200))

        if user_status == 'online':
            status = Image.open(self.online)
        if user_status == 'offline':
            status = Image.open(self.offline)
        if user_status == 'idle':
            status = Image.open(self.idle)
        if user_status == 'streaming':
            status = Image.open(self.streaming)
        if user_status == 'dnd':
            status = Image.open(self.dnd)

        status = status.convert("RGBA").resize((40,40))

        profile_pic_holder = Image.new(
            "RGBA", card.size, (155, 155, 155)
        )  # Is used for a blank image so that i can mask

        # Mask to crop image
        mask = Image.new("RGBA", card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            [(67, 40), (213.5, 189)], fill=(255, 25, 255, 255)
        )  # The part need to be cropped

        # Editing stuff here

        # ======== Fonts to use =============
        font_normal = ImageFont.truetype(self.UbuntuR, 40)
        font_med = ImageFont.truetype(self.UbuntuR, 30)
        font_large = ImageFont.truetype(self.UbuntuB, 42)
        font_small = ImageFont.truetype(self.UbuntuB, 22)
        font_signa = ImageFont.truetype(self.font2, 25)

        # ======== Colors ========================
        WHITE = (242, 242, 242)
        DARK = (110, 151, 241)
        YELLOW = (255, 234, 167)

        def get_str(xp):
            if xp < 1000:
                return str(xp)
            if xp >= 1000 and xp < 1000000:
                return str(round(xp / 1000, 1)) + "k"
            if xp > 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(card)
        draw.text((290, 79), "Server", WHITE, font=font_med)
        draw.text((299, 109), "Rank", WHITE, font=font_med)
        draw.text((441, 79), "Weekly", WHITE, font=font_med)
        draw.text((455, 109), "Rank", WHITE, font=font_med)
        draw.text((455, 154), "WIP", YELLOW, font=font_normal)
        draw.text((780, 200), f"Exp {get_str(user_xp)}/{get_str(next_xp)}", WHITE, font=font_small)
        draw.text((259, 15), user_name, WHITE, font=font_large)
        draw.text((274, 155), f"#{user_position}", DARK, font=font_normal)
        draw.text((610, 83), f"Level", WHITE, font=font_med)
        draw.text((610, 154), f"{level}", WHITE, font=font_normal)
        
                
        # Adding another blank layer for the progress bar
        # Because drawing on card dont make their background transparent
        blank = Image.new("RGBA", card.size, (255, 255, 255, 0))
        blank_draw = ImageDraw.Draw(blank)
        blank_draw.rectangle(
            (0, 250, 900, 230), fill=(7, 7, 7)
        )

        xpneed = next_xp - current_xp
        xphave = user_xp - current_xp

        current_percentage = (xphave / xpneed) * 100
        length_of_bar = (current_percentage * 5*2)+50+20 
        
        blank_draw.rectangle((-1, 230, length_of_bar, 900), fill=DARK)
        
        #blank_draw.ellipse((20, 20, 218, 218), fill=(255, 255, 255, 0), outline=DARK)

        profile_pic_holder.paste(profile, (29, 29, 229, 229))
        

        pre = Image.composite(profile_pic_holder, card, mask)
        pre = Image.alpha_composite(pre, blank)

        # Status badge
        # Another blank
        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))
        #blank.paste(status, (169, 169))
        blank.paste(status, (184, 159))

        final = Image.alpha_composite(pre, blank)
        final_bytes = BytesIO()
        final.save(final_bytes, 'png')
        final_bytes.seek(0)
        return final_bytes