import click
import toml
from pathlib import Path
from dataclasses import dataclass
from functools import partial
from cb_utils.data import *
from cb_utils.transformers import *
from cb_utils.analysis import *

pl.Config.set_tbl_rows(200)


@dataclass
class Config:
    expectations: Path
    matching: Path
    participants: Path
    responses: Path
    any_color: bool
    output_file_prefix: Path

    @classmethod
    def from_path(cls, path: Path):
        with open(path, "r") as f:
            config = toml.load(path)
        return cls(**config)
    
    def get_dataset(self) -> Dataset:
        return Dataset.from_paths(
            responses_path=self.responses,
            participants_path=self.participants,
            matching_path=self.matching,
            expectations_path=self.expectations
        )


@click.group()
@click.option("--config", required=True, help="Path to config file", type=click.Path(exists=True))
@click.pass_context
def cli(ctx, config: str):
    ctx.obj = Config.from_path(Path(config))



@cli.command()
@click.pass_obj
def build(config: Config):
    # Load data to frames
    dataset = config.get_dataset()
    df = pipeline(
        dataset.full, 
        [
            infer_guess_result,
            infer_chosen_word, 
            partial(infer_category, any_color=config.any_color)
        ]
    ).sort(["survey", "subject", "page"])
    outpath = f"{config.output_file_prefix}_full_data.csv" if not config.any_color else f"{config.output_file_prefix}_full_data_any_color.csv"
    df.write_csv(outpath)


@cli.command()
@click.option("-t", "--summary-type", required=True, type=click.Choice(["results", "survey"]))
@click.option("--write/--no-write", default=False)
@click.pass_obj
def summarize(config: Config, summary_type: str, write: bool):
    dataset = config.get_dataset()
    match summary_type:
        case "results":
            df = infer_guess_result(dataset.full)
            df = summarize_guess_percentages(df)
        case "survey":
            df = summarize_response_data(dataset.full)
    if write:
        outpath = f"{config.output_file_prefix}_summary_{summary_type}.csv"
        df.write_csv(outpath)
    else:
        print(df)


def main():
    cli()


if __name__ == '__main__':
    main()