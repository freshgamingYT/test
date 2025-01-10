class Scale:
    def __init__(self):
        self.enabled = True

    def init(self):
        if self.enabled:
            return "Scale initialized"
        else:
            return "Scale is disabled"

    def calibrate(self):
        if self.enabled:
            return "Scale calibrated"
        else:
            return "Scale is disabled"

    def enable(self):
        self.enabled = True
        return "Scale enabled"

    def disable(self):
        self.enabled = False
        return "Scale disabled"
