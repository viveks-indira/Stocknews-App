# final
from datetime import datetime
from flask import Flask, render_template, request
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw ,ImageFont
import re
import pandas as pd
import time

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\freedom\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Route for rendering the HTML page
@app.route('/')
def index():
    return render_template('upload.html')

# Function to preprocess the image for better OCR results
def preprocess_image(image):
    # Convert to grayscale
    image = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # You can adjust the factor as needed
    # Apply a filter (optional)
    image = image.filter(ImageFilter.SHARPEN)
    return image

# # Function to extract titles and paragraphs from the OCR text
# def parse_news(text):
#     # Updated regex pattern for identifying titles followed by paragraphs
#     news_pattern = re.compile(r'([A-Za-z0-9 @.]+): (.+?)(?=\n[A-Za-z0-9 @.]+:|\Z)', re.DOTALL)
#     matches = news_pattern.findall(text)
#
#     news = []
#     for match in matches:
#         title = match[0].strip()
#         paragraph = match[1].strip().replace('\n', ' ')
#         news.append({"title": title, "paragraph": paragraph})
#
#     return news
# Function to extract titles and paragraphs from the OCR text
def parse_news(text):
    # Updated regex pattern for identifying titles followed by paragraphs
    news_pattern = re.compile(r'([A-Za-z0-9 .@]+):\s*(.+?)(?=\s*(?:@|[A-Za-z0-9 .]+:|\Z))', re.DOTALL)
    matches = news_pattern.findall(text)

    news = []
    for match in matches:
        title = match[0].strip().replace('@', '')  # Remove @ from title
        paragraph = match[1].strip().replace('\n', ' ')
        news.append({"title": title, "paragraph": paragraph})
    return news


# Route for file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'documents' not in request.files:
        return render_template('upload.html', error_msg='No files uploaded')

    files = request.files.getlist('documents')
    if not files:
        return render_template('upload.html', error_msg='No files selected')

    all_news = []

    # Process each image file using Tesseract OCR
    try:
        for file in files:
            if file.filename == '':
                continue  # Skip empty filenames

            image = Image.open(file.stream)
            image = preprocess_image(image)  # Preprocess the image
            extracted_text = pytesseract.image_to_string(image)

            # Print the raw extracted text to the console for debugging
            print("Extracted Text:", extracted_text)

            # Parse the extracted text for news titles and paragraphs
            news = parse_news(extracted_text)

            # Print the fetched news to the console for debugging
            print("Fetched News:", news)

            all_news.extend(news)  # Add news from this file to the list

        if not all_news:
            return render_template('upload.html', error_msg='No valid news found in the images')
        image_path = r"E:\Stock News\StockNews App\sample_background_news.jpeg"
        draw_wrapped_text_on_image(all_news, image_path)  # Use a background image path here

        # Render the page with the extracted news
        return render_template('upload.html', news=all_news)
    except Exception as e:
        return render_template('upload.html', error_msg=f'Error processing files: {str(e)}')


