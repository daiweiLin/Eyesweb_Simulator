class patchflag:
    """Object of flags for interrupt requests"""

    def __init__(self, type):
        self.type = type
        if self.type == 'sma-infrared':
            self.sma_ack = False
            self.LED_ack = False
