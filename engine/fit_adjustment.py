from rules.fit_rules import FIT_ALLOWANCE

def apply_fit(measurements, fit):
    rules = FIT_ALLOWANCE.get(fit, FIT_ALLOWANCE["regular"])
    final = {}

    for k, v in measurements.items():
        final[k] = round(v + rules.get(k, 0), 1)

    final["FitType"] = fit
    return final
