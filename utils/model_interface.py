from dataclasses import dataclass, asdict
from typing import Any, Optional
@dataclass
class PredictionResult:
    predicted_class: str
    confidence: Optional[float]
    probabilities: dict[str,float]
    model_version: str
    status: str
    message: str = ""
    def to_dict(self): return asdict(self)
def predict_eeg(eeg_data, sampling_rate=None, channels=None):
    if eeg_data is None or (sampling_rate is not None and sampling_rate <= 0):
        return PredictionResult("Not evaluated",None,{},"not-connected","invalid_input","Please provide valid EEG data and sampling rate.")
    return PredictionResult("Not evaluated",None,{},"not-connected","model_not_configured","CNN-LSTM model is not connected yet. No AI prediction was performed.")
