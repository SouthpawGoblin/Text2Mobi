import os
import hashlib
import time
import shutil
from pyquery import PyQuery as pq


class Text2Mobi:
    """
    text to .mobi converter class
    """

    # TODO: support .pdf etc...
    SUPPORTED_FILE_EXTS = [".txt", ".html"]
    SUPPORTED_INPUT_TYPES = ["file", "string"]

    def __init__(self, kindlegen_path="./kindlegen/win32/kindlegen.exe", temp_path="./temp"):
        assert os.path.exists(kindlegen_path), "Kindlegen file not found"
        self.kindlegen_path = kindlegen_path
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        self.temp_path = temp_path

    def convert(self, book_title, input_file="", input_text="", output_path=""):
        """
        do the conversion
        :return:
        """
        assert len(book_title), "Book's title must be specified"
        input_type = None
        if len(input_file):
            input_file = os.path.normpath(input_file)
            input_file_ext = os.path.splitext(input_file)[1].lower()
            assert input_file_ext in Text2Mobi.SUPPORTED_FILE_EXTS, "Input File type not supported"
            input_type = "file"
        elif len(input_text):
            input_type = "string"

        # current directory is the default output path
        output_path = output_path if len(output_path) else os.getcwd()
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

        # 1. extract content string
        assert input_type is not None, "No valid content uploaded"
        content_string = ""
        if input_type == "string":
            content_string = input_text
        elif input_type == "file" and input_file_ext != ".html":
            content_string = self._extract_string(input_file)

        # 2. pre-process content string
        assert len(content_string) or input_file_ext == ".html", "Content extraction failed"
        processed_string = self._pre_process_string(content_string)

        # 3. inject content into template
        injected_html_path = ""
        if len(processed_string):
            dir_name = self._md5(str(time.time()) + book_title)[:8]
            temp_dir = self.temp_path + "/" + dir_name
            temp_file = temp_dir + "/book.html"
            os.mkdir(temp_dir)
            self._inject_into_template(book_title, processed_string, "./templates/book.html", temp_file)
            injected_html_path = temp_file
        elif input_type == "file" and input_file_ext == ".html":
            injected_html_path = input_file
        else:
            assert False, "Content pre-processing failed"

        # 4. kindlegen
        assert len(injected_html_path), "Html generation failed"
        self._kindlegen(self.kindlegen_path, injected_html_path)

        # 5. post-process
        book_path = os.path.splitext(injected_html_path)[0] + ".mobi"
        assert os.path.exists(book_path), "Kindlegen failed"
        shutil.move(book_path, output_path)
        shutil.rmtree(temp_dir) if not input_type == "file" or input_file_ext != ".html" else None
        assert os.path.exists(output_path + "/book.mobi"), "Post-process failed"

        print("Text to Mobi Finished!")

    @staticmethod
    def _extract_string(file_path):
        ext = os.path.splitext(file_path)[1]
        if ext == ".txt":
            with open(file_path, "r+") as f:
                return f.read()
        elif ext == ".pdf":
            # TODO
            return ""

    @staticmethod
    def _pre_process_string(string):
        return string.replace("\n", "<br>").replace(" ", "&nbsp;").replace("\t", "&nbsp;" * 4)

    @staticmethod
    def _inject_into_template(title, content, template_path, output_path):
        with open(template_path, "r") as tpl:
            d = pq(tpl.read())
        d('title').empty().append(title)
        d('article').append(content)
        with open(output_path, "w+", encoding="utf-8") as f:
            f.write(str(d))

    @staticmethod
    def _kindlegen(kindlegen_path, target_path):
        abs_kg = os.path.abspath(kindlegen_path)
        abs_tgt = os.path.abspath(target_path)
        os.system(os.path.splitext(abs_kg)[0] + ' ' + abs_tgt)

    @staticmethod
    def _md5(text):
        md5 = hashlib.md5()
        md5.update(str(text).encode('utf-8'))
        return md5.hexdigest()


if __name__ == "__main__":
    t2m = Text2Mobi()
    t2m.convert("Text2Mobi", input_text="This is a sample book.\nEnjoy!", output_path="./output")
