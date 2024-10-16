import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pywhatkit as kit
from PIL import Image, ImageDraw, ImageFont

class MarketScraper:

    def __init__(self):
        self.url = self.construct_url()  # Construct URL during initialization
        self.soup = None
        self.data = []
        self.df = pd.DataFrame()  # Initialize an empty DataFrame
        self.fallback_number = "+919630177986"

        # def construct_url(self):
    #     today = datetime.now()
    #     # Get the first three characters of the current month in lowercase
    #     month = today.strftime("%B")[:3].lower()
    #     formatted_date = f"{month}-{today.day}"
    #     print(f"Formatted Date: {formatted_date}")
    #
    #     # Primary URL based on the current date
    #     url = f"https://www.ndtvprofit.com/markets/stock-market-today-all-you-need-to-know-going-into-trade-on-{formatted_date}"
    #     fallback_url = f"https://www.ndtvprofit.com/markets/stock-market-update-{formatted_date}-us-earnings-release-and-india-market-slump?src=p1"
    #
    #     try:
    #         # Send a request to check if the URL exists
    #         response = requests.get(url)
    #         # Raise an error for non-successful status codes (e.g., 404)
    #         response.raise_for_status()
    #         print(f"URL Found: {url}")
    #     except requests.exceptions.RequestException as e:
    #         # In case of any error, use the fallback URL
    #         print(f"Primary URL not found, using fallback URL: {fallback_url}")
    #         url = fallback_url
    #
    #     return url
    def construct_url(self):
        today = datetime.now()
        month = today.strftime("%B")[:3].lower()
        formatted_date = f"{month}-{today.day}"
        print(f"Formatted Date: {formatted_date}")

        url = f"https://www.ndtvprofit.com/markets/stock-market-update-oct-15-s-p-500-nasdaq-composite-earnings-reliance-industries-hcl-technologies"
        fallback_url = f"https://www.ndtvprofit.com/markets/stock-market-update-oct-8-us-earnings-release-and-india-market-slump?src=p1"
        fallback_url_1 =f" https://www.ndtvprofit.com/markets/stock-market-today-all-you-need-to-know-going-into-trade-on-oct-14-2?src=p1"

        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"URL Found: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Primary URL not found, using fallback URL: {fallback_url}")
            try:
                response = requests.get(fallback_url)
                response.raise_for_status()
                print(f"Fallback URL found: {fallback_url}")
                url = fallback_url
            except requests.exceptions.RequestException as e:
                print("Both URLs not found. Sending notification...")
                self.send_whatsapp_error_message("Stock news Both URL not found", url, fallback_url)
                raise Exception("Both URLs not found, notifications sent.")

        return url

    def fetch_html(self):
        time.sleep(5)  # Pause to prevent overwhelming the server
        response = requests.get(self.url)

        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve data from {self.url}, Status Code: {response.status_code}")

    def parse_html(self):
        if not self.soup:
            raise Exception("HTML content not fetched. Call fetch_html() first.")

        # Fetch 'Stocks To Watch' section
        heading = self.soup.find('h2', string="Stocks To Watch")
        if not heading:
            raise Exception("'Stocks To Watch' section not found.")

        ul_element = heading.find_next('ul')
        if not ul_element:
            raise Exception("No 'ul' found after the 'Stocks To Watch' heading.")

        li_elements = ul_element.find_all('li')
        for li in li_elements:
            stock_name = li.find('strong').get_text() if li.find('strong') else "Unknown Stock"
            stock_info = li.get_text(separator="\n").strip()
            self.data.append({
                'title': stock_name.strip(),
                'body': stock_info.replace(stock_name, "").strip()
            })

        # Print the parsed data to check if it's correctly fetched
        #print("Parsed data:", self.data)

    def create_dataframe(self):
        # Convert the scraped data into a DataFrame
        self.df = pd.DataFrame(self.data)
        print("DataFrame created:", self.df)
        return self.df

    def format_json(self):
        # Format the news data into a readable string format
        formatted_text = ""
        for index, row in self.df.iterrows():
            formatted_text += f"{row['title']}: {row['body']}\n\n"
        return formatted_text.strip()

    def send_whatsapp_error_message(self, message, url1, url2):
        phone_number = "+919630177986"
        print("inside error")
        """Send an error message with two URLs through WhatsApp."""
        current_date = datetime.now().strftime("%B %d, %Y")

        complete_message = (
            f"{current_date} - {message}\n"
            f"Primary URL: {url1}\n"
            f"Fallback URL: {url2}"
        )

        # Extracting hours and minutes for sending the message
        hour = datetime.now().hour
        minute = datetime.now().minute + 2  # Add a couple of minutes to ensure the message sends

        try:
            # Sending message via WhatsApp using pywhatkit
            kit.sendwhatmsg(
                phone_number,
                f"Stock News Image Generation Failed: {complete_message}",
                hour,
                minute,
                wait_time=15  # Wait time before sending the message
            )
            print("Message Sent!")  # Prints success message in console
            time.sleep(15)  # Sleep for a while to avoid any issues after sending

        except Exception as e:
            print("Error in sending the message:", e)  # Print the exception message

    def send_whatsapp_message(self, phone_number, message, image_paths=None):
        # Send images through WhatsApp along with a message
        current_date = datetime.now().strftime("%B %d, %Y")  # Format the date as needed

        if image_paths:
            print(f"Sending {len(image_paths)} images to {phone_number}...")

            for index, image_path in enumerate(image_paths):
                try:
                    kit.sendwhats_image(
                        phone_number,
                        image_path,
                        f"{current_date} Market Update {index + 1}/{len(image_paths)}",
                        wait_time=15  # Increase wait time for better reliability
                    )
                    time.sleep(15)  # Ensure a delay between image sends
                    print(f"Image {index + 1} sent to {phone_number}: {image_path}")
                except Exception as e:
                    print(f"Failed to send image {image_path}: {e}")
        else:
            print("No images to send.")

    def draw_wrapped_text_on_image(self, image_path, font_path="arial.ttf", max_images=2, line_spacing=5):
        df = self.df
        df['body'] = df['body'].str.strip().str.replace(r'\s+', ' ', regex=True)

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

                image.save(f"E:\Stock News\StocksDailyNewsImage\stocknews_{image_counter}.jpg")
                image_paths.append(
                    f"E:\Stock News\StocksDailyNewsImage\stocknews_{image_counter}.jpg")  # Add the image path to the list
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
            final_image_path = f"E:\Stock News\StocksDailyNewsImage\stocknews_{image_counter}.jpg"
            image.save(final_image_path)
            image_paths.append(final_image_path)  # Add the last image path to the list
            print(f"Image {image_counter} created successfully!")

        return image_paths  # Return the list of image paths

    def scrape(self):
        self.fetch_html()
        self.parse_html()
        self.create_dataframe()
        formatted_text = self.format_json()
        print(formatted_text)

        # Draw the images and get their paths
        image_paths = self.draw_wrapped_text_on_image(
            r"E:\Stock News\StocksDailyNewsImage\sample_background_news.jpeg")

        print("Image paths:", image_paths)
        # You can specify the phone number where you want to send the images
        phone_number = "+919630177986"  # Replace with your number
        #self.send_whatsapp_message(phone_number, formatted_text, image_paths)


if __name__ == "__main__":
    scraper = MarketScraper()
    scraper.scrape()
