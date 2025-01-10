class Servo:
    def __init__(self):
        self.enabled = True

    def init(self):
        if self.enabled:
            return "Servo motor initialized"
        else:
            return "Servo motor is disabled"

    def enable(self):
        self.enabled = True
        return "Servo motor enabled"

    def disable(self):
        self.enabled = False
        return "Servo motor disabled"
