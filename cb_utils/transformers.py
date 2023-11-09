import polars as pl


def pipeline(df: pl.DataFrame, functions: list) -> pl.DataFrame:
    """Given a list of functions, apply them to a dataframe in order"""
    for f in functions:
        df = f(df)
    return df

def infer_guess_result(df: pl.DataFrame) -> pl.DataFrame:
    correct_guesses = (
        df
        .filter((pl.col("color").is_not_null()) & (pl.col("color") == pl.col("expected")))
        .with_columns(pl.lit("correct").alias("guess_result"))
    )
    incorrect_guesses = (
        df
        .filter(pl.col("color").is_not_null())
        .filter((pl.col("color") != pl.col("expected")) | (pl.col("expected").is_null()))
        .with_columns(pl.lit("incorrect").alias("guess_result"))
    )
    no_guesses = (
        df
        .filter(pl.col("color").is_null())
        .with_columns(pl.lit("no guess").alias("guess_result"))
    )
    return (
        pl.concat([correct_guesses, incorrect_guesses, no_guesses])
    )


def infer_chosen_word(df: pl.DataFrame) -> pl.DataFrame:
    """Given a fully merged df from dataset with a guess result, infer the chosen word for each page"""
    correct_guesses = (
        df
        .filter(pl.col("guess_result") == "correct")
        .sort("time")
        .unique(["subject", "page", "survey"], keep="first")
        .with_columns(pl.col("area").alias("chosen_word"))
    )
    incorrect_guesses = (
        df
        .filter(pl.col("guess_result") == "incorrect")
        .sort("time")
        .unique(["subject", "page", "survey"], keep="first")
        .with_columns(pl.col("area").alias("chosen_word"))
    )
    no_guesses = (
        df
        .filter(pl.col("guess_result") == "no guess")
        .sort("time")
        .unique(["subject", "page", "survey"], keep="first")
        .with_columns(pl.lit("skipped").alias("chosen_word"))
    )
    return (
        pl.concat([correct_guesses, incorrect_guesses, no_guesses])
        .unique(["subject", "page", "survey"], keep="first")
    )


def infer_category(df: pl.DataFrame, any_color: bool) -> pl.DataFrame:
    """Given a fully merged df from dataset with an infered chosen_word, infer the category for response"""
    if any_color is False:
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