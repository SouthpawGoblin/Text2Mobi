import os
import sys
import hashlib
import time
import shutil
from pyquery import PyQuery as pq


class Text2Mobi:
    """
    text to .mobi converter class
    """

    # TODO: support .pdf, .html etc...
    SUPPORTED_FILE_EXTS = ["txt", "html"]
    SUPPORTED_INPUT_TYPES = ["file", "string"]

    def __init__(self, book_title, input_file="", input_text="", output_path=""):
        assert len(book_title), "The book's title must be specified"
        self.book_title = book_title
        self.__input_type = None
        if len(input_file):
            norm_file_path = os.path.normpath(input_file)
            assert os.path.splitext(norm_file_path)[1] in Text2Mobi.SUPPORTED_FILE_EXTS, "Input File type not supported"
            self.input_file = norm_file_path
            self.__input_type = "file"
        elif len(input_text):
            # TODO: add string length limit lest out-of-memory issue occurs
            self.input_text = input_text
            self.__input_type = "string"

        # current directory is the default output path
        self.output_path = output_path if len(output_path) else os.getcwd()
        os.mkdir('./temp') if not os.path.exists('./temp') else None

    def convert(self):
        """
        do the conversion
        :return: an object of ConvertResult
        """
        if self.__input_type is None:
            return self.ConvertResult(False, fail_reason="no valid content uploaded")
        elif self.__input_type == "string":
            dir_name = self._md5(str(time.time()) + self.book_title)[:8]
            temp_dir = "./temp/" + dir_name
            temp_file = temp_dir + "/book.html"
            os.mkdir(temp_dir)
            with open("./templates/book.html", "r") as tpl:
                c = tpl.read()
                print(c)
                d = pq(c)
            d('article').append(self.input_text)
            d('title').empty().append(self.book_title)
            print(d)
            with open(temp_file, "w+") as f:
                f.write(str(d))
            self._kindlegen('./kindlegen/win32/kindlegen.exe', temp_file)

    @staticmethod
    def _md5(text):
        md5 = hashlib.md5()
        md5.update(str(text).encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def _kindlegen(kg_loc, tgt_loc):
        abs_kg = os.path.abspath(kg_loc)
        abs_tgt = os.path.abspath(tgt_loc)
        os.system(os.path.splitext(abs_kg)[0] + ' ' + abs_tgt)

    class ConvertResult:
        """
        object that will be returned by Text2Mobi.convert()
        """
        def __init__(self, success, output_file=None, fail_reason=None):
            self.success = True if success else False
            self.output_file = output_file
            self.fail_reason = fail_reason


if __name__ == "__main__":
    t2m = Text2Mobi("Python 改变当前工作目录", input_text="""Python 改变当前工作目录\n
今天在写一个Python脚本，要把一个svn project 先checkout出来，然后转到这个工程目录下执行其它的svn命令。\n

本来我是在Python里执行了一个cd命令，希望能转到目标工程目录下。但是这个cd命令一直执行不成功。后来了解到，其实这个cd命令已经执行成功了，只是它执行完以后又返回了当前的工作目录（也就是执行python脚本的这个目录），所以最终结果其实跟cd没有执行一样。\n

如果要达到这个目的，应该在脚本中显式地改变当前工作目录。目前我使用的是 os.chdir('目标目录')。注意之前要import os\n

 

 

python获得当前工作目录\n

import os \n
curDir = os.getcwd()\n

print(curDir )\n""")
    t2m.convert()
