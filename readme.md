This is a command-line interface to use for analyzing coloringbook data.

## Installation

To install, use [pipx](https://pypa.github.io/pipx/installation/)

`pipx install git+https://github.com/CentreForDigitalHumanities/coloringbook-utils`

To validate that your installation worked, run `cb-utils --help`

If this executes correctly, then installation was successful.


## Usage

This tool offers 2 commands:

- `cb-utils summarize`
- `cb-utils build`

Below are explanations of each.
Every command must be prefixed with a reference ot a configuration file.
The configuration file is written in `toml` and looks like so:

```toml
expectations = "data/expectations.csv"
matching = "data/matching.csv"
participants = "data/participants.csv"
responses = "data/responses.csv"
any_color = false
output_file_prefix = ".data/output"
```

### Summarize

You can use summary as a sanity check to get some quick stats about the data.
The command will show you three tables: survey summary, page summary, and page guess summary.

An example of the usage is:

```bash
cb-utils --config config.toml summarize -t results
```

or 

```bash
cb-utils --config config.toml summarize -t survey
```


This will output data about guesses and the survey respectively.
You can append a `--write` flag to store this data in a file:

```bash
cb-utils --config config.toml summarize -t results --write
```

### Build

With build you can synthesize the data into a single csv.

You can invoke the command as so:

```bash
cb-utils --config config.toml build
```

## Troubleshooting

- If you get the following error: `polars.exceptions.SchemaFieldNotFoundError:`, please ensure that there are no spaces in the headers of any files
- The participants file must be a csv (separated by commas). You can export it to this format through excel (or any other spreadsheet software)
- If something does not work as expected or an output is incorrect, please make a github issue and if possible provide:
  - An example input
  - The expected output
  - The actual output