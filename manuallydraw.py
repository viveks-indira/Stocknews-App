# import time
# import pandas as pd
# from datetime import datetime
# from PIL import Image, ImageDraw, ImageFont
#
#
# class MarketScraper:
#     def __init__(self):
#         self.data = []  # Initialize an empty list for the news items
#         self.df = pd.DataFrame()  # Initialize an empty DataFrame
#
#     def fetch_news_data(self):
#         # Your provided news data
#         self.data = [
#             {"title": "Grasim Industries", "body": "The board approved a fund raise of Rs 4,000 crore via rights issue to fund capex and repay debt."},
#             {"title": "Gujarat Mineral Development Corporation", "body": "GMDC presented a Rs 269.44 crore dividend cheque to the Gujarat government, which holds 74% of the company."},
#             {"title": "Bombay Dyeing", "body": "The company has received consideration of about Rs 4,675 crore towards Phased, located at Worli, Mumbai, after signing a conveyance deed with a subsidiary of Sumitomo Realty. The proceeds realised will be used for repaying loans, and the balance will be invested in approved securities for future developments."},
#             {"title": "Jio Financial Services", "body": "The company named AR Ganesh as group Chief Technology Officer w.e.f. Oct. 16."},
#             {"title": "Mphasis", "body": "Ayaskant Sarangi is the new Chief Human Resource Officer (CHRO) as of Oct. 16. Srikanth Karra will remain in the Chief Administrative Officer role (CAO) to assist with the transition and superannuate from the company on April 29, 2024."},
#             {"title": "NLC India", "body": "The company incorporated a new wholly owned subsidiary, 'NLC India Green Energy’ (NIGEL), which currently undertakes projects of 2 GW of renewable energy."},
#             {"title": "Data Patterns", "body": "The company announced a licencing and transfer of technology (ToT) agreement with IN-SPACe, an autonomous agency in the Department of Space. This agreement will provide data patterns with miniature SAR radar capability."},
#             {"title": "Uttam Sugar Mills", "body": "The Board redeemed 1,38,850 (6.50%) and 1,80,575 (10%) non-cumulative redeemable preference shares."},
#             {"title": "Electronics Mart India", "body": "The company has commenced the commercial operation of a new multi-brand store under the brand name ‘BAJAJ ELECTRONICS’ on Oct. 15 in Andhra Pradesh."},
#             {"title": "JK Paper", "body": "The Board approved the acquisition of Manipal Utility Packaging Solutions Pvt. (MUPSPL), which is engaged in the business of manufacturing packaging products with a revenue of Rs 147.77 crore in FY23."},
#             {"title": "ICICI Securities", "body": "The board approved the payment of an interim dividend of Rs 12 per equity share with a face value of Rs 5 each. The record date is set for Oct. 27, 2023."},
#             {"title": "Varun Beverages", "body": "The board approved the acquisition of 5.03% of the paid-up capital of the manufacturing subsidiary for Rs 10 crore, Lunarmech Technologies. Post-acquisition, Varun Beverages will hold a 60.07% stake in the company. It also approved an investment of Rs 1.92 crore for a 9.80% stake in Isharays Energy Two, a special-purpose vehicle by Sunsource Energy to supply solar power in Uttar Pradesh."},
#             {"title": "Piramal Pharma", "body": "The company announced the launch of a high-throughput screening facility that augments the existing in-vitro biology capabilities at its drug discovery services site in Ahmedabad, India."},
#             {"title": "KEC International", "body": "The company bagged new orders worth Rs 1,315 crores in its transmission and cable business."},
#             {"title": "Coal India", "body": "The company expects to exceed its demand projection of 610 MT of supply to the country’s power plant for FY24 after supplies to thermal power plants shot up by close to 6% to. 23.5 million MT during the first fortnight of October 2023."},
#             {"title": "Lemon Tree Hotels", "body": "The company signed an agreement for a 55-room property in Dehradun, Uttarakhand, under the brand 'Keys Prime by Lemon Tree Hotels' and is expected to be operational by FY 2027."},
#             {"title": "Lupin", "body": "The company signed a business transfer agreement with the unit to carve out two API manufacturing sites."},
#             {"title": "Tata Power", "body": "The company signed a power distribution agreement with Endurance Technologies for setting up a 12.5 MW solar plant."},
#             {"title": "Som Distilleries", "body": "The breweries will manufacture Indian-made foreign liquor in Jammu and Kashmir."},
#             {"title": "Voltas", "body": "The company will consider debenture issues at the Oct. 19 board meeting."}
#         ]
#         self.create_dataframe()
#
#     def create_dataframe(self):
#         # Create DataFrame from the news data
#         self.df = pd.DataFrame(self.data)
#
#     def draw_wrapped_text_on_image(self, image_path, font_path="arial.ttf", max_images=2, line_spacing=5):
#         df = self.df
#         df['body'] = df['body'].str.strip().str.replace(r'\s+', ' ', regex=True)
#
#         # Set the margins
#         top_margin = 380
#         bottom_margin = 150
#         left_margin = 50
#         right_margin = 150
#
#         # Page Area length and width to be text print
#         image_counter = 1
#         image_paths = []  # List to hold image paths
#         image = Image.open(image_path)
#         image_width, image_height = image.size
#         drawable_width = image_width - left_margin - right_margin + 100
#         drawable_height = image_height - top_margin - bottom_margin + 350
#
#         y_offset = top_margin
#         # Get current date
#         current_date = datetime.now().strftime("%B %d, %Y")  # Format the date as needed
#         date_position = (750, 280)  # Position for the date
#
#         # Font settings
#         try:
#             title_font = ImageFont.truetype("arialbd.ttf", 24)  # Title font
#             body_font = ImageFont.truetype(font_path, 22)  # Body font
#             date_font = ImageFont.truetype(font_path, 22)  # Date font
#         except IOError:
#             title_font = ImageFont.load_default()
#             body_font = ImageFont.load_default()
#             date_font = ImageFont.load_default()
#
#         draw = ImageDraw.Draw(image)
#         # Draw the date at the start of the image
#         draw.text(date_position, current_date, font=date_font, fill="white", weight="5")  # Draw date
#
#         print("Starting to draw text on the image...")
#
#
#         # Iterate through the DataFrame and draw text across images
#         for index, row in df.iterrows():
#             title = row['title']
#             body = row['body']
#
#             # Draw title without justification (left-aligned)
#             y_offset = self.draw_text(draw, title, (left_margin, y_offset), title_font, drawable_width, "title",line_spacing)
#             y_offset += line_spacing  # Add space after title
#
#             y_offset += 10
#             # Draw body with justification
#             y_offset = self.draw_text_justified(draw, body, (left_margin, y_offset), body_font, drawable_width)
#
#             # Draw separator line
#             y_offset += 10  # Add space before separator line
#             # Draw a horizontal line
#             draw.line([(left_margin, y_offset), (drawable_width + left_margin, y_offset)], fill="black", width=1)
#             y_offset += 15  # Add space after the line
#
#             # Check if we need to create a new image
#             if y_offset > drawable_height:
#                 image.save(f"E:\Stock News\StockDailyNewsTest\output_image_{image_counter}.jpg")
#                 image_paths.append(f"E:\Stock News\StockDailyNewsTest\output_image_{image_counter}.jpg")  # Add the image path to the list
#                 print(f"Image {image_counter} created successfully!")
#                 image_counter += 1
#                 if image_counter > max_images:  # Stop after the specified max number of images
#                     break
#                 image = Image.open(image_path)  # Reload image for the next page
#                 y_offset = top_margin  # Reset y_offset for new image
#
#         # Save the final image if there's remaining content
#         if y_offset > top_margin:
#             image.save(f"E:\Stock News\StockDailyNewsTest\outputnews_image{image_counter}.jpg")
#             image_paths.append(f"E:\Stock News\StockDailyNewsTest\output_image_{image_counter}.jpg")
#             print(f"Final Image {image_counter} created successfully!")
#
#         return image_paths  # Return the list of image paths
#
#     def draw_text(self, draw, text, position, font, max_width, text_type,line_spacing):
#         """Draw left-aligned text on the image and return the updated y-offset."""
#         x, y = position
#         lines = []
#         words = text.split()
#         current_line = ""
#
#         # Define color based on text type
#         color = "black"  # Default color for body text
#         if text_type == "title":
#             color = (37, 164, 138)  # Greenish color for title
#             font = font  # Use the title font
#
#         # Split text into lines that fit within the drawable width
#         for word in words:
#             test_line = current_line + word + " "
#             test_line_width = draw.textlength(test_line, font=font)
#
#             if test_line_width <= max_width:
#                 current_line = test_line
#             else:
#                 lines.append(current_line.strip())
#                 current_line = word + " "
#
#         if current_line:
#             lines.append(current_line.strip())
#
#         # Draw each line
#         for line in lines:
#             draw.text((x, y), line, font=font, fill=color)
#             line_bbox = draw.textbbox((x, y), line, font=font)
#             line_height = line_bbox[3] - line_bbox[1]
#             y += line_height + line_spacing
#
#         return y  # Return updated y position
#
#     def draw_text_justified(self, draw, text, position, font, max_width):
#         """Draw justified text on the image, handling the last line as start-aligned (left-aligned)."""
#         x, y = position
#         words = text.replace('\n', ' ').split()  # Replace newlines with spaces and split into words
#         lines = []
#         current_line = []
#         current_line_width = 0
#
#         # Split text into lines that fit within the drawable width
#         for word in words:
#             word_width = draw.textlength(word + " ", font=font)
#             if current_line_width + word_width <= max_width:
#                 current_line.append(word)
#                 current_line_width += word_width
#             else:
#                 lines.append((current_line, current_line_width))
#                 current_line = [word]
#                 current_line_width = word_width
#
#         if current_line:
#             lines.append((current_line, current_line_width))
#
#         # Draw each line with proper justification
#         for i, (line, line_width) in enumerate(lines):
#             # If this is the last line or the line has only one word, left-align it
#             if i == len(lines) - 1 or len(line) == 1:
#                 # Left-align the text (start-aligned)
#                 draw.text((x, y), " ".join(line), font=font, fill="black")
#             else:
#                 # Justify the text (distribute space between words)
#                 total_spaces = len(line) - 1
#                 space_width = (max_width - line_width) / total_spaces if total_spaces > 0 else 0
#                 x_offset = x
#                 for word in line:
#                     draw.text((x_offset, y), word, font=font, fill="black")
#                     word_width = draw.textlength(word + " ", font=font)
#                     x_offset += word_width + space_width
#
#             line_bbox = draw.textbbox((x, y), " ".join(line), font=font)
#             line_height = line_bbox[3] - line_bbox[1]
#             y += line_height + 5  # Add line spacing
#
#         return y  # Return updated y position
#
# if __name__ == "__main__":
#     scraper = MarketScraper()
#     scraper.fetch_news_data()  # Fetch the news data
#     image_paths = scraper.draw_wrapped_text_on_image(r"E:\Stock News\StockDailyNewsTest\sample_background_news.jpeg")  # Provide the path to your image
#     print("Images created:", image_paths)

import time
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


class MarketScraper:
    def __init__(self):
        self.data = []  # Initialize an empty list for the news items
        self.df = pd.DataFrame()  # Initialize an empty DataFrame

    def fetch_news_data(self):
        # Your provided news data
        self.data = [
            {"title": "Grasim Industries", "body": "The board approved a fund raise of Rs 4,000 crore via rights issue to fund capex and repay debt."},
            {"title": "Gujarat Mineral Development Corporation", "body": "GMDC presented a Rs 269.44 crore dividend cheque to the Gujarat government, which holds 74% of the company."},
            {"title": "Bombay Dyeing", "body": "The company has received consideration of about Rs 4,675 crore towards Phased, located at Worli, Mumbai, after signing a conveyance deed with a subsidiary of Sumitomo Realty. The proceeds realised will be used for repaying loans, and the balance will be invested in approved securities for future developments."},
            {"title": "Jio Financial Services", "body": "The company named AR Ganesh as group Chief Technology Officer w.e.f. Oct. 16."},
            {"title": "Mphasis", "body": "Ayaskant Sarangi is the new Chief Human Resource Officer (CHRO) as of Oct. 16. Srikanth Karra will remain in the Chief Administrative Officer role (CAO) to assist with the transition and superannuate from the company on April 29, 2024."},
            {"title": "NLC India", "body": "The company incorporated a new wholly owned subsidiary, 'NLC India Green Energy’ (NIGEL), which currently undertakes projects of 2 GW of renewable energy."},
            {"title": "Data Patterns", "body": "The company announced a licencing and transfer of technology (ToT) agreement with IN-SPACe, an autonomous agency in the Department of Space. This agreement will provide data patterns with miniature SAR radar capability."},
            {"title": "Uttam Sugar Mills", "body": "The Board redeemed 1,38,850 (6.50%) and 1,80,575 (10%) non-cumulative redeemable preference shares."},
            {"title": "Electronics Mart India", "body": "The company has commenced the commercial operation of a new multi-brand store under the brand name ‘BAJAJ ELECTRONICS’ on Oct. 15 in Andhra Pradesh."},
            {"title": "JK Paper", "body": "The Board approved the acquisition of Manipal Utility Packaging Solutions Pvt. (MUPSPL), which is engaged in the business of manufacturing packaging products with a revenue of Rs 147.77 crore in FY23."},
            {"title": "ICICI Securities", "body": "The board approved the payment of an interim dividend of Rs 12 per equity share with a face value of Rs 5 each. The record date is set for Oct. 27, 2023."},
            {"title": "Varun Beverages", "body": "The board approved the acquisition of 5.03% of the paid-up capital of the manufacturing subsidiary for Rs 10 crore, Lunarmech Technologies. Post-acquisition, Varun Beverages will hold a 60.07% stake in the company. It also approved an investment of Rs 1.92 crore for a 9.80% stake in Isharays Energy Two, a special-purpose vehicle by Sunsource Energy to supply solar power in Uttar Pradesh."},
            {"title": "Piramal Pharma", "body": "The company announced the launch of a high-throughput screening facility that augments the existing in-vitro biology capabilities at its drug discovery services site in Ahmedabad, India."},
            {"title": "KEC International", "body": "The company bagged new orders worth Rs 1,315 crores in its transmission and cable business."},
            {"title": "Coal India", "body": "The company expects to exceed its demand projection of 610 MT of supply to the country’s power plant for FY24 after supplies to thermal power plants shot up by close to 6% to. 23.5 million MT during the first fortnight of October 2023."},
            {"title": "Lemon Tree Hotels", "body": "The company signed an agreement for a 55-room property in Dehradun, Uttarakhand, under the brand 'Keys Prime by Lemon Tree Hotels' and is expected to be operational by FY 2027."},
            {"title": "Lupin", "body": "The company signed a business transfer agreement with the unit to carve out two API manufacturing sites."},
            {"title": "Tata Power", "body": "The company signed a power distribution agreement with Endurance Technologies for setting up a 12.5 MW solar plant."},
            {"title": "Som Distilleries", "body": "The breweries will manufacture Indian-made foreign liquor in Jammu and Kashmir."},
            {"title": "Voltas", "body": "The company will consider debenture issues at the Oct. 19 board meeting."}
        ]
        self.create_dataframe()

    def create_dataframe(self):
        # Create DataFrame from the news data
        self.df = pd.DataFrame(self.data)

    def draw_wrapped_text_on_image(self, image_path, font_path="arial.ttf", max_images=3, line_spacing=5):
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

                image.save(f"E:\Stock News\StockNews App - Copy\static\images\output_{image_counter}.jpg")
                image_paths.append(
                    f"E:\Stock News\StockNews App - Copy\static\images\output_{image_counter}.jpg")  # Add the image path to the list
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
            final_image_path = f"E:\Stock News\StockNews App - Copy\static\images\output_{image_counter}.jpg"
            image.save(final_image_path)
            image_paths.append(final_image_path)  # Add the last image path to the list
            print(f"Image {image_counter} created successfully!")

        return image_paths  # Return the list of image paths


if __name__ == "__main__":
    scraper = MarketScraper()
    scraper.fetch_news_data()
    image_path =r"E:\Stock News\StockNews App\sample_background_news.jpeg"  # Path to your background image
    scraper.draw_wrapped_text_on_image(image_path)
