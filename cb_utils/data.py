import polars as pl


def read_cb_data(path: str) -> pl.DataFrame:
    """Columns: survey;page;area;subject;time;clicks;color;expected;here;category"""
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000)
        .with_columns(
            pl.when(pl.col("color") == "white").then(None).otherwise(pl.col("color")).keep_name()
        )
    )

def read_participant_data(path: str) -> pl.DataFrame:
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
    return (
        pl
        .read_csv(path, infer_schema_length=20000)
        .rename(column_mapping)
        .with_columns(
            pl.col("name").str.to_uppercase().alias("match_name")
        )
    )

def check_duplicate_participants(participant_df: pl.DataFrame) -> pl.DataFrame:
    return (
        participant_df
        .with_row_count(offset=1)
        .with_columns(pl.col("match_name").is_duplicated().alias("is_duplicate"))
        .filter(pl.col("is_duplicate"))
        .select(["row_nr", "name"])
    )

def read_cb_matching_data(path: str) -> pl.DataFrame:
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000)
        .with_columns(
            pl.col("name").str.to_uppercase()
        )
        .select(["id", "name"])
    )


def join_cb_with_matching(matching_df: pl.DataFrame, cb_df: pl.DataFrame) -> pl.DataFrame:
    return cb_df.join(matching_df, left_on="subject", right_on="id", how="left")

def join_cb_with_participants(cb_df: pl.DataFrame, participant_df: pl.DataFrame) -> pl.DataFrame:
    return cb_df.join(participant_df, left_on="name", right_on="match_name", how="left", suffix="_participant")

def missing_cb_matches(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .filter(pl.col("name_participant").is_null())
        .select(["name", "name_participant", "subject"])
        .unique(["name", "subject"])
    )

def survey_summary(cb_df: pl.DataFrame) -> pl.DataFrame:
    return (
        cb_df
        .group_by("survey")
        .agg(
            pl.col("page").n_unique().alias("unique_pages"),
            pl.col("page").count().alias("total_pages"),
            pl.col("name").n_unique().alias("unique_participants"),
        )
    )

def page_summary(cb_df: pl.DataFrame) -> pl.DataFrame:
    return (
        cb_df
        .filter(pl.col("area").is_not_null())
        .group_by("page")
        .agg(pl.col("area").n_unique().alias("unique_areas"))
    )

def correct_area_guesses(cb_df: pl.DataFrame) -> pl.DataFrame:
    return (
        cb_df
        .filter(pl.col("expected").is_not_null())
        .group_by(["page", "expected"])
        .agg(
            # total amount of guesses
            pl.col("color").count().alias("total_guesses"),
            # blank guesses
            pl.col("color").filter(pl.col("color").is_null()).count().alias("blank_guesses"),
            # percentage of blank guesses
            (pl.col("color").filter(pl.col("color").is_null()).count() / pl.col("color").count()).alias("blank_guess_percentage"),
            # amount of unique colors used as an input
            pl.col("color").n_unique().alias("unique_color_guesses"),
            # amount of times color matches expected
            pl.col("color").filter(pl.col("color") == pl.col("expected")).count().alias("correct_color_guesses"),
            # percentage of correct guesses
            (pl.col("color").filter(pl.col("color") == pl.col("expected")).count() / pl.col("color").count()).alias("correct_guess_percentage")
        )
        .sort("correct_guess_percentage", descending=False)
    )

def with_expectation_count(cb_df: pl.DataFrame) -> pl.DataFrame:
    return (
        cb_df
        .group_by("page")
        .agg(
            # the amount of unique expectations that are not null
            pl.col("expected").filter(pl.col("expected").is_not_null()).n_unique().alias("unique_expectations"),
        )
    )

def pages_with_no_expectation(cb_df: pl.DataFrame) -> pl.DataFrame:
    return with_expectation_count(cb_df).filter(pl.col("unique_expectations") == 0)

def pages_with_multiple_expectations(cb_df: pl.DataFrame) -> pl.DataFrame:
    return with_expectation_count(cb_df).filter(pl.col("unique_expectations") > 1)


def compute_chosen_word(group_df: pl.DataFrame) -> pl.DataFrame:
    correct_color = group_df.filter(pl.col("color") == pl.col("expected"))
    if len(correct_color) > 0:
        return correct_color.sort("time").sample(1).with_columns(
            pl.col("area").alias("chosen_word"),
        )
    colored = group_df.filter(pl.col("color").is_not_null())
    if len(colored) > 0:
        return colored.sort("time").sample(1).with_columns(
            pl.col("area").alias("chosen_word"),
        )
    return group_df.sort("time").sample(1).with_columns(
        pl.lit("skipped").alias("chosen_word")
    )

def build_output(df: pl.DataFrame, any_color = False) -> pl.DataFrame:
    df = (
        df
        .with_columns(
            pl.when(pl.col("expected").is_not_null()).then(pl.col("area")).otherwise(None).alias("expected_word"),
        )
        .group_by(["survey", "page", "subject"]).map_groups(compute_chosen_word)
        .rename({
            "name_participant": "nameExcel",
            "name": "nameCB"
        })
    )
    if not any_color:
        return (
            df
            .with_columns(
                pl.when((pl.col("chosen_word") == "skipped") & (pl.col("expected").is_not_null())).then(pl.lit("not_expected"))
                .when((pl.col("chosen_word") == "skipped") & (pl.col("expected").is_null())).then(pl.lit("unspecified"))
                .otherwise(pl.col("category")).alias("category")
            )
        )
    else:
        return (
            df
            .with_columns(
                pl.when(pl.col("category").is_in(["expected", "miscolored"])).then(pl.lit(1))
                .otherwise(0).alias("category")
            )
        )