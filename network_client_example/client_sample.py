
# Written by @HuseyinTutan 2024

import dogfight_client as df
import time


t = 0
t0 = 0
t1 = 0

def print_fps():
	global t, t0, t1
	t1 = time.time()
	dt = t1 - t0
	t0 = t1
	if dt > 0:
		print(str(1 / dt))

df.connect("192.168.56.1", 50888)

time.sleep(2)

planes = df.get_planes_list()
print(str(planes))

df.disable_log()
df.activate_IA(planes[0])

df.activate_IA(planes[2])
df.activate_IA(planes[1])
plane_id = planes[3]

df.reset_machine(plane_id)
df.set_plane_thrust(plane_id, 1)
df.set_client_update_mode(True)


while t < 1:
	plane_state = df.get_plane_state(plane_id)

	df.update_scene()

	t = plane_state["thrust_level"]


df.activate_post_combustion(plane_id)
df.set_plane_pitch(plane_id, -0.5)

p = 0
while p < 15:

	time.sleep(1/200)
	plane_state = df.get_plane_state(plane_id)
	df.update_scene()
	p = plane_state["pitch_attitude"]

df.stabilize_plane(plane_id)

df.retract_gear(plane_id)

s = 0
while s < 500 / 3.6: 
	plane_state = df.get_plane_state(plane_id)
	df.update_scene()
	next_physics = df.compute_next_timestep_physics(plane_id, 1/60)
	print(str(next_physics))
	s = plane_state["linear_speed"]

df.deactivate_post_combustion(plane_id)

# df.set_renderless_mode(True)

# f = False
# while not f:
# 	f = df.get_running()["running"]

# print("RenderLess running")

# Wait until plane altitude >= 5000 m
a = 0

while a < 500:
	print_fps()
	# df.display_2DText([0.25, 0.75], "Plane speed: " + str(plane_state["linear_speed"]), 0.04, [1, 0.5, 0, 1])
	df.update_scene()
	plane_state = df.get_plane_state(plane_id)
	a = plane_state["altitude"]

# When cruising speed & altitude are OK, setups and starts the autopilot
df.set_plane_autopilot_altitude(plane_id, 800)
df.set_plane_autopilot_heading(plane_id, 360-0)
df.set_plane_autopilot_speed(plane_id, 250 )
df.activate_autopilot(plane_id)

# df.set_renderless_mode(False)

# Wait while Renderless mode setting up
# f = False
# while not f:
# 	f = df.get_running()["running"]
df.activate_IA(planes[0])
df.activate_IA(planes[2])
df.activate_IA(planes[1])

# Client update mode OFF
df.set_client_update_mode(False)

# Disconnect from the Dogfight server

#df.disconnect()


