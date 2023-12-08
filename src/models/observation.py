from dataclasses import dataclass

from numpy import ndarray


@dataclass
class Observation:
    average_preference: ndarray
    disclaimed: float
    chose: ndarray

    def __str__(self):
        w_str = " ".join(str(w) for w in self.average_preference)
        wp_str = " ".join(str(w) for w in self.chose)
        return f"{w_str} {self.disclaimed} {wp_str}"
