from enum import Enum, auto

class State(Enum):
    IDLE        = auto()
    PREHEAT     = auto()
    MOISTURE_LOCK = auto()
    EXTRACTING  = auto()
    CONDITIONING = auto()
    COMPLETE    = auto()

class ProcessFSM:
    def __init__(self):
        self.state = State.IDLE

    def transition(self, sensor_data):
        t   = sensor_data.get('temp', 0)
        m   = sensor_data.get('moisture', 0)
        ph  = sensor_data.get('ph', 0)
        cm  = sensor_data.get('compost_moisture', 0)
        cur = sensor_data.get('current', 0)

        if self.state == State.PREHEAT and t >= 80:
            self.state = State.MOISTURE_LOCK

        elif self.state == State.MOISTURE_LOCK and 10 <= m <= 12.8:
            self.state = State.EXTRACTING

        elif self.state == State.EXTRACTING:
            if cur > 7.5:
                return 'JAM_DETECTED'
            if t >= 175:
                return 'OVERHEAT_WARNING'

        elif self.state == State.CONDITIONING:
            if 6.5 <= ph <= 7.0 and 40 <= cm <= 60:
                self.state = State.COMPLETE

        return self.state.name

    def start(self):
        if self.state == State.IDLE:
            self.state = State.PREHEAT

    def advance_to_conditioning(self):
        self.state = State.CONDITIONING
