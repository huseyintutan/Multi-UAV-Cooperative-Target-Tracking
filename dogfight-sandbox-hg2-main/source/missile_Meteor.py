# Copyright (C) 2018-2021 Eric Kernin, NWNC HARFANG.

import harfang as hg
from random import uniform
from Machines import *


class Meteor(Missile):
    model_name = "Meteor"
    instance_scene_name = "weaponry/missile_meteor.scn"

    @classmethod
    def init(cls, scene):
        print("Meteor missile class init")

    def __init__(self, name, scene, scene_physics, pipeline_ressource: hg.PipelineResources, nationality):
        Missile.__init__(self, name, Meteor.model_name, nationality, scene, scene_physics, pipeline_ressource, Meteor.instance_scene_name)

        self.f_thrust = 80
        self.smoke_parts_distance = 1.44374
        self.angular_frictions = hg.Vec3(0.00005, 0.00005, 0.00005)  # pitch, yaw, roll
        self.drag_coeff = hg.Vec3(0.37, 0.37, 0.0003)
        self.life_delay = 40
        self.smoke_delay = 1.5

    def get_hit_damages(self):
        return uniform(0.40, 0.60)
