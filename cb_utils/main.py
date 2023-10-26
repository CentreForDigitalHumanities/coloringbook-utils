import polars as pl





def read_cb_data(path: str) -> pl.DataFrame:
    """Reads a coloring book data file into a polars DataFrame"""
    return pl.read_csv(path, separator=";", infer_schema_length=20000)


def read_participant_data(path: str) -> pl.DataFrame:
    """Reads a participant data file into a polars DataFrame"""
    column_mapping = {
        'Deelnemernaam': 'name',
        'Leeftijd (maanden)': 'age_months',
        'Tijd in Nederland (in dagen)': 'days_in_nl',
        'Tijd op school (in dagen)': 'days_in_school',
        'Vluchteling (ja/nee)': 'is_refugee',
        'Thuistaal': 'native_language',
        'Versie': 'version',
        'Testdatum': 'test_date',
        'Zelfbeeldscore': 'selfesteem_score',
        'Opleidingsniveau 1': 'education_level_1',
        'Opleidingsniveau 2': 'education_level_2',
        'Thuistalen': 'home_languages',
        'Voorlezen': 'read_aloud',
        'Taal voorlezen': 'read_aloud_language',
        'Geboortedatum': 'date_of_birth',
        'Nederland': 'date_in_netherlands',
        'School': 'date_in_school',
        'Opmerkingen': 'comments',
        'Klas': 'class'
    }
    df = pl.read_csv(path, infer_schema_length=20000)
    return df.rename(column_mapping)

