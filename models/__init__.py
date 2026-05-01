"""
预警模型包
"""

from .warning_models import (
    # 11个单项预警
    blood_pressure_warning_algorithm,
    pulse_pressure_warning_algorithm,
    morning_hypertension_warning_algorithm,
    ecg_warning_algorithm,
    spo2_warning_algorithm,
    hrv_warning_algorithm,
    glucose_warning_algorithm,
    ketone_warning_algorithm,
    uric_acid_warning_algorithm,
    temperature_warning_algorithm,
    weight_warning_algorithm,
    # 12个联合预警
    dka_warning_algorithm,
    stroke_warning_algorithm,
    ami_warning_algorithm,
    osa_warning_algorithm,
    metabolic_syndrome_warning_algorithm,
    respiratory_failure_warning_algorithm,
    heart_failure_warning_algorithm,
    hypoglycemia_coma_warning_algorithm,
    hhs_warning_algorithm,
    sepsis_warning_algorithm,
    arrhythmia_death_warning_algorithm,
    gout_warning_algorithm,
    # 2个专项预警
    stroke_complete_warning_algorithm,
    ami_complete_warning_algorithm
)

__all__ = [
    # 11个单项预警
    "blood_pressure_warning",
    "pulse_pressure_warning",
    "morning_hypertension_warning",
    "ecg_warning",
    "spo2_warning",
    "hrv_warning",
    "glucose_warning",
    "ketone_warning",
    "uric_acid_warning",
    "temperature_warning",
    "weight_warning",
    # 12个联合预警
    "dka_warning",
    "stroke_warning",
    "ami_warning",
    "osa_warning",
    "metabolic_syndrome_warning",
    "respiratory_failure_warning",
    "heart_failure_warning",
    "hypoglycemia_coma_warning",
    "hhs_warning",
    "sepsis_warning",
    "arrhythmia_death_warning",
    "gout_warning",
    # 2个专项预警
    "stroke_complete_warning",
    "ami_complete_warning"
]