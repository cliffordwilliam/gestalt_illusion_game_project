from constants import *


class Animator:
    '''
    How to use: 
        1: Give me animation data
        2: Starting animation
        3: Run my update callback

    What will happen:
        1: Timer counts until current animation frame duration
        2: If it is time to cycle to next frame, timer is 0 and go to next frame
        3: Check if next frame is last
        4: If it is last loop or not loop?
        5: Update owner region with updated frame
        6: If it is last and don't loop, got next animation?
        7: Got next animation? play it, reset timer and frame index
    '''

    def __init__(self, owner, animation_data, initial_animation_name):
        # region Owner
        self.owner = owner
        # endregion Owner

        # region Animation data
        self.animation_data = animation_data
        # endregion Animation data

        # region dynamic data
        self.current_animation = initial_animation_name
        self.is_loop = self.animation_data[self.current_animation]["is_loop"]
        self.next_animation = self.animation_data[self.current_animation]["next_animation"]
        self.frames_list = self.animation_data[self.current_animation]["frames_list"]
        self.frames_list_len = len(self.frames_list)
        self.frames_list_i_len = self.frames_list_len - 1
        self.frame_index = 0
        self.timer = 0
        self.frame_data = self.frames_list[self.frame_index]
        self.owner.region = self.frame_data["region"]
        self.duration = self.frame_data["duration"]
        # endregion dynamic data

    def set_current_animation(self, value):
        # region Return if new anim is same as current
        if self.current_animation == value:
            return
        # endregion Return if new anim is same as current

        # region Set new animation
        self.current_animation = value
        # endregion Set new animation

        # region New anim loop?
        self.is_loop = self.animation_data[self.current_animation]["is_loop"]
        # endregion New anim loop?

        # region New anim has next anim?
        self.next_animation = self.animation_data[self.current_animation]["next_animation"]
        # endregion New anim has next anim?

        # region Get new anim frames list, its len and i len
        self.frames_list = self.animation_data[self.current_animation]["frames_list"]
        self.frames_list_len = len(self.frames_list)
        self.frames_list_i_len = self.frames_list_len - 1
        # endregion Get new anim frames list, its len and i len

        # region Reset frame index and timer
        self.set_frame_index(0)
        self.timer = 0
        # endregion Reset frame index and timer

    def set_frame_index(self, value):
        # region Update frame index
        self.frame_index = value
        # endregion Update frame index

        # On last frame?
        if self.frame_index > self.frames_list_i_len:
            # This anim loop?
            if self.is_loop == 1:
                # region Reset frame index
                self.frame_index = 0
                # endregion Reset frame index

            # This anim don't loop?
            else:
                # region Stay on last frame
                self.frame_index -= 1
                # endregion Stay on last frame

                # Didn't loop, this anim has transition animation?
                if self.next_animation != 0:
                    # region Play next anim
                    self.set_current_animation(self.next_animation)
                    # endregion Play next anim

                # If staying on last frame no need to update data
                return

        # region Update data with new frame index, new region and duration
        self.frame_data = self.frames_list[self.frame_index]
        self.owner.region = self.frame_data["region"]
        self.duration = self.frame_data["duration"]
        # endregion Update data with new frame index, new region and duration

    def update(self, dt):
        # region update timer, set frame index
        self.timer += dt
        if self.timer >= self.duration:
            self.timer = 0
            self.set_frame_index(self.frame_index + 1)
        # endregion update timer, set frame index
