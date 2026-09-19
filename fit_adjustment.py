from fit_rules import FIT_ALLOWANCE

def apply_fit(measurements, fit):
    rules = FIT_ALLOWANCE.get(fit, FIT_ALLOWANCE["regular"])

    adjusted = {}
    for key, value in measurements.items():
        if key in rules:
            adjusted[key] = round(value + rules[key], 1)
        else:
            adjusted[key] = value

    return adjusted
