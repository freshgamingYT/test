class Servo:
    def __init__(self):
        self.enabled = True

    def init(self):
        try:
            if self.enabled:
                return "Servo motor initialized"
            else:
                return "Servo motor is disabled"
        except Exception as e:
            return f"Error initializing servo motor: {e}"

    def enable(self):
        try:
            self.enabled = True
            return "Servo motor enabled"
        except Exception as e:
            return f"Error enabling servo motor: {e}"

    def disable(self):
        try:
            self.enabled = False
            return "Servo motor disabled"
        except Exception as e:
            return f"Error disabling servo motor: {e}"
