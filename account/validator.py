def contact_number_validator(value:str) -> bool:
    return len(value) == 11 and value.startswith("01")