import PyPDF2

from iBott.files_and_folders.files import File


class PDF(File):
    """
    PDF Class Heritates from File Class
    Arguments:
        file_path (str): Path of the file
    Attributes:
        file_path (str): Path of the file
        pages (int): number of pages in the file
        info (str): info of the file

    Methods:
        read_pages(page_num, encoding=None): Returns a string with the text in the page
        append(pdf_document2,merge_path): Appends a pdf document to the current document
        split(): split pdf into several pdfs 
    """
    def __init__(self, path):

        super().__init__(path)
        self.pages = PyPDF2.PdfFileReader(open(path, "rb")).getNumPages() - 1
        self.info = PyPDF2.PdfFileReader(open(path, "rb")).getDocumentInfo()

    def read_page(self, page_num, encoding=None):
        """
        Read page from PDF, receives number of page to receive and encofing
        Arguments:
            page_num (int): number of page to receive
            encoding (str): encoding of the text
        Returns:
            str: text of the page
        """

        if encoding is None:
            encoding = "utf-8"
        with open(self.path, "rb") as file:
            pdf = PyPDF2.PdfFileReader(file)
            page = pdf.getPage(page_num)
            text = page.extractText().encode(encoding)
            if text is None:
                raise ValueError("Pdf not readable with this method, use OCR instead")
            return text

    def append(self, pdf_document2, merged_path):
        """
        Append new pdf to current and store it as a new one.
        Arguments:
            pdf_document2 (PDF): PDF to append
            merged_path (str): Path to store the new PDF
        """

        from PyPDF2 import PdfFileMerger
        pdfs = [str(self.path), str(pdf_document2)]
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(merged_path)

    def spit(self):
        """
        Split pdf into multiple pages with format: pdfName_n.pdf
        """

        pdf = PyPDF2.PdfFileReader(self.path)
        for page in range(self.pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))
            output_filename = '{}_page_{}.pdf'.format(self.file_name, page + 1)
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
