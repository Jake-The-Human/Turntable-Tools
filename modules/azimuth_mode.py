from math import sqrt, log
from neopixel import NeoPixel
from modules.adc_sensor import AdcSensor

SAMPLE_BUFFER_SIZE: int = 1500


def _get_next_index(index: int, list_len: int) -> int:
    """This is for the moving average index so it does not go out of bounds"""
    return (index + 1) % list_len


class AzimuthMode:
    def __init__(self, pixel: NeoPixel) -> None:
        self._pixel = pixel
        self.rms_1: float = 0.0
        self.rms_2: float = 0.0

    def update(self, adc_sensor: AdcSensor) -> None:
        """Update the buffer with new samples and maintain a running RMS."""
        self.rms_1, self.rms_2 = adc_sensor.get_rms()

    # def measure_azimuth():
    #     print("Play the left-channel-only tone...")
    #     # time.sleep(5)  # Wait for the test tone to stabilize

    #     # Measure left channel signal and right channel crosstalk
    #     L_signal = rms_left.calculate_rms()
    #     R_crosstalk = rms_right.calculate_rms()

    #     print(f"Left Signal RMS: {L_signal:.4f} V")
    #     print(f"Right Crosstalk RMS: {R_crosstalk:.4f} V")

    #     # Calculate crosstalk in dB
    #     crosstalk_left_db = 20 * log(R_crosstalk / L_signal, 10)
    #     print(f"Crosstalk (left channel): {crosstalk_left_db:.2f} dB")

    #     print("\nPlay the right-channel-only tone...")
    #     time.sleep(5)  # Wait for the test tone to stabilize

    #     # Measure right channel signal and left channel crosstalk
    #     R_signal = rms_right.calculate_rms()
    #     L_crosstalk = rms_left.calculate_rms()

    #     print(f"Right Signal RMS: {R_signal:.4f} V")
    #     print(f"Left Crosstalk RMS: {L_crosstalk:.4f} V")

    #     # Calculate crosstalk in dB
    #     crosstalk_right_db = 20 * log(L_crosstalk / R_signal, 10)
    #     print(f"Crosstalk (right channel): {crosstalk_right_db:.2f} dB")

    #     # Return crosstalk ratios
    #     return crosstalk_left_db, crosstalk_right_db
