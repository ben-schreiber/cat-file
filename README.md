# Cat-File
> A command-line tool for displaying the data found in files

## Motivation
Tabular data is stored in many different formats: csv, parquet, excel, etc. Additionally,
outside of personal projects, these files are often stored in the cloud; thereby, creating
the need to first download the download the files to a local machine, and only then find a
suitable program to open them in. Of course there are ways to download the files using a UI,
but why rule out using the CLI? Many of the common file formats have standalone CLI tools
to open and inspect them, but each one has its own quirks (such as not accepting paths to files
in the cloud as links or not allowing data to be piped into the program).

As such, `cat-file` comes to fill these gaps. It is a single tool for many common storage
formats, it allows data to be piped into it, and it reads the file into a buffer -- never
writing it to disk.

Note, this program is _not_ coming to replace `cat`-ing of non-tabular data files (e.g. JSON)

## Installation
```bash
pip install git+https://github.com/schreiberben/cat-file.git
```

## Usage
The following file formats are supported:
1. CSV
2. Parquet
3. Excel (reads the first sheet)
4. JSON Lines
The program can be run by either piping data into the program or by providing a path
to a local file. The program also accepts an optional flag indicating the type of file.
If no flag is provided, then the program will attempt to infer the file type.

In regards to what data is printed to the console, the default is to print the entire file.
However, there are optional `--head` and `--tail` arguments to print only the first or last
`N` lines of data from the file. The default `N` is 5, but any positive integer is also
accepted.

If printing the contents is not the desired action, there is an optional `--describe` flag
which can be passed to the CLI to print a synopsis of the file instead of its contents.

## Examples
### Calling Directly
When using a locally stored file, you can call the program directly and pass the path of the
file as a parameter:
```bash
cat-file ~/Desktop/file.csv
cat-file -c ~/Desktop/file.csv # Explicitly declaring the file type
cat-file --head ~/Desktop/file.csv # Printing only the first 5 lines
cat-file --head=7 ~/Desktop/file.csv # Printing only the first 7 lines
cat-file --describe ~/Desktop/file.csv # Printing a synopsis of the contents
```

### Piping Data into the Program
Alternatively, you can pipe data into the program. this is useful when dealing with files stored remotely.
```bash
cat /path/to/remote | cat-file
cat /path/to/remote | cat-file -c # Explicitly declaring the file type
cat /path/to/remote | cat-file --head # Printing only the first 5 lines
cat /path/to/remote | cat-file --head=7 # Printing only the first 7 lines
cat /path/to/remote | cat-file --describe # Printing a synopsis of the contents
```
