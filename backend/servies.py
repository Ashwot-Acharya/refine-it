from pypdf import PdfReader, PdfWriter
import threading 
import textanalysis as ta
filename = '1'

def perform_analysis(text):
    pass

def separate_paragraphs(text):

     paragraphs = text.split("\n")
     paragraphs = [p.strip() for p in paragraphs if p.strip()]
     for i, paragraph in enumerate(paragraphs):
        print(f"Paragraph {i + 1}: {paragraph}")
        print("------------------------")



def read_papers(pdf):
    try:
        reader = PdfReader(pdf)
        page_length =  len(reader.pages)
        for x in range(page_length):
            page = reader.pages[x]
            text = page.extract_text()
            ta.analyze_sentence(text , text , text)
            # separate_paragraphs(text)
    except Exception as e:
        print(e)      

def PDFsplit(pdf, sections):
    try:
        reader = PdfReader(pdf)

        total_pages = len(reader.pages)

        split_size = total_pages // sections
        splits = [split_size * i for i in range(1, sections)]

        start = 0

        for i, end in enumerate(splits + [total_pages]):
            writer = PdfWriter()

            outputpdf = pdf.split('.pdf')[0] + f"_part_{i + 1}.pdf"

            for page in range(start, end):
                writer.add_page(reader.pages[page])

            with open(outputpdf, "wb") as f:
                writer.write(f)

            start = end

    except Exception as e:
        print(e)


    

def run_page_slice(filename):
    t1 = threading.Thread(target=read_papers(f"./papers/{filename}_part_1.pdf"), name='t1')
    t2 = threading.Thread(target=read_papers(f"./papers/{filename}_part_2.pdf"), name='t2')
    t3 = threading.Thread(target=read_papers(f"./papers/{filename}_part_3.pdf"), name='t3')
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

# def run_para_slice(filename):

#     t1 = threading.Thread(target= separate_paragraphs(f"{filename}_part_1.pdf") , name ='t1')
#     t2 = threading.Thread(target= separate_paragraphs(f"{filename}_part_2.pdf") , name ='t2')
#     t3 = threading.Thread(target= separate_paragraphs(f"{filename}_part_3.pdf") , name ='t3')

#     t1.start()
#     t2.start()
#     t3.start()
#     t1.join()
#     t2.join()
#     t3.join()

run_page_slice('1')

PDFsplit('./papers/1.pdf' , 3)
