# Copyright (C) 2018-2021 Eric Kernin, NWNC HARFANG.

import harfang as hg
from master import Main
import vcr
from Missions import *
from SmartCamera import *
from HUD import *
from overlays import *
from MachineDevice import ControlDevice
import Machines

def create_inputs_names(df_device_name, control_device_name, inputs_mapping):
    im = {}
    for k, v in inputs_mapping[df_device_name][control_device_name].items():
        if v != "":
            if "name" in ControlDevice.device_configurations[control_device_name][v]:
                v = ControlDevice.device_configurations[control_device_name][v]["name"]
            elif "_" in v:
                v = v.split("_")[1]
        im[k] = v
    return im

def update_joystick_inputs():
    if ControlDevice.is_joystick_connected():
        imj = create_inputs_names("AircraftUserInputsMapping",ControlDevice.get_current_joystick().GetDeviceName(), Main.aircraft_inputs_mapping_encoded)
        inpt = Main.inputs_commands["commands_dict"]
        inpt["Pitch"]["joystick"] = "" if not "SET_PITCH" in imj else imj["SET_PITCH"]
        inpt["Roll"]["joystick"]= "" if not "SET_ROLL" in imj else imj["SET_ROLL"]
        inpt["Yaw"]["joystick"]= "" if not "SET_YAW" in imj else imj["SET_YAW"]
        inpt["Gun"]["joystick"]= "" if not "FIRE_MACHINE_GUN" in imj else imj["FIRE_MACHINE_GUN"]
        inpt["Missiles"]["joystick"]= "" if not "FIRE_MISSILE" in imj else imj["FIRE_MISSILE"]
        inpt["Target selection"]["joystick"]= "" if not "NEXT_TARGET" in imj else imj["NEXT_TARGET"]
        
        if not "SET_THRUST_LEVEL" in imj and not "INCREASE_THRUST_LEVEL" in imj and not "DECREASE_THRUST_LEVEL" in imj:
            t = ""
        elif "SET_THRUST_LEVEL" in imj:
            t = imj["SET_THRUST_LEVEL"]
        else:
            t = imj["INCREASE_THRUST_LEVEL"] + " / " + imj["DECREASE_THRUST_LEVEL"]
        
        inpt["Thrust level"]["joystick"] = t

        inpt["Brake"]["joystick"]= ("" if not "INCREASE_BRAKE_LEVEL" in imj else (imj["INCREASE_BRAKE_LEVEL"] + " / ")) + ("" if "DECREASE_BRAKE_LEVEL" not in imj else imj["DECREASE_BRAKE_LEVEL"])
        inpt["Flaps"]["joystick"]= ("" if not "INCREASE_FLAPS_LEVEL" in imj else (imj["INCREASE_FLAPS_LEVEL"] + " / ")) + ("" if "DECREASE_FLAPS_LEVEL" not in imj else imj["DECREASE_FLAPS_LEVEL"])
        inpt["Post combustion (only thrust=100%)"]["joystick"]= "" if not "SWITCH_POST_COMBUSTION" in imj else imj["SWITCH_POST_COMBUSTION"]
        inpt["Deploy / Undeploy gear"]["joystick"]= "" if not "SWITCH_GEAR" in imj else imj["SWITCH_GEAR"]

def init_menu_state():
    Main.flag_display_selected_aircraft = False
    Main.flag_running = False
    
    vcr.request_new_state(Main, "disable")
    Main.smart_camera.flag_inertia = True
    
    Main.set_renderless_mode(False)
    Main.flag_network_mode = False
    Main.fading_to_next_state = False
    Main.destroy_sfx()
    ParticlesEngine.reset_engines()
    Destroyable_Machine.reset_machines()
    Main.create_aircraft_carriers(1, 0)
    Missions.setup_carriers(Main.aircraft_carrier_allies, hg.Vec3(0, 0, 0), hg.Vec3(100, 0, 25), 0)
    Main.create_players(["Rafale", "Eurofighter", "Rafale", "Eurofighter", "Rafale", "F16"], [])
    n = len(Main.players_allies)
    Missions.aircrafts_starts_on_carrier(Main.players_allies[0:n // 2], Main.aircraft_carrier_allies[0], hg.Vec3(10, 19.5, 60), 0, hg.Vec3(0, 0, -20))
    Missions.aircrafts_starts_on_carrier(Main.players_allies[n // 2:n], Main.aircraft_carrier_allies[0], hg.Vec3(-10, 19.5, 40), 0, hg.Vec3(0, 0, -20))
    nd = Main.scene.GetNode("aircraft_carrier")

    if Main.intro_anim_id == 1:
        Main.anim_camera_intro_dist = Animation(5, 30, 80, 250)
        Main.anim_camera_intro_rot = Animation(0, 20, 1, 20)
        Main.camera_intro.GetTransform().SetPos(hg.Vec3(0, 50, 90))
        Main.camera_intro.GetTransform().SetRot(hg.Vec3(0, 0, 0))
        Main.smart_camera.follow_distance = Main.anim_camera_intro_dist.v_start
        Main.smart_camera.lateral_rot = Main.anim_camera_intro_rot.v_start
        Main.smart_camera.setup(SmartCamera.TYPE_FOLLOW, Main.camera_intro, nd)
        Main.display_dark_design = True
        Main.display_Logo = True

    elif Main.intro_anim_id == 0:
        pos, rot, fov = hg.Vec3(13.018, 19.664, 49.265), hg.Vec3(-0.310, 4.065, 0.000), 0.271  # Pilotes sunshine
        Main.camera_intro.GetTransform().SetPos(pos)
        Main.camera_intro.GetTransform().SetRot(rot)
        Main.camera_intro.GetCamera().SetFov(fov)
        Main.smart_camera.setup(SmartCamera.TYPE_FPS, Main.camera_intro)
        Main.scene.SetCurrentCamera(Main.camera_intro)
        Main.display_dark_design = True
        Main.display_logo = False

    elif Main.intro_anim_id == 2:

        Main.display_dark_design = True
        Main.display_logo = False

        keyframes = [

            {"order": 0, "name": "Lateral", "duration": 10, "fade_in": 0.5, "fade_out": 0.5,
             "pos_start": hg.Vec3(-89.067, 17.386, -9.640), "pos_end": hg.Vec3(-88.963, 17.386, -13.672),
             "rot_start": hg.Vec3(0.000, 1.545, 0.000), "rot_end": hg.Vec3(0.000, 1.545, 0.000),
             "fov_start": 0.133, "fov_end": 0.133},

            {"order": 1, "name": "Pilotes sunshine", "duration": 10, "fade_in": 0.5, "fade_out": 0.5,
             "pos_start": hg.Vec3(13.145, 19.664, 49.002), "pos_end": hg.Vec3(12.950, 19.664, 49.531),
             "rot_start": hg.Vec3(-0.300, 3.925, 0.000), "rot_end": hg.Vec3(-0.300, 3.925, 0.000),
             "fov_start": 0.271, "fov_end": 0.271},

            {"order": 2, "name": "Carrier mass", "duration": 10, "fade_in": 0.5, "fade_out": 0.5,
             "pos_start": hg.Vec3(196.515, 34.984, 272.780), "pos_end": hg.Vec3(179.877, 28.862, 262.723),
             "rot_start": hg.Vec3(0.055, 3.755, 0.000), "rot_end": hg.Vec3(0.035, 3.755, 0.000),
             "fov_start": 0.120, "fov_end": 0.120},

            {"order": 3, "name": "missiles", "duration": 10, "fade_in": 0.5, "fade_out": 0.5,
             "pos_end": hg.Vec3(-41.906, 19.598, 40.618), "pos_start": hg.Vec3(-41.881, 19.598, 39.685),
             "rot_start": hg.Vec3(0.010, 1.545, 0.000), "rot_end": hg.Vec3(0.010, 1.545, 0.000),
             "fov_start": 0.039, "fov_end": 0.039},

            {"order": 4, "name": "behind carrier", "duration": 10, "fade_in": 0.5, "fade_out": 0.5,
             "pos_start": hg.Vec3(-7.179, 16.457, 832.241), "pos_end": hg.Vec3(-7.179, 40.457, 832.241),
             "rot_start": hg.Vec3(-0.015, 3.130, 0.000), "rot_end": hg.Vec3(0.015, 3.130, 0.000),
             "fov_start": 0.052, "fov_end": 0.048}
        ]
        strt = int(uniform(0, 1000)) % len(keyframes)
        for kf in keyframes:
            kf["order"] = strt
            strt = (strt + 1) % len(keyframes)
        keyframes.sort(key=lambda p: p["order"])

        Main.smart_camera.setup(SmartCamera.TYPE_CINEMATIC, Main.camera_intro)
        Main.scene.SetCurrentCamera(Main.camera_intro)
        Main.smart_camera.set_keyframes(keyframes)

        # pos,rot,fov = hg.Vec3(-93.775, 17.924, 37.808),hg.Vec3(0.015, 1.540, 0.000),0.145 #Lateral
        # pos,rot,fov = hg.Vec3(13.018,19.664,49.265),hg.Vec3(-0.310,4.065,0.000),0.271 # Pilotes sunshine
        # pos, rot, fov = hg.Vec3(196.515, 34.984, 272.780), hg.Vec3(0.055, 3.755, 0.000), 0.120 # Carrier mass
        # pos, rot, fov = hg.Vec3(-28.444, 19.464, 41.583), hg.Vec3(0.010, 1.545, 0.000), 0.039 # missiles
        # pos, rot, fov = hg.Vec3(-7.179, 16.457, 832.241), hg.Vec3(-0.015, 3.130, 0.000), 0.052 # behind carrier

    # Keyboard commands:
    Main.aircraft_inputs_mapping_encoded, _ = ControlDevice.load_inputs_mapping_file(Aircraft.user_inputs_mapping_file, "AircraftUserInputsMapping")
    
    imkb = {}
    for k, v in Main.aircraft_inputs_mapping_encoded["AircraftUserInputsMapping"]["Keyboard"].items():
        if "_" in v:
            v = v.split("_")[1]
        imkb[k] = v

    commands = [
        ["Recenter view", {"keyboard": "F11"}],
        ["Pitch" , {"keyboard": imkb["PITCH_UP"] + " / " + imkb["PITCH_DOWN"]}],
        ["Roll" , {"keyboard": imkb["ROLL_LEFT"] + " / " + imkb["ROLL_RIGHT"]}],
        ["Yaw" , {"keyboard": imkb["YAW_LEFT"] + " / " + imkb["YAW_RIGHT"]}],
        ["Gun" , {"keyboard": imkb["FIRE_MACHINE_GUN"]}],
        ["Missiles" , {"keyboard": imkb["FIRE_MISSILE"]}],
        ["Target selection" , {"keyboard": imkb["NEXT_TARGET"]}],
        ["Thrust level", {"keyboard": imkb["INCREASE_THRUST_LEVEL"] + " / " + imkb["DECREASE_THRUST_LEVEL"]}],
        ["Brake" , {"keyboard": imkb["INCREASE_BRAKE_LEVEL"] + " / " + imkb["DECREASE_BRAKE_LEVEL"]}],
        ["Flaps" , {"keyboard": imkb["INCREASE_FLAPS_LEVEL"] + " / " + imkb["DECREASE_FLAPS_LEVEL"]}],
        ["Post combustion (only thrust=100%)" ,{"keyboard": imkb["SWITCH_POST_COMBUSTION"]}],
        ["Deploy / Undeploy gear",{"keyboard": imkb["SWITCH_GEAR"]}],
        ["Reset game" , {"keyboard": "TAB"}],
        ["Set View" , {"keyboard":"2/3/4/8/6/5/7/9"}],
        ["Zoom" , {"keyboard": "Insert / Page Up"}],
        ["Aircraft selection (multi allies missions)" , {"keyboard": "Numeric pad : 1"}],
        ["Activate IA" , {"keyboard": "I"}],
        ["Activate User control" , {"keyboard": "U"}],
        ["HUD ON / OFF" , {"keyboard":"F10"}]
    ]
    
    Main.inputs_commands = {"display_order": [], "commands_dict": {}}
    for cmd in commands:
        Main.inputs_commands["commands_dict"][cmd[0]] = cmd[1]
        Main.inputs_commands["display_order"].append(cmd[0])
    
    # Joystick commands (if joystick(s) connected)
    update_joystick_inputs()

    Main.scene.SetCurrentCamera(Main.camera_intro)
    Main.t = 0
    Main.fading_cptr = 0
    Main.menu_fading_cptr = 0
    if Main.flag_sfx:
        Main.main_music_state[0].volume = Main.master_sfx_volume
        Main.main_music_state[1].volume = Main.master_sfx_volume
        Main.main_music_source = tools.play_stereo_sound(Main.main_music_ref, Main.main_music_state)

    Main.post_process.setup_fading(3, 1)
    Main.flag_running = True
    vcr.validate_requested_state()
    return menu_state


def menu_state(dts):

    Main.t += dts
    Main.post_process.update_fading(dts)
    if Main.flag_sfx:
        if Main.post_process.fade_running:
            Main.master_sfx_volume = Main.post_process.fade_f
        tools.set_stereo_volume(Main.main_music_source, Main.master_sfx_volume)

    for carrier in Main.aircraft_carrier_allies:
        carrier.update_kinetics(dts)

    if Main.display_dark_design:
        Main.spr_design_menu.set_position(0.5 * Main.resolution.x, 0.5 * Main.resolution.y)
        Main.spr_design_menu.set_color(hg.Color(1, 1, 1, 1))
        Main.sprites_display_list.append(Main.spr_design_menu)

    if Main.display_logo:
        Main.spr_logo.set_position(0.5 * Main.resolution.x, 0.5 * Main.resolution.y)
        Main.sprites_display_list.append(Main.spr_logo)

    # fade in:
    fade_in_delay = 2.
    Main.fading_cptr = min(fade_in_delay, Main.fading_cptr + dts)

    if Main.fading_cptr >= fade_in_delay:
        # Start infos:
        tps = hg.time_to_sec_f(hg.GetClock())
        menu_fade_in_delay = 1
        Main.menu_fading_cptr = min(menu_fade_in_delay, Main.menu_fading_cptr + dts)

        f = Main.menu_fading_cptr / menu_fade_in_delay

        yof7 = -0.1 

        Overlays.add_text2D("MULTI - UAV COOPERATIVE TARGET TRACKING ", hg.Vec2(0.5, 800 / 900 - 0.08), 0.035, hg.Color.White * f, Main.hud_font, hg.DTHA_Center)
        Overlays.add_text2D("110190021 - Huseyin Tutan - ITU FAA - UCK4902", hg.Vec2(0.5, 770 / 900 - 0.08), 0.025, hg.Color.White * f, Main.hud_font, hg.DTHA_Center)

        Missions.display_mission_title(Main, f, dts, yof7)

        Overlays.add_text2D("Choose network mode then run python script.", hg.Vec2(0.5, 611 / 900 + yof7), 0.025, hg.Color(1, 1, 1, (0.7 + sin(tps * 5) * 0.3)) * f, Main.hud_font, hg.DTHA_Center)

        # Number of colmuns for commands display
        n_col = 1
        #if Main.flag_paddle: n_col += 1
        #if Main.flag_generic_controller: n_col += 1
        x_step_cmds = 345 / 1600
        x_step = 200 / 1600
        w = x_step_cmds + n_col * x_step
        x_start = 0.5 - (w/2)

        # s = 0.015
        # x = x_start
        # y = 500 + yof7 * 900
        # c = hg.Color(1., 0.9, 0.3, 1) * f
        # if Main.flag_vr:
        #     Overlays.add_text2D(Main.inputs_commands["display_order"][0], hg.Vec2(x, (y+20) / 900), s, c, Main.hud_font)
        # stp = 0
        # for i in range(1,len(Main.inputs_commands["display_order"])):
        #     Overlays.add_text2D(Main.inputs_commands["display_order"][i], hg.Vec2(x, (y - stp) / 900), s, c, Main.hud_font)
        #     stp += 20
    
        # c2 = hg.Color.Grey * f

        # x += x_step_cmds

        # c = hg.Color.White * f
        
        # Keyboard:
        # if Main.control_mode == ControlDevice.CM_KEYBOARD:
            
        #     #Overlays.add_text2D("Keyboard commands", hg.Vec2(x, (y+60) / 900), s, c2, Main.hud_font)
        #     if Main.flag_vr:
        #         Overlays.add_text2D(Main.inputs_commands["commands_dict"]["Recenter view"]["keyboard"], hg.Vec2(x, (y+20) / 900), s, c, Main.hud_font)
        #     stp = 0
        #     for i in range(1, len(Main.inputs_commands["display_order"])):
        #         command_name = Main.inputs_commands["display_order"][i]
        #         command = Main.inputs_commands["commands_dict"][command_name]
        #         if "keyboard" in command:
        #             pass
                    # Overlays.add_text2D(command["keyboard"], hg.Vec2(x, (y - stp) / 900), s, c, Main.hud_font)
                #stp += 20
       
        # Joystick
        # elif Main.control_mode == ControlDevice.CM_JOYSTICK:
        #     #x += x_step
        #     Overlays.add_text2D("Joystick commands - " + ControlDevice.get_current_joystick().GetDeviceName() + " / " + ControlDevice.get_current_joystick_name(), hg.Vec2(x, (y+60) / 900), s, c2, Main.hud_font)
        #     stp = 0
        #     for i in range(1, len(Main.inputs_commands["display_order"])):
        #         command_name = Main.inputs_commands["display_order"][i]
        #         command = Main.inputs_commands["commands_dict"][command_name]
        #         if "joystick" in command:
        #             if command["joystick"] != "":
        #                 Overlays.add_text2D(command["joystick"],  hg.Vec2(x, (y - stp) / 900), s, c, Main.hud_font)
        #             elif "keyboard" in command:
        #                 Overlays.add_text2D("Keyboard - " + command["keyboard"], hg.Vec2(x, (y - stp) / 900), s, c * 0.8, Main.hud_font)
        #         elif "keyboard" in command:
        #             Overlays.add_text2D("Keyboard - " + command["keyboard"], hg.Vec2(x, (y - stp) / 900), s, c * 0.8, Main.hud_font)
        #         stp += 20

        if vcr.is_init():
            vcr.update(Main, Main.simulation_dt)

        if Main.intro_anim_id == 1:
            Main.anim_camera_intro_dist.update(Main.t)
            Main.anim_camera_intro_rot.update(Main.t)

            Main.smart_camera.follow_distance = Main.anim_camera_intro_dist.v
            Main.smart_camera.lateral_rot = Main.anim_camera_intro_rot.v

    Main.smart_camera.update(Main.camera_intro, dts)

    if not Main.fading_to_next_state:
        
        f_start = False
        f_key = False
        exclude_keys = [hg.K_Escape, hg.K_Left, hg.K_Right]
        for k in range(hg.K_Last):
            if k not in exclude_keys:
                if Main.keyboard.Pressed(k):
                    f_key = True
                    break
        if f_key:
            if Main.control_mode == AircraftUserControlDevice.CM_KEYBOARD:
                f_start = True
                Main.next_state = "main"
            Main.control_mode = AircraftUserControlDevice.CM_KEYBOARD

        elif ControlDevice.is_joystick_connected():
            joystick = ControlDevice.get_joystick_button_pressed()
            if joystick is not None:
                if Main.control_mode == AircraftUserControlDevice.CM_JOYSTICK and ControlDevice.get_current_joystick() == joystick:
                    f_start = True
                    Main.next_state = "main"
                Main.control_mode = AircraftUserControlDevice.CM_JOYSTICK
                ControlDevice.set_current_joystick(joystick)
                update_joystick_inputs()
        
        elif vcr.request_state == "replay":
            Main.control_mode = AircraftUserControlDevice.CM_NONE
            f_start = True
            Main.next_state = "replay"
        
        if f_start:
            Main.post_process.setup_fading(1, -1)
            Main.fading_to_next_state = True
    else:
        if not Main.post_process.fade_running:
            Main.destroy_players()
            if Main.next_state == "replay":
                init_replay_state()
                return replay_state
            else:
                init_main_state()
                return main_state
    return menu_state


# =================================== IN GAME =============================================

def init_main_state():
    Main.flag_display_selected_aircraft = False
    Main.smart_camera.flag_inertia = True
    vcr.request_new_state(Main, "record")
    Main.flag_running = False
    Main.fading_to_next_state = False
    Main.post_process.setup_fading(1, 1)
    #hg.StopAllSources()
    Main.destroy_sfx()
    ParticlesEngine.reset_engines()
    Destroyable_Machine.reset_machines()
    mission = Missions.get_current_mission()

    mission.setup_players(Main)

    n_aircrafts = len(Main.players_allies) + len(Main.players_ennemies)
    n_missile_launchers = len(Main.missile_launchers_allies) + len(Main.missile_launchers_ennemies)
    n_missiles = 0
    for aircraft in Main.players_allies:
        n_missiles += aircraft.get_num_missiles_slots()
    for aircraft in Main.players_ennemies:
        n_missiles += aircraft.get_num_missiles_slots()

    HUD_Radar.setup_plots(Main.resolution, n_aircrafts, n_missiles, mission.allies_carriers + mission.ennemies_carriers, n_missile_launchers)

    # Setup recorder
    vcr.setup_items(Main)

    Main.num_start_frames = 10
    Main.reset_timestamp()
    Main.flag_running = True
    vcr.validate_requested_state()
    return main_state


def main_state(dts):
    
    Main.update_timestamp(dts)
    if not Main.flag_renderless:
        Main.post_process.update_fading(dts)
        if Main.flag_sfx:
            if Main.post_process.fade_running:
                Main.master_sfx_volume = Main.post_process.fade_f

        if Main.flag_control_views:
            Main.control_views(Main.keyboard)

        if Main.flag_display_HUD:
            if Main.user_aircraft is not None:
                if Main.user_aircraft.type == Destroyable_Machine.TYPE_AIRCRAFT:
                    HUD_Aircraft.update(Main, Main.user_aircraft, Main.destroyables_list)
                elif Main.user_aircraft.type == Destroyable_Machine.TYPE_MISSILE_LAUNCHER:
                    HUD_MissileLauncher.update(Main, Main.user_aircraft, Main.destroyables_list)

            if Main.flag_display_selected_aircraft and Main.selected_machine is not None:
                HUD_MissileTarget.display_selected_target(Main, Main.selected_machine)

        if Main.flag_display_landing_trajectories:
            if Main.user_aircraft is not None:
                ia_ctrl = Main.user_aircraft.get_device("IAControlDevice")
                if ia_ctrl is not None:
                    Main.display_landing_trajectory(ia_ctrl.IA_landing_target)
                    Main.display_landing_projection(Main.user_aircraft)
        if Main.flag_display_machines_bounding_boxes:
            for machine in Destroyable_Machine.machines_list:
                if machine.is_activated:
                    if machine.bounding_boxe is not None:
                        matrix = machine.get_parent_node().GetTransform().GetWorld()
                        Overlays.add_line(matrix * machine.bound_front, matrix * (machine.bound_front + hg.Vec3(0, 0, 1)), hg.Color.Blue, hg.Color.Blue)
                        Overlays.add_line(matrix * machine.bound_back, matrix * (machine.bound_back + hg.Vec3(0, 0, -1)), hg.Color.Blue, hg.Color.Blue)
                        Overlays.add_line(matrix * machine.bound_up, matrix * (machine.bound_up + hg.Vec3(0, 1, 0)), hg.Color.Green, hg.Color.Green)
                        Overlays.add_line(matrix * machine.bound_down, matrix * (machine.bound_down + hg.Vec3(0, -1, 0)), hg.Color.Green, hg.Color.Green)
                        Overlays.add_line(matrix * machine.bound_right, matrix * (machine.bound_right + hg.Vec3(1, 0, 0)), hg.Color.Red, hg.Color.Red)
                        Overlays.add_line(matrix * machine.bound_left, matrix * (machine.bound_left + hg.Vec3(-1, 0, 0)), hg.Color.Red, hg.Color.Red)
                        Overlays.display_boxe(machine.get_world_bounding_boxe(), hg.Color.Yellow)
    else:
        if Main.user_aircraft is not None and Main.flag_display_radar_in_renderless:
            HUD_Radar.update(Main, Main.user_aircraft, Main.destroyables_list)

    # Destroyable_Machines physics & movements update
    Main.update_kinetics(dts)

    # Update sfx
    if Main.flag_sfx:
        for sfx in Main.players_sfx: sfx.update_sfx(Main, dts)
        for sfx in Main.missiles_sfx: sfx.update_sfx(Main, dts)


    if vcr.is_init():
        vcr.update(Main, Main.simulation_dt)

    camera_noise_level = 0

    if Main.user_aircraft is not None:

        if Main.user_aircraft.type == Destroyable_Machine.TYPE_AIRCRAFT:
            acc = Main.user_aircraft.get_linear_acceleration()
            camera_noise_level = max(0, Main.user_aircraft.get_linear_speed() * 3.6 / 2500 * 0.1 + pow(min(1, abs(acc / 7)), 2) * 1)
            if Main.user_aircraft.post_combustion:
                camera_noise_level += 0.1

        if Main.player_view_mode == SmartCamera.TYPE_FIX:
            cam = Main.camera_cokpit
        else:
            cam = Main.camera

        if Main.keyboard.Pressed(hg.K_Y):
            flag = Main.user_aircraft.get_custom_physics_mode()
            Main.user_aircraft.set_custom_physics_mode(not flag)

    else:
        cam = Main.camera_fps

    if Main.satellite_view:
        cam = Main.satellite_camera

    Main.smart_camera.update(cam, dts, camera_noise_level)

    mission = Missions.get_current_mission()

    if Main.keyboard.Pressed(hg.K_L):
        Destroyable_Machine.flag_update_particles = not Destroyable_Machine.flag_update_particles

    if Main.keyboard.Pressed(hg.K_R):
        Main.set_renderless_mode(not Main.flag_renderless)

    if Main.keyboard.Pressed(hg.K_Tab):
        Main.set_renderless_mode(False)
        mission.aborted = True
        init_end_state()
        return end_state
    elif mission.end_test(Main):
        init_end_state()
        return end_state
    elif vcr.request_state == "replay":
        Main.destroy_players()
        init_replay_state()
        return replay_state

    return main_state


# =================================== REPLAY MODE =============================================

def init_replay_state():
    Main.flag_display_selected_aircraft = False
    Main.smart_camera.flag_inertia = False
    Main.set_renderless_mode(False)
    Main.flag_running = False
    Main.fading_to_next_state = False
    Main.post_process.setup_fading(1, 1)
    Main.destroy_sfx()
    ParticlesEngine.reset_engines()
    Destroyable_Machine.reset_machines()
    
    Main.flag_network_mode = False
    
    fps_start_matrix = hg.TranslationMat4(hg.Vec3(0, 20, 0))
    Main.camera_fps.GetTransform().SetWorld(fps_start_matrix)

    Main.user_aircraft = None
    Main.setup_views_carousel(True)
    Main.set_view_carousel("fps")

    Main.reset_timestamp()
    Main.flag_running = True
    vcr.validate_requested_state()


def replay_state(dts):

    Main.post_process.update_fading(dts)
    
    if Main.flag_control_views:
            Main.control_views(Main.keyboard)
    
    if Main.flag_display_HUD:
        if Main.user_aircraft is not None:
            if Main.user_aircraft.type == Destroyable_Machine.TYPE_AIRCRAFT:
                HUD_Aircraft.update(Main, Main.user_aircraft, Main.destroyables_list)
            elif Main.user_aircraft.type == Destroyable_Machine.TYPE_MISSILE_LAUNCHER:
                HUD_MissileLauncher.update(Main, Main.user_aircraft, Main.destroyables_list)

    if Main.flag_display_selected_aircraft and Main.selected_machine is not None:
        HUD_MissileTarget.display_selected_target(Main, Main.selected_machine)
    
    if Main.flag_display_machines_bounding_boxes:
        for machine in Destroyable_Machine.machines_list:
            if machine.is_activated:
                if machine.bounding_boxe is not None:
                    matrix = machine.get_parent_node().GetTransform().GetWorld()
                    Overlays.add_line(matrix * machine.bound_front, matrix * (machine.bound_front + hg.Vec3(0, 0, 1)), hg.Color.Blue, hg.Color.Blue)
                    Overlays.add_line(matrix * machine.bound_back, matrix * (machine.bound_back + hg.Vec3(0, 0, -1)), hg.Color.Blue, hg.Color.Blue)
                    Overlays.add_line(matrix * machine.bound_up, matrix * (machine.bound_up + hg.Vec3(0, 1, 0)), hg.Color.Green, hg.Color.Green)
                    Overlays.add_line(matrix * machine.bound_down, matrix * (machine.bound_down + hg.Vec3(0, -1, 0)), hg.Color.Green, hg.Color.Green)
                    Overlays.add_line(matrix * machine.bound_right, matrix * (machine.bound_right + hg.Vec3(1, 0, 0)), hg.Color.Red, hg.Color.Red)
                    Overlays.add_line(matrix * machine.bound_left, matrix * (machine.bound_left + hg.Vec3(-1, 0, 0)), hg.Color.Red, hg.Color.Red)
                    Overlays.display_boxe(machine.get_world_bounding_boxe(), hg.Color.Yellow)

    if vcr.is_init():
        vcr.update(Main, Main.simulation_dt)

    camera_noise_level = 0
    if Main.user_aircraft is not None:

        #if Main.user_aircraft.type == Destroyable_Machine.TYPE_AIRCRAFT:
        #    acc = Main.user_aircraft.get_linear_acceleration()
        #    camera_noise_level = max(0, Main.user_aircraft.get_linear_speed() * 3.6 / 2500 * 0.1 + pow(min(1, abs(acc / 7)), 2) * 1)
        #    if Main.user_aircraft.post_combustion:
        #        camera_noise_level += 0.1

        if Main.player_view_mode == SmartCamera.TYPE_FIX:
            cam = Main.camera_cokpit
        else:
            cam = Main.camera

    else:
        cam = Main.camera_fps

    if Main.satellite_view:
        cam = Main.satellite_camera
   
    Main.smart_camera.update(cam, dts, camera_noise_level)


    if not Main.fading_to_next_state:
        
        if Main.keyboard.Pressed(hg.K_Tab) or vcr.request_state == "disable":
            vcr.request_new_state(Main, "disable")
            Main.post_process.setup_fading(1, -1)
            Main.fading_to_next_state = True
    else:
        Main.post_process.update_fading(dts)
        if Main.flag_sfx:
            Main.master_sfx_volume = Main.post_process.fade_f
        if not Main.post_process.fade_running:
            Main.destroy_players()
            init_menu_state()
            return menu_state

    return replay_state

# =================================== END GAME =============================================

def init_end_state():
    Main.flag_display_selected_aircraft = False
    Main.smart_camera.flag_inertia = True
    Main.set_renderless_mode(False)
    Main.flag_running = False
    Main.deactivate_cockpit_view()
    Main.satellite_view = False
    Main.end_state_timer = 20

    if Main.user_aircraft is not None:

        uctrl = Main.user_aircraft.get_device("UserControlDevice")
        if uctrl is not None:
            uctrl.deactivate()

        ia = Main.user_aircraft.get_device("IAControlDevice")
        if ia is not None:
            ia.activate()

        Main.user_aircraft = None

    mission = Missions.get_current_mission()

    aircraft = None
    if mission.failed:
        for player in Main.players_ennemies:
            if not player.wreck:
                aircraft = player
                break
        if aircraft is None:
            aircraft = Main.players_allies[0]
    else:
        for player in Main.players_allies:
            if not player.wreck:
                aircraft = player
                break
        if aircraft is None:
            aircraft = Main.players_allies[0]

    Main.end_state_following_aircraft = aircraft
    Main.smart_camera.setup(SmartCamera.TYPE_FOLLOW, Main.camera, aircraft.get_parent_node())
    Main.scene.SetCurrentCamera(Main.camera)
    Main.flag_running = True
    return end_state


def end_state(dts):
    
    Main.update_kinetics(dts)

    if Main.flag_sfx:
        for sfx in Main.players_sfx: sfx.update_sfx(Main, dts)
        for sfx in Main.missiles_sfx: sfx.update_sfx(Main, dts)

    if Main.flag_display_selected_aircraft and Main.selected_machine is not None:
        HUD_MissileTarget.display_selected_target(Main, Main.selected_machine)

    mission = Missions.get_current_mission()
    mission.update_end_phase(Main, dts)

    if vcr.is_init():
        vcr.update(Main, Main.simulation_dt)

    Main.smart_camera.update(Main.camera, dts)
    
    if not Main.fading_to_next_state:
        if Main.end_state_following_aircraft.flag_destroyed or Main.end_state_following_aircraft.wreck:
            Main.end_state_timer -= dts
        
        if Main.keyboard.Pressed(hg.K_Tab) or Main.end_state_timer < 0 or Main.end_state_following_aircraft.flag_landed:
            Main.post_process.setup_fading(1, -1)
            Main.fading_to_next_state = True
            Main.next_state = "menu"
        elif vcr.request_state == "replay":
            Main.post_process.setup_fading(1, -1)
            Main.fading_to_next_state = True
            Main.next_state = "replay"
    else:
        Main.post_process.update_fading(dts)
        if Main.flag_sfx:
            Main.master_sfx_volume = Main.post_process.fade_f
        if not Main.post_process.fade_running:
            if Main.next_state == "replay":
                Main.destroy_players()
                init_replay_state()
                return replay_state
            else:
                mission.reset()
                Main.destroy_players()
                init_menu_state()
                return menu_state
    return end_state
