from fpdf import FPDF


class Shirtificate(FPDF):
    def add_centered_title(self, title_text):
        self.set_font("Arial", size=30, style="B")
        self.set_y(40)
        self.multi_cell(0, 10, title_text, border=0, align="C")

    def add_centered_image(self, image_path, width=100):
        x = (210 - width) / 2
        y = 100
        self.image(image_path, x=x, y=y, w=width)

    def add_centered_name_on_shirt(self, name):
        text_to_display = f"{name} took CS50"
        self.set_font("Arial", size=20, style="B")
        self.set_text_color(255, 255, 255)

        # Use the full text width to calculate the position
        text_width = self.get_string_width(text_to_display)
        text_x = (210 - text_width) / 2
        text_y = 140

        self.set_xy(text_x, text_y)
        self.cell(text_width, 10, text_to_display)


def create_shirtificate(name):
    # Initialize PDF with A4 format
    pdf = Shirtificate(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # Add title, image, and name to the PDF
    pdf.add_centered_title("CS50 Shirtificate")
    pdf.add_centered_image("shirtificate.png")
    pdf.add_centered_name_on_shirt(name)

    # Save the PDF
    pdf.output("shirtificate.pdf")


def main():
    name = input("Enter your name: ")
    create_shirtificate(name)


if __name__ == "__main__":
    main()
