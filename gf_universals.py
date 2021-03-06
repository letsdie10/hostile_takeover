import sys
import pygame
import time

from time import process_time

from explosion import Explosion

import gf_sounds as gfsounds



""" This file is sorted in this pattern:
    1) Universal
    2) 
    3) 
"""

""" 1) Universal
		a) Time
		b) Explosions
		c) Ship hit
		d) Remove Upgrades
"""

"""_____________________________________________________________________________
   1a) Universal: Time
_____________________________________________________________________________"""

def get_process_time():
	# Returns the process time at the time of request or call of this method.
	process_time = time.process_time()
	return process_time
	
	
	
	
	
	
	
	
	
	
"""_____________________________________________________________________________
   1b) Universal: Explosions
_____________________________________________________________________________"""

def create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='hostile'):
	"""Gets object death position and create an explosion on the spot."""
	ai_settings.explosion_time_create = ai_settings.time_game_total_play
	#print("Time create: " + str(ai_settings.explosion_time_create))
	if object_type == 'hostile':
		create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y)
	elif object_type == 'ship':
		create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='ship')

def create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='hostile'):
	"""Creates an explosion image to spawn at the specified position and
	adds it into the list(explosions)."""
	if object_type == 'hostile':
		hostile_explosion = Explosion(ai_settings, screen)
		hostile_explosion.centerx = death_x
		hostile_explosion.centery = death_y
		explosions.add(hostile_explosion)
	elif object_type == 'ship':
		create_sound_ship(ai_settings, shipexplode_sounds)
		ship_explosion = Explosion(ai_settings, screen)
		# Changes the explosion image for ship.
		ship_explosion.image = pygame.image.load('images/explosion/ship_explosion1.bmp')
		ship_explosion.centerx = death_x
		ship_explosion.centery = death_y
		explosions.add(ship_explosion)
		
def create_sound_ship(ai_settings, shipexplode_sounds):
	# Plays the Ship Explosion Sound.
	gfsounds.shipexplode_sound_start_internals(ai_settings, shipexplode_sounds)
		
		
def check_time_explosion_disappear(ai_settings, explosions):
	"""Removes the explosion image after a specified time.
	(Time specified in settings.py)"""
	# Extracts the explosion_time_create and adds the explosion_time_disappear
	# from ai_settings.py to it to get the time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The explosion_time_disappear can be optimized to run just once.
	explosion_time_disappear = float('{:.1f}'.format(ai_settings.explosion_time_create + ai_settings.explosion_time_disappear))
	#print("Time New: " + str(explosion_time_new))
	#print("Time Disappear: " + str(explosion_time_disappear))
	#print(explosion_time_new == explosion_time_disappear)
	# If time_new equate time_no_immune, remove explosion image.
	for explosion in explosions.copy():
		if ai_settings.time_game_total_play >= explosion_time_disappear:
			explosions.remove(explosion)
	
	
	
	
	
	
	
	
	
	
"""_____________________________________________________________________________
   1b) Universal: Ship hit
_____________________________________________________________________________"""
	
		
def ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, explosions, stats, sb):
	"""Creates explosion image, Continues if there are still ships left,
	Else, end game."""
	# Runs explosion counter and creates explosion image
	# at death position of object.
	create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, ship.rect.centerx, ship.rect.centery, object_type='ship')
	
	# Stops the railgun sounds.
	if ship.upgrades_allow_railguns and ai_settings.shipbullets_constant_firing:
		gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
		
	# Remove all Ship Upgrades.
	remove_upgrades_all(ai_settings, ship, u_i_rail, u_i_secondary, u_i_missile, u_i_laser)
	
	# If there are still ships left, immunity set to true for immunity counter,
	# ships left decreased by 1, and ship is centered.
	if stats.ship_left > 0:
		ship.immunity = True
		stats.ship_left -= 1
		ship.center_ship()
	# Else, game_active set to False, mouse set to visible again,
	# set_grab set to False
	# High score is dumped to json file so that upon clicking the statistics 
	# button, the statistics will be updated with the new high score that is 
	# newly acquired/achieved.
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		sb.dumps_stats_to_json()
	
	
	
	
	
	
	
	
	
	
"""_____________________________________________________________________________
   1b) Universal: Ship hit
_____________________________________________________________________________"""
		
def remove_upgrades_all(ai_settings, ship, u_i_rail, u_i_secondary, u_i_missile, u_i_laser):
	"""Removes all the upgrades of ships."""
	u_i_rail.empty()
	u_i_secondary.empty()
	u_i_missile.empty()
	u_i_laser.empty()
	
	ai_settings.upgrades_time_railgun_end = ai_settings.time_game_total_play - 1
	ai_settings.upgrades_time_secondary_end = ai_settings.time_game_total_play - 1
	ai_settings.upgrades_time_missile_end = ai_settings.time_game_total_play - 1
	ai_settings.upgrades_time_laser_end = ai_settings.time_game_total_play - 1
	ship.upgrades_allow_railguns = False
	ship.upgrades_allow_bullets = False
	ai_settings.shipbullet_time_fire_interval = 0.3
	ship.upgrades_allow_bullet_secondary_gun = False
	ship.upgrades_allow_missiles = False
	ship.upgrades_allow_missile_secondary_gun = False
	ship.upgrades_allow_lasers = False
	
	ai_settings.upgrades_no_of_current_upgrades = 0
	
	if ai_settings.ship_weapon_default == 1:
		ship.upgrades_allow_bullets = True
		if ai_settings.shipbullets_constant_firing or ai_settings.shipmissiles_constant_firing:
			ai_settings.shipbullets_constant_firing = True
	elif ai_settings.ship_weapon_default == 2:
		ship.upgrades_allow_missiles = True
		if ai_settings.shipbullets_constant_firing or ai_settings.shipmissiles_constant_firing:
			ai_settings.shipmissiles_constant_firing = True
