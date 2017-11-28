# Text2Mobi
Convert text string or .txt/.html file to .mobi file for Amazon Kindle.

## Install
```
pip install text2mobi
```

## Usage
1. Import and initialize text2mobi.
```python
from text2mobi import Text2Mobi

t2m = Text2Mobi()
```
The initialization can take in 2 parameters:

- `kindlegen_path`: the converter depends on `kindlegen` tool, this package embeds one and uses it as default. You can configure your own kindlegen path through this parameter.
- `temp_path`: during the conversion, several temporary files will be generated, stored and finally deleted.This parameter configures the temporary folder, defaults to `./temp`.

2. Simply invoke the `convert` method.
```python
t2m.convert("Text2Mobi", input_text="This is a sample book.\nEnjoy!", output_path="./output")
```  
- `book_title`: a good book deserves a good title, right?
- `input_file`: path of the original file to be converted, currently supports `.txt` and `.html`.
- `input_text`: book content in plain text strings, will be ignored if `input_file` is given. 
- `output_path`: output path of the final `.mobi` file, it will be named as `book.mobi` by default.

## License
MIT