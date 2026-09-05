import pandas as pd


def clean_patients(df):
    cleaned = df.copy()

    # Convert dates to datetime.
    # Invalid values become NaT, but validation already confirmed
    # that the source dates are valid.
    cleaned["BIRTHDATE"] = pd.to_datetime(
        cleaned["BIRTHDATE"],
        errors="coerce",
        dayfirst=True
    )

    cleaned["DEATHDATE"] = pd.to_datetime(
        cleaned["DEATHDATE"],
        errors="coerce",
        dayfirst=True
    )

    # Preserve missing DEATHDATE values.
    # Do not remove patients based on missing values.

    return cleaned

def clean_encounters(df):
    cleaned = df.copy()

    # Convert encounter timestamps
    cleaned["START"] = pd.to_datetime(
        cleaned["START"],
        errors="coerce",
        utc=True
    )

    cleaned["STOP"] = pd.to_datetime(
        cleaned["STOP"],
        errors="coerce",
        utc=True
    )

    # Validation confirmed:
    # - Id is unique and non-missing
    # - PATIENT references are valid
    # - START/STOP are valid
    # - STOP is never before START
    # Therefore, no encounter rows are removed.

    return cleaned

def clean_careplans(df):
    cleaned = df.copy()

    cleaned["START"] = pd.to_datetime(
        cleaned["START"],
        errors="coerce",
        utc=True
    )

    cleaned["STOP"] = pd.to_datetime(
        cleaned["STOP"],
        errors="coerce",
        utc=True
    )

    return cleaned

if __name__ == "__main__":
    from extract_team1 import extract_patients, extract_encounters,extract_careplans


    patients = extract_patients()
    encounters = extract_encounters()
    careplans = extract_careplans()

    cleaned_patients = clean_patients(patients)
    cleaned_encounters = clean_encounters(encounters)
    cleaned_careplans = clean_careplans(careplans)

    print("\nPATIENT CLEANING")
    print("----------------")
    print("Before:", len(patients))
    print("After :", len(cleaned_patients))

    print("\nENCOUNTER CLEANING")
    print("------------------")
    print("Before:", len(encounters))
    print("After :", len(cleaned_encounters))
    print("Rows removed:", len(encounters) - len(cleaned_encounters))

    print("\nEncounter date types:")
    print(cleaned_encounters[["START", "STOP"]].dtypes)

    print("\nCAREPLANS CLEANING")
    print("------------------")
    print("Before:", len(careplans))
    print("After :", len(cleaned_careplans))
    print("Rows removed:", len(careplans) - len(cleaned_careplans))

    print("\nCareplan date types:")
    print(cleaned_careplans[["START", "STOP"]].dtypes)