class Scale:
    def __init__(self):
        self.enabled = True

    def init(self):
        try:
            if self.enabled:
                return "Scale initialized"
            else:
                return "Scale is disabled"
        except Exception as e:
            return f"Error initializing scale: {e}"

    def calibrate(self):
        try:
            if self.enabled:
                return "Scale calibrated"
            else:
                return "Scale is disabled"
        except Exception as e:
            return f"Error calibrating scale: {e}"

    def enable(self):
        try:
            self.enabled = True
            return "Scale enabled"
        except Exception as e:
            return f"Error enabling scale: {e}"

    def disable(self):
        try:
            self.enabled = False
            return "Scale disabled"
        except Exception as e:
            return f"Error disabling scale: {e}"
