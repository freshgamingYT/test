class Servo:
    """
    A class to represent the servo motor and its related operations.
    """

    def __init__(self):
        self.enabled = True

    def init(self):
        """
        Initialize the servo motor.

        Returns:
            str: A message indicating the servo motor's initialization status.
        """
        if self.enabled:
            return "Servo motor initialized"
        else:
            return "Servo motor is disabled"

    def enable(self):
        """
        Enable the servo motor.

        Returns:
            str: A message indicating the servo motor's enable status.
        """
        self.enabled = True
        return "Servo motor enabled"

    def disable(self):
        """
        Disable the servo motor.

        Returns:
            str: A message indicating the servo motor's disable status.
        """
        self.enabled = False
        return "Servo motor disabled"
