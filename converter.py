import os
import hashlib
import time
import logging
from pyquery import PyQuery as pq


class Text2Mobi:
    """
    text to .mobi converter class
    """

    # TODO: support .pdf, .html etc...
    SUPPORTED_FILE_EXTS = [".txt", ".html"]
    SUPPORTED_INPUT_TYPES = ["file", "string"]

    def __init__(self, kindlegen_path, temp_folder_path=None):
        assert os.path.exists(kindlegen_path), "Kindlegen file not found"
        self.kindlegen_path = kindlegen_path
        if temp_folder_path and os.path.isdir(temp_folder_path):
            self.temp_folder_path = temp_folder_path
        else:
            logging.warning("No valid 'temp_folder_path' is given, using default './temp'")
            self.temp_folder_path = "./temp"

    def convert(self, book_title, input_file="", input_text="", output_path=""):
        """
        do the conversion
        :return:
        """
        assert len(book_title), "Book's title must be specified"
        input_type = None
        if len(input_file):
            input_file = os.path.normpath(input_file)
            input_file_ext = os.path.splitext(input_file)[1]
            assert input_file_ext in Text2Mobi.SUPPORTED_FILE_EXTS, "Input File type not supported"
            input_type = "file"
        elif len(input_text):
            input_type = "string"

        # current directory is the default output path
        output_path = output_path if len(output_path) else os.getcwd()
        os.mkdir(self.temp_folder_path) if not os.path.exists(self.temp_folder_path) else None

        if input_type is None:
            logging.error("No valid content uploaded")
            return
        elif input_type == "file":
            if input_file_ext == ".txt":
                with open(input_file, "r+") as f:
                    input_text = f.read()
        elif input_type == "string":
            dir_name = self._md5(str(time.time()) + book_title)[:8]
            temp_dir = "./temp/" + dir_name
            temp_file = temp_dir + "/book.html"
            os.mkdir(temp_dir)
            with open("./templates/book.html", "r") as tpl:
                c = tpl.read()
                print(c)
                d = pq(c)
            d('article').append(input_text)
            d('title').empty().append(book_title)
            print(d)
            with open(temp_file, "w+") as f:
                f.write(str(d))
            self._kindlegen('./kindlegen/win32/kindlegen.exe', temp_file)

    @staticmethod
    def _extract_string(file_path):
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def _pre_process_string(string):
        pass

    @staticmethod
    def _inject_into_template(string, template_path):
        pass

    @staticmethod
    def _kindlegen(kindlegen_path, target_path):
        abs_kg = os.path.abspath(kindlegen_path)
        abs_tgt = os.path.abspath(target_path)
        os.system(os.path.splitext(abs_kg)[0] + ' ' + abs_tgt)

    @staticmethod
    def _post_process_output(output_path, target_path):
        pass

    @staticmethod
    def _md5(text):
        md5 = hashlib.md5()
        md5.update(str(text).encode('utf-8'))
        return md5.hexdigest()


if __name__ == "__main__":
    t2m = Text2Mobi("./kindlegen/win32/kindlegen.exe")
    t2m.convert("my first book", input_text="This is my first book!")
