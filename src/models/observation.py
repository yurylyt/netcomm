from dataclasses import dataclass

from numpy import ndarray
import json


@dataclass
class Observation:
    preference: ndarray
    disclaimed: float
    chose: ndarray

    def __str__(self):
        w_str = " ".join(str(w) for w in self.preference)
        wp_str = " ".join(str(w) for w in self.chose)
        return f"{w_str} {self.disclaimed} {wp_str}"
