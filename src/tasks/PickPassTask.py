import time
from src.tasks.SRTriggerTask import SRTriggerTask

class PickPassTask(SRTriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Auto Claim Monthly Pass"
        self.description = "Automatically claims monthly pass when the interface appears"
        self.trigger_count = 0
        self.last_action_time = None
        

    def run(self):
        now = time.time()
        if self.last_action_time is not None and now - self.last_action_time <= 0.5:
            return False
        
        if self.ocr(0.30, 0.45, 0.70, 0.55, match='Collection Card'):
            self.click(0.5, 0.5)
            self.last_action_time = now
            return True
        
        if self.ocr(0.30, 0.55, 0.70, 0.65, match='monthly card rewards'):
            self.click(0.5, 0.5)
            self.last_action_time = now
            return True
        
        if self.ocr(0.35, 0.10, 0.65, 0.25, match='Obtained'):
            self.send_key('esc')
            self.last_action_time = now
            return True
            
        return False