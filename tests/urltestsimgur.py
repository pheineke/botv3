import requests
import os
import time
import datetime
import string
import random
import argparse
import io
from PIL import Image

NAME_CHARACTERS_POOL = string.ascii_letters + string.digits
URL = 'https://i.imgur.com/'
MIN_NAME_LENGTH = 5
MAX_NAME_LENGTH = 7
MIN_WIDTH = 10
MIN_HEIGHT = 2000


def random_string(length):
    return ''.join(random.choice(NAME_CHARACTERS_POOL) for i in range(length))

def fetch_image(name):
	image = requests.get(URL + name + '.png', allow_redirects=False)

	if image.status_code == 400:
		print(name + ' returned bad request, skipping...')
	elif image.status_code == 404 or image.status_code == 302:
		print(name + ' doesn\'t exists or removed, skipping...')
	elif image.status_code == 200:
		image_content = image.content
		pil_image = Image.open(io.BytesIO(image_content))

		if pil_image.width < MIN_WIDTH:
			print(name + ' width less than minimum, skipping...')
			return False

		if pil_image.height < MIN_HEIGHT:
			print(name + ' height less than minimum, skipping...')
			return False

		print(URL)

		

		return True

	return False

i = 0
while(i < 50):
	image_name_length = random.randint(40, 2000)
	random_image_name = random_string(image_name_length)

	if fetch_image(random_image_name):
		i = i + 1