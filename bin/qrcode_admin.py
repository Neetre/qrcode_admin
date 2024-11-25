import qrcode
import qrcode.constants
import cv2 as cv
import os
from datetime import datetime
import logging


logging.basicConfig(
    filename="../log/receipts.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class QRCodeTool:
    def __init__(self, output_dir="../data/qr_codes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_qr(self, data, filename=None):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"qr_code_{timestamp}.png"
            elif not filename.endswith(".png"):
                filename += ".png"

            file_path = os.path.join(self.output_dir, filename)
            qr_image.save(file_path)
            return file_path
        except Exception as e:
            print(f"Error generating QR code: {str(e)}")
            return None
        
    def read_qr(self, image_path):
        try:
            image = cv.imread(image_path)

            if image is None:
                raise ValueError("Could not read the image file")

            qr_detector = cv.QRCodeDetector()

            data, bbox, straight_qrcode = qr_detector.detectAndDecode(image)

            if bbox is not None:
                print("QR Code successfully read!")
                return data
            else:
                print("No QR Code found in the image!")
                return None
        except Exception as e:
            print(f"Error reading QR code: {str(e)}")
            return None


def main():
    qr_tool = QRCodeTool()

    while True:
        print("\nQR Code Tool Menu:")
        print("1. Generate QR Code")
        print("2. Read QR Code")
        print("3. Exit")

        choice = int(input("Enter your choice (1-3) ---> "))

        if choice == 1:
            data = input("Enter the data for the QR Code ---> ")
            filename = input("Enter filename (optional, press Enter to skip) ---> ")
            filename = filename if filename else None
            qr_tool.generate_qr(data, filename)
            print("QR Code generated!")
        
        elif choice == 2:
            image_path = input("Enter the path to the QR Code image ---> ")
            data = qr_tool.read_qr(image_path)
            if data:
                print(f"Decoded data: {data}")
        
        elif choice == 3:
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again...")
    return


if __name__ == "__main__":
    main()
