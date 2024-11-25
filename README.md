# qrcode_admin

## Description

This is a simple python script that generates and reads QR codes.
It uses the `qrcode` and `opencv-python` libraries.

## Installation

### Requirements

- Python > 3.9

### Environment setup

1. Create and activate a virtual environment:

   **Linux/macOS:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**

    ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
cd bin
python qrcode_admin.py
```
In the main menu, you can choose between generating a QR code or reading one.

![Menu](data/readme/menu.png)

Example of a generated QR code:
![Test](data/readme/test.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[Neetre](https://github.com/Neetre)
