import click

from cb_utils.data import *

pl.Config.set_tbl_rows(200)

@click.group()
def cli():
    pass


@cli.command()
@click.option("--cbdata", required=True, help="Path to the coloringbook data csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--cbmatch", required=True, help="Path to the coloringbook matching csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--participants", required=True, help="Path to the participants csv file (delimited by ,)", type=click.Path(exists=True))
def validate(cbdata: str, cbmatch: str, participants: str):
    # Load data to frames
    cb_df = read_cb_data(cbdata)
    match_df = read_cb_matching_data(cbmatch)
    cb_with_name = join_cb_with_matching(match_df, cb_df)
    participants_df = read_participant_data(participants)
    cb_with_participant = join_cb_with_participants(cb_with_name, participants_df)

    # Perform validations
    checks = []
    # Check if there are any duplicate names in participants file
    duplicate_participants = check_duplicate_participants(participants_df)
    if len(duplicate_participants) > 0:
        checks.append((f"🔥 Found {len(duplicate_participants)} duplicate names in participants data", duplicate_participants))
    else:
        checks.append(("👍 No duplicate names found in participants", None))
    
    # Check if there are any pages without expectations
    pages_no_expectations = pages_with_no_expectation(cb_df)
    if len(pages_no_expectations) > 0:
        checks.append((f"🔥 Found {len(pages_no_expectations)} pages without expectations", pages_no_expectations))
    else:
        checks.append(("👍 No pages without expectations found", None))

    # Check if there are any pages with multiple expectations
    pages_multiple_expectations = pages_with_multiple_expectations(cb_df)
    if len(pages_multiple_expectations) > 0:
        checks.append((f"🔥 Found {len(pages_multiple_expectations)} pages with multiple expectations", pages_multiple_expectations))
    else:
        checks.append(("👍 No pages with multiple expectations found", None))

    # Check if there are any missing matches in CB
    missing_matches = missing_cb_matches(cb_with_participant)
    if len(missing_matches) > 0:
        checks.append((f"🔥 Found {len(missing_matches)} missing matches", missing_matches))
    else:
        checks.append(("👍 No missing matches found", None))

    print("Checklist:\n")
    for check, _ in checks:
        print("\t", check)

    for check, check_df in checks:
        if check_df is not None:
            print("\n", check)
            print(check_df)

@cli.command()
@click.option("--cbdata", required=True, help="Path to the coloringbook data csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--cbmatch", required=True, help="Path to the coloringbook matching csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--participants", required=True, help="Path to the participants csv file (delimited by ,)", type=click.Path(exists=True))
def summary(cbdata: str, cbmatch: str, participants: str):
    # Load data to frames
    cb_df = read_cb_data(cbdata)
    match_df = read_cb_matching_data(cbmatch)
    cb_with_name = join_cb_with_matching(match_df, cb_df)

    # Survey Summary
    print("Survey Summary")
    print(survey_summary(cb_with_name))

    # Page summary
    print("Page Summary")
    print(page_summary(cb_with_name))

    # Page guesses
    print("Page Guesses")
    print(correct_area_guesses(cb_with_name))


@cli.command()
@click.option("--cbdata", required=True, help="Path to the coloringbook data csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--cbmatch", required=True, help="Path to the coloringbook matching csv file (delimited by ;)", type=click.Path(exists=True))
@click.option("--participants", required=True, help="Path to the participants csv file (delimited by ,)", type=click.Path(exists=True))
@click.option("--output", required=True, help="Name of CSV file to write data to", type=click.Path())
@click.option("--any-color", is_flag=True, help="If set, any color will be counted as correct")
def build(cbdata, cbmatch, participants, output, any_color):
    # Load data to frames
    cb_df = read_cb_data(cbdata)
    match_df = read_cb_matching_data(cbmatch)
    cb_with_name = join_cb_with_matching(match_df, cb_df)
    participants_df = read_participant_data(participants)
    cb_with_participant = join_cb_with_participants(cb_with_name, participants_df)
    out_df = build_output(cb_with_participant, any_color)
    out_df.write_csv(output)


def main():
    cli()


if __name__ == '__main__':
    main()