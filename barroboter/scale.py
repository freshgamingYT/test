class Scale:
    """
    A class to represent the scale and its related operations.
    """

    def __init__(self):
        self.enabled = True

    def init(self):
        """
        Initialize the scale.

        Returns:
            str: A message indicating the scale's initialization status.
        """
        if self.enabled:
            return "Scale initialized"
        else:
            return "Scale is disabled"

    def calibrate(self):
        """
        Calibrate the scale.

        Returns:
            str: A message indicating the scale's calibration status.
        """
        if self.enabled:
            return "Scale calibrated"
        else:
            return "Scale is disabled"

    def enable(self):
        """
        Enable the scale.

        Returns:
            str: A message indicating the scale's enable status.
        """
        self.enabled = True
        return "Scale enabled"

    def disable(self):
        """
        Disable the scale.

        Returns:
            str: A message indicating the scale's disable status.
        """
        self.enabled = False
        return "Scale disabled"
