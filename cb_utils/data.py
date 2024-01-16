import polars as pl
from pathlib import Path
from dataclasses import dataclass


def load_responses(path: Path) -> pl.DataFrame:
    """Columns: survey;page;area;subject;time;clicks;color;expected;here;category"""
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000)
        .with_columns(
            pl.when(pl.col("color") == "white").then(None).otherwise(pl.col("color")).keep_name()
        )
    )

def load_participants(path: Path) -> pl.DataFrame:
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
        'Opmerkingen': 'examinator_comments',
        'Klas': 'class'
    }
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000)
        .rename(column_mapping)
        .with_columns(
            pl.col("name").str.strip().str.to_uppercase()
        )
    )

def load_matching(path: Path) -> pl.DataFrame:
    """Columns: id;name;numeral;birth;eyesight;#lang;nativelang;survey;difficulty;topic;comments"""
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000)
        .rename({"comments": "participant_comments"})
        .with_columns(
            pl.col("name").str.strip().str.to_uppercase()
        )
    )

def load_expectations(path: Path) -> pl.DataFrame:
    """Columns: survey,page,expected word,,"""
    return (
        pl
        .read_csv(path, separator=";", infer_schema_length=20000, truncate_ragged_lines=True)
    )

@dataclass
class Dataset:
    responses: pl.DataFrame
    participants: pl.DataFrame
    matching: pl.DataFrame
    expectations: pl.DataFrame

    @classmethod
    def from_paths(cls, responses_path: Path, participants_path: Path, matching_path: Path, expectations_path: Path):
        return cls(
            responses=load_responses(responses_path),
            participants=load_participants(participants_path),
            matching=load_matching(matching_path),
            expectations=load_expectations(expectations_path)
        )

    @property
    def participants_with_metadata(self) -> pl.DataFrame:
        """participants + matching"""
        return (
            self.participants.join(
                self.matching, left_on="name", right_on="name", how="left"
            )
        )

    @property
    def responses_with_participants(self) -> pl.DataFrame:
        """participants_with_metadata + responses"""
        return (
            self.responses.join(
                self.participants_with_metadata, left_on=["subject", "survey"], right_on=["id", "survey"], how="left"
            )
        )

    @property
    def full(self) -> pl.DataFrame:
        """responses_with_participants + expectations"""
        response_table = (
            self.expectations.join(
                self.responses.select(["survey", "subject"]).unique(["survey", "subject"]),
                on=["survey"],
                how="left"
            )
        )
        return response_table.join(
            self.responses_with_participants,
            on=["survey", "page", "subject"], how="left"
        )