import time
import datetime
import re
import threading

from ok import og

from src.tasks.SRTriggerTask import SRTriggerTask

class FishingTask(SRTriggerTask):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Fishing"
        self.description = "Automatically fishes after interacting with fishing spot"
        
        self.settings = [
            {'key': 'ignore_tension_spam_click', 'label': 'Ignore line tension and spam click (slows reeling, reduces occasional line breaks)', 'default': False},
            {'key': 'switch_rod_key', 'label': 'Switch rod key', 'default': "m"}
        ]
        
        self.default_config.update({
            setting['label']: setting['default'] for setting in self.settings
        })
        
        self._settings_map = {s['key']: s for s in self.settings}
        
        self.trigger_count = 0

        # State variables for the "fish reeling" minigame
        self.pos = 0
        self.last_update_time = None
        self.key_a_pressed = False
        self.key_d_pressed = False
        self.fish_pos_from_game = 0

        self.last_start_time = None
        self.last_reeling_time = None
        self.last_continue_time = None
        self.last_switch_time = None

        # For asynchronous splash detection
        self._splash_finder_thread = None
        self._fish_pos_lock = threading.Lock()

        self.regex_map = {
            'chinese': {
                'add_rod': re.compile('添加鱼竿'),
                'continue_fishing': re.compile('继续钓鱼'),
                'use': re.compile('使用'),
            },
            'english': {
                'add_rod': re.compile('pole'),
                'continue_fishing': re.compile('Continue fishing'),
                'use': re.compile('Use'),
            }
        }

    def _splash_finder_worker(self):
        """
        Asynchronous task for finding splash.
        """
        splash_box = self.find_splash()
        if splash_box:
            with self._fish_pos_lock:
                self.fish_pos_from_game = splash_box[0].center()[0] / (self.width / 2) - 1 + 0.04

    def run(self):
        """
        Main execution loop for the fishing task.
        Calls the corresponding handler function based on current game state.
        """
        if self._handle_minigame():
            return
        if self._handle_start_and_rod_change():
            return
        if self._handle_hook_fish():
            return
        if self._handle_continue_fishing():
            return

    def _handle_start_and_rod_change(self) -> bool:
        """Check initial fishing interface to cast or replace broken rod."""
        now = time.time()
        if self.last_start_time is not None and now - self.last_start_time <= 3:
            return False
        if self._find_fishing_level():
            self.sleep(0.5)
            # Check if rod is broken
            if self.ocr(0.90, 0.92, 0.96, 0.96, match=self.get_regex('add_rod')):
                self.log_info('Switching rod', notify=False)
                self.send_key(self.get_config_value('switch_rod_key'))
                use_boxes = self.wait_ocr(box=None, match=self.get_regex('use'), log=False, threshold=0.8, time_out=15)
                if use_boxes:
                    self.log_info('Clicking use rod', notify=False)
                    center = use_boxes[0].center()
                    self.click(center[0] / self.width, center[1] / self.height)
                else:
                    self.log_info('Out of rods', notify=True)
                    self.screenshot()
                    raise Exception("Out of rods, need to implement rod purchasing")
            else:
                self.log_info('Casting', notify=False)
                self.click(0.5, 0.5)
                self.last_start_time = now
            return True
        return False

    def _handle_hook_fish(self) -> bool:
        """Check for fish hooked prompt and click to start reeling."""
        now = time.time()
        if self.last_reeling_time is not None and now - self.last_reeling_time <= 3:
            return False
        if self.find_one("hint_fishing_click", threshold=0.5):
            self.log_info('Fish hooked', notify=False)
            self.my_mouse_down(0.5, 0.5)
            self.last_update_time = time.time()
            self.pos = 0
            self.last_reeling_time = now
            return True
        return False

    def _handle_continue_fishing(self) -> bool:
        # Click continue fishing at most once per second
        now = time.time()
        if self.last_continue_time is not None and now - self.last_continue_time <= 1:
            return False
        if self._match_continue_fishing():
            self.log_info('Clicking continue fishing', notify=False)
            self.click(0.82, 0.90)
            self.last_continue_time = now
            return True
        return False

    def _handle_minigame(self) -> bool:
        """Manage reeling and fish playing"""
        # If "line tension" text is visible, need to reel in.
        if self.find_one("box_fishing_icon", box=self.box_of_screen(0.33, 0.80, 0.37, 0.87)):
            if self.get_config_value('ignore_tension_spam_click') or self.find_one("box_stop_pull", box=self.box_of_screen(0.50, 0.75, 0.70, 0.92), threshold=0.5):
                self.my_mouse_switch(0.5, 0.5)
            else:
                self.my_mouse_down(0.5, 0.5)
            # Get actual fish position
            if self._splash_finder_thread is None or not self._splash_finder_thread.is_alive():
                self._splash_finder_thread = threading.Thread(target=self._splash_finder_worker)
                self._splash_finder_thread.start()
            fish_pos_for_minigame = 0
            with self._fish_pos_lock:
                fish_pos_for_minigame = self.fish_pos_from_game
            self._play_the_fish(fish_pos_for_minigame)
            return True
        elif self.last_update_time:
            # If minigame is not active, ensure mouse and keys are released.
            self._reset_minigame_state()
            return True
        return False

    def _play_the_fish(self, fish_pos: float):
        delta_time = self._update_time()

        normalized_fish_pos = min(max(fish_pos / 0.7, -1.3), 1.3)

        self._update_rod_position(delta_time)
        self._update_key_presses(normalized_fish_pos)

    def _update_time(self) -> float:
        """Calculate and return time difference (delta_time) since last update."""
        current_time = time.time()
        if self.last_update_time is None:
            self.last_update_time = current_time
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        return delta_time

    def _update_key_presses(self, normalized_fish_pos: float):
        """Decide which key to press or release based on fish position."""
        if abs(self.pos - normalized_fish_pos) < 0.06:
            return
        if normalized_fish_pos < self.pos:
            # Fish is to the left of rod, rod is on right side of screen, release D key
            if self.pos > 0 and self.key_d_pressed:
                self.send_key_up('d')
                self.key_d_pressed = False
            # Fish is to the left of rod, rod is on left side of screen, press A key
            if self.pos <= 0 and not self.key_a_pressed:
                self.send_key_down('a')
                self.key_a_pressed = True
        else: 
            # Fish is to the right of rod, rod is on left side of screen, release A key
            if self.pos < 0 and self.key_a_pressed:
                self.send_key_up('a')
                self.key_a_pressed = False
            # Fish is to the right of rod, rod is on right side of screen, press D key
            if self.pos >= 0 and not self.key_d_pressed:
                self.send_key_down('d')
                self.key_d_pressed = True

    def _update_rod_position(self, delta_time: float):
        """Update fishing rod position."""
        # When no keys are pressed, drift toward center point
        if not self.key_a_pressed and not self.key_d_pressed:
            if self.pos > 0: 
                self.pos -= 1.0 * delta_time
                if self.pos < 0: self.pos = 0
            else : 
                self.pos += 1.0 * delta_time
                if self.pos > 0: self.pos = 0
        
        # When 'A' key is pressed and pos < 0, move toward -1
        if self.key_a_pressed and self.pos <= 0:
            self.pos -= 0.5 * delta_time
            
        # When 'D' key is pressed and pos > 0, move toward 1
        if self.key_d_pressed and self.pos >= 0:
            self.pos += 0.5 * delta_time
            
        # Limit position to range [-1, 1]
        self.pos = min(max(self.pos, -1.0), 1.0)
    
    def _reset_minigame_state(self):
        """Reset fish playing state when reeling ends."""
        self.log_info('Resetting fish play', notify=False)
        self.my_mouse_up()
        if self.key_a_pressed:
            self.send_key_up('a')
            self.key_a_pressed = False
        if self.key_d_pressed:
            self.send_key_up('d')
            self.key_d_pressed = False
        self.last_update_time = None
        self.fish_pos_from_game = 0

    def find_splash(self, threshold=0.5):
        ret = og.my_app.yolo_detect(self.frame, threshold=threshold, label=0)
        # for box in ret:
        #     self.log_info(box, notify=False)
        #     self.screenshot('splash', show_box=True, frame_box=box)
        return ret

    def _find_fishing_level(self):
        if self.get_game_language() == 'chinese':
            return self.find_one("box_fishing_level", box=self.box_of_screen(0.56, 0.91, 0.60, 0.96))
        else:
            return self.find_one("box_fishing_level_eng", box=self.box_of_screen(0.56, 0.91, 0.60, 0.96))

    def _match_continue_fishing(self):
        lang = self.get_game_language()
        if lang == 'chinese':
            return self.ocr(0.79, 0.88, 0.87, 0.93, match=self.get_regex('continue_fishing'))
        else:
            return self.ocr(0.76, 0.88, 0.90, 0.93, match=self.get_regex('continue_fishing'))