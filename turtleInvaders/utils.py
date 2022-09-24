# utils.py
# Keep reusable methods for the asteriods game.


from pygame.image import load


def load_sprite(name, with_alpha=True):
	path = f"assets/sprites/{name}.png"
	loaded_sprite = load(path)

	if with_alpha:
		return loaded_sprite.convert_alpha()
	return loaded_sprite.convert()