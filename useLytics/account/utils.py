def normalize_phone(phone_number: str | None):
    """parses the` phone_number` and normalize it"""
    # is not none and contains digits
    if not phone_number or not phone_number.isdigit():
        return None

    phone_number = phone_number.strip()

    if phone_number.startswith("+"):
        phone_number = phone_number.replace("+", "")

    if phone_number.startswith("254"):
        if len(phone_number) != 12:
            return None
        if not (phone_number.startswith("2547") or phone_number.startswith("2541")):
            return None
        return phone_number
    if len(phone_number) == 10:
        if phone_number.startswith("07") or phone_number.startswith("01"):
            return "254" + phone_number[1:]

    return None


def slugify(value: str) -> str:
    value = str(value).strip().lower()
    return "_".join(value.split(" "))
