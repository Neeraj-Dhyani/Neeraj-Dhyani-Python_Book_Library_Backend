import random
import os 
import fitz
import string 
import random
def genrate_random_num():
    num = 9
    generated_num = ""
    for i in range(5):
        new_num = random.randint(0, num)
        generated_num += str(new_num)
    
    return generated_num

# genrate_random_num()

def gen_otp():
    az_list = list(string.ascii_lowercase)
    otp = ""

    for i in range(5):
        if(i <= 2):
           letter = random.randint(0, 5)
           otp += az_list[letter]
        new_num = random.randint(1, 9)
        otp += str(new_num)

    return otp
        

def is_folder():
    dir = "Book_PDF"
    if not os.path.exists(dir):
        os.mkdir(dir)

def generate_thumnail(pdf_path , thumpath):
    pdf = fitz.open(pdf_path)
    page = pdf.load_page(0)
    pix = page.get_pixmap(matrix=fitz.Matrix(2,2))

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    thumbnail_path = os.path.join(
        thumpath,
        f"{pdf_name}.png"
    )
    pix.save(thumbnail_path)
    return f"/media/thumbnail/{pdf_name}.png"

