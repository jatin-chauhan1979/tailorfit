def recommend_fit(m):
    chest = m.get("Chest", 0)
    waist = m.get("Waist", 0)
    hip = m.get("Hip", chest)

    if chest == 0 or waist == 0:
        return "regular"

    if chest / waist > 1.25:
        return "slim"
    if abs(chest - waist) < 6:
        return "loose"

    return "regular"
