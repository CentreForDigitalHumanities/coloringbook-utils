import polars as pl


def summarize_response_data(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .group_by("survey")
        .agg(
            pl.col("page").n_unique().alias("unique_pages"),
            pl.col("page").count().alias("total_records"),
            pl.col("subject").n_unique().alias("unique_participants"),
        )
        .sort("survey", descending=False)
    )

def summarize_guess_percentages(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df
        .group_by(["survey", "page", "expected"])
        .agg(
            pl.col("color").count().alias("total_guesses"),
            pl.col("color").filter(pl.col("color").is_null()).count().alias("blank_guesses"),
            (pl.col("color").filter(pl.col("color").is_null()).count() / pl.col("color").count()).alias("blank_guess_percentage"),
            pl.col("color").n_unique().alias("unique_color_guesses"),
            pl.col("color").filter(pl.col("guess_result") == "correct").count().alias("correct_color_guesses"),
            (pl.col("color").filter(pl.col("guess_result") == "correct").count() / pl.col("color").count()).alias("correct_guess_percentage")
        )
        .sort("correct_guess_percentage", descending=False)
    )