This is a command-line interface to use for analyzing coloringbook data.

## Installation

To install, use [pipx]()

`pipx install git+https://github.com/CentreForDigitalHumanities/coloringbook-utils`

To validate that your installation worked, run `cb-utils --help`

If this executes correctly, then installation was successful.


## Usage

This tool offers 3 commands:

- `cb-utils validate`
- `cb-utils summary`
- `cb-utils build`

Below are explanations of each.

### Validate

This runs a number of checks on the data you have. 
You can repair data accordingly in your input sheets. 
To use the command, you must also specify the input files.
An example of how this might look:

```bash
cb-utils validate --cbdata='coloringbook.csv' --cbmatch='cb_matching.csv' --participants='participants.csv'
```

![validate gif](demo_gifs/validate_demo.gif)

### Summary

You can use summary as a sanity check to get some quick stats about the data.
The command will show you three tables: survey summary, page summary, and page guess summary.

An example of the usage is:

```bash
cb-utils summary --cbdata='coloringbook.csv' --cbmatch='cb_matching.csv' --participants='participants.csv'
```

![summary gif](demo_gifs/summary_demo.gif)

### Build

With build you can synthesize the data into a single csv.
You can provide the `--any-color` flag to convert category to 0s and 1s as per specification based on color. 

You can invoke the command as so:

```bash
cb-utils build --cbdata='coloringbook.csv' --cbmatch='cb_matching.csv' --participants='participants.csv' --out='output.csv'
```

Or with the `any color` flag:

```bash
cb-utils build --cbdata='coloringbook.csv' --cbmatch='cb_matching.csv' --participants='participants.csv' --out='output.csv' --any-color
```

![build gif](demo_gifs/build_demo.gif)

## Troubleshooting

- If you get the following error: `polars.exceptions.SchemaFieldNotFoundError:`, please ensure that there are no spaces in the headers of any files
- The participants file must be a csv (separated by commas). You can export it to this format through excel (or any other spreadsheet software)
- If something does not work as expected or an output is incorrect, please make a github issue and if possible provide:
  - An example input
  - The expected output
  - The actual output