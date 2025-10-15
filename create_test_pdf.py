from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Welcome to the Nigerian audiobook converter!", ln=1)
pdf.multi_cell(0, 10, txt="This is a test. The Nigerian voice will pronounce this text with authentic Nigerian English accent. Nigeria is a beautiful country with rich culture and diversity.")
pdf.output("test.pdf")
print("Created test.pdf")
