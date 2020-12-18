from disrank import generator
from PIL import Image, ImageDraw, ImageFont, ImageChops
from io import BytesIO
import sys
sys.version


disrank = generator.Generator()

args = {
			'bg_image' : '', # Background image link (Optional)
			'profile_image' : 'https://images-ext-1.discordapp.net/external/Vn2YDNmin4oNdyO91g9N1ss5i_VyZoCwP1YyesAlEkA/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/98802238364876800/a8730866ce43c5e5988064977b4c1849.png', # User profile picture link
			'level' : 1, # User current level 
			'current_xp' : 10, # Current level minimum xp 
			'user_xp' : 50, # User current xp
			'next_xp' : 155, # xp required for next level
			'user_position' : 1, # User position in leaderboard
			'user_name' : "DiabeticTurtlepip#1604", # user name with descriminator 
			'user_status' : "online", # User status eg. online, offline, idle, streaming, dnd
		}

image = disrank.generate_profile(**args)

byte_io = BytesIO()

with open("test.png", "wb") as f:
    f.write(image.read())

print("Succesful") 