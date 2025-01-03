import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

class PDFToImageConverter:
    def __init__(self, root):
        self.root = root
        self.pdf_path = None
        self.output_dir = None
        self.thumbnail_canvas = tk.Canvas(self.root, width=300, height=400, bg="white")

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="PDF to Image Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_pdf_button = tk.Button(self.root, text="Select PDF", command=self.select_pdf)
        select_pdf_button.pack(pady=(0, 10))

        select_output_dir_button = tk.Button(self.root, text="Select Output Directory", command=self.select_output_dir)
        select_output_dir_button.pack(pady=(0, 10))

        convert_button = tk.Button(self.root, text="Convert to Images", command=self.convert_pdf_to_images)
        convert_button.pack(pady=(20, 10))

        self.thumbnail_canvas.pack(pady=(10, 20))

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.display_pdf_thumbnail()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")

    def display_pdf_thumbnail(self):
        if self.pdf_path:
            try:
                doc = fitz.open(self.pdf_path)
                page = doc[0]
                pix = page.get_pixmap()
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Create thumbnail
                image.thumbnail((300, 400))
                thumbnail_image = ImageTk.PhotoImage(image)
                self.thumbnail_canvas.create_image(150, 200, image=thumbnail_image)
                self.thumbnail_canvas.image = thumbnail_image
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display thumbnail: {e}")

    def convert_pdf_to_images(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap()
                output_path = os.path.join(self.output_dir, f"page_{page_num + 1}.png")
                pix.save(output_path)

            messagebox.showinfo("Success", f"PDF successfully converted to images in {self.output_dir}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    root = tk.Tk()
    root.title("PDF to Image")
    converter = PDFToImageConverter(root)
    root.geometry("400x600")
    root.mainloop()


if __name__ == "__main__":
    main()