def draw_wrapped_text_on_image(news_data, image_path, font_path="arial.ttf", max_images=2, line_spacing=5):

    # df = self.df
    # df['body'] = df['body'].str.strip().str.replace(r'\s+', ' ', regex=True)

    df = pd.DataFrame(news_data)  # Assuming news_data is a list of dicts
    print(df)
    df['body'] = df['paragraph'].str.strip().str.replace(r'\s+', ' ', regex=True)

    # Set the margins
    top_margin = 380  # Increased top margin for better readability
    bottom_margin = 150  # Increased bottom margin to prevent overflow
    left_margin = 50  # Left margin adjusted
    right_margin = 150  # Right margin adjusted

    # Page Area length and width to be text print
    image_counter = 1
    image_paths = []  # List to hold image paths
    image = Image.open(image_path)
    image_width, image_height = image.size
    drawable_width = image_width - left_margin - right_margin + 100
    drawable_height = image_height - top_margin - bottom_margin + 350

    y_offset = top_margin

    # Get current date
    current_date = datetime.now().strftime("%B %d, %Y")  # Format the date as needed
    date_position = (750, 280)  # Position for the date

    # Font settings (use your desired font and size)
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 24)  # Title font
        body_font = ImageFont.truetype(font_path, 22)  # Body font
        date_font = ImageFont.truetype(font_path, 22)  # Date font
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        date_font = ImageFont.load_default()

    def draw_text(draw, text, position, font, max_width, text_type):
        """Draw left-aligned text on the image and return the updated y-offset."""
        x, y = position
        lines = []
        words = text.split()
        current_line = ""

        # Define color based on text type
        color = "black"  # Default color for body text
        if text_type == "title":
            color = (37, 164, 138)  # Greenish color for title
            font = title_font  # Use the title font
        else:
            font = body_font  # Use the body font

        # Split text into lines that fit within the drawable width
        for word in words:
            test_line = current_line + word + " "
            test_line_width = draw.textlength(test_line, font=font)

            if test_line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        # Draw each line
        for line in lines:
            draw.text((x, y), line, font=font, fill=color)
            line_bbox = draw.textbbox((x, y), line, font=font)
            line_height = line_bbox[3] - line_bbox[1]
            y += line_height + line_spacing

        return y  # Return updated y position

    # Function to draw justified text for the body with special handling for the last line
    def draw_text_justified(draw, text, position, font, max_width):
        """Draw justified text on the image, handling the last line as start-aligned (left-aligned)."""
        x, y = position
        words = text.replace('\n', ' ').split()  # Replace newlines with spaces and split into words
        lines = []
        current_line = []
        current_line_width = 0

        # Split text into lines that fit within the drawable width
        for word in words:
            word_width = draw.textlength(word + " ", font=font)
            if current_line_width + word_width <= max_width:
                current_line.append(word)
                current_line_width += word_width
            else:
                lines.append((current_line, current_line_width))
                current_line = [word]
                current_line_width = word_width

        if current_line:
            lines.append((current_line, current_line_width))

        # Draw each line with proper justification
        for i, (line, line_width) in enumerate(lines):
            # If this is the last line or the line has only one word, left-align it
            if i == len(lines) - 1 or len(line) == 1:
                # Left-align the text (start-aligned)
                draw.text((x, y), " ".join(line), font=font, fill="black")
            else:
                # Justify the text (distribute space between words)
                total_spaces = len(line) - 1
                space_width = (max_width - line_width) / total_spaces if total_spaces > 0 else 0
                x_offset = x
                for word in line:
                    draw.text((x_offset, y), word, font=font, fill="black")
                    word_width = draw.textlength(word + " ", font=font)
                    x_offset += word_width + space_width

            line_bbox = draw.textbbox((x, y), " ".join(line), font=font)
            line_height = line_bbox[3] - line_bbox[1]
            y += line_height + line_spacing

        return y  # Return updated y position

    draw = ImageDraw.Draw(image)

    # Draw the date at the start of the image
    draw.text(date_position, current_date, font=date_font, fill="white", weight="5")  # Draw date

    print("Starting to draw text on the image...")
    # Iterate through the DataFrame and draw text across images
    for index, row in df.iterrows():
        title = row['title']
        body = row['body']

        # Draw title without justification (left-aligned)
        y_offset = draw_text(draw, title, (left_margin, y_offset), title_font, drawable_width, "title")
        y_offset += line_spacing  # Add space after title

        # Draw body with justification
        y_offset = draw_text_justified(draw, body, (left_margin, y_offset), body_font,
                                       drawable_width)  # Pass body to justified method

        # Draw separator line
        y_offset += 10  # Add space before separator line
        draw.line([(left_margin, y_offset), (drawable_width + left_margin, y_offset)], fill="black", width=1)
        y_offset += 15  # Add space after the line

        # Check if we need to create a new image
        if y_offset > drawable_height:
            # Draw the date before saving the image
            draw.text(date_position, current_date, font=date_font, fill="white", weight="5")  # Draw date

            image.save(f"E:\Stock News\StockNews App\stocknews_{image_counter}.jpg")
            image_paths.append(
                f"E:\Stock News\StockNews App\stocknews_{image_counter}.jpg")  # Add the image path to the list
            print(f"Image {image_counter} created successfully!")
            image_counter += 1
            if image_counter > max_images:  # Stop after the specified max number of images
                break
            image = Image.open(image_path)  # Start a new image
            draw = ImageDraw.Draw(image)
            y_offset = top_margin  # Reset the y_offset for the new image

            # Draw the date on the new image
            draw.text(date_position, current_date, font=date_font, fill="white",
                      weight="5")  # Draw date on the new image

    # Draw the date on the last image if it hasn't been saved
    if image_counter <= max_images:
        draw.text(date_position, current_date, font=date_font, fill="white", weight="5")  # Draw date
        final_image_path = f"E:\Stock News\StockNews App\stocknews_{image_counter}.jpg"
        image.save(final_image_path)
        image_paths.append(final_image_path)  # Add the last image path to the list
        print(f"Image {image_counter} created successfully!")

    return image_paths  # Return the list of image paths

if __name__ == '__main__':
    app.run(debug=True)
