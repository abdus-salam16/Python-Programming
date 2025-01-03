import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import random
import time
import webbrowser
import threading


def wait():
    time.sleep(random.randrange(1, 6))


def open_link(url):
    webbrowser.open(url)


def scrape():
    search_query = entry.get()
    if not search_query:
        messagebox.showerror("Error", "Please enter a search term")
        return

    base_url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="
    URL_input = base_url + search_query
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        output_text.delete(1.0, tk.END)  # Clear previous output

        for page_number in range(0, 10):  # Loop to get multiple pages
            start = page_number * 10
            paginated_url = f"{URL_input}&start={start}"

            page = requests.get(paginated_url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            wait()

            results = soup.find("div", id="gs_res_ccl_mid")
            if not results:
                continue
            job_elements = results.find_all("div", class_="gs_ri")

            for job_element in job_elements:
                title_element = job_element.find("h3", class_="gs_rt").text.strip()
                link_element = job_element.find("h3", class_="gs_rt").find("a")

                # Get the link URL
                if link_element:
                    link_url = link_element["href"]
                else:
                    link_url = "No direct link available"

                ref_element = job_element.find("div", class_="gs_a").text

                # Insert title, link, and references into output_text
                output_text.insert(tk.END, f"Title: {title_element}\n")
                link_start_index = output_text.index(tk.END)
                output_text.insert(tk.END, f"Link: {link_url}\n")
                link_end_index = output_text.index(tk.END)

                # Insert references
                output_text.insert(tk.END, f"References: {ref_element}\n\n")

                # Configure link appearance and add a clickable tag
                output_text.tag_configure('link', foreground="blue", underline=True)
                output_text.tag_add('link', link_start_index, link_end_index)

                # Correctly bind the clickable link with a default argument to capture the link URL
                output_text.tag_bind('link', '<Button-1>', lambda e, url=link_url: open_link(url))

        messagebox.showinfo("Success", "Search Completed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def start_scrape_thread():
    threading.Thread(target=scrape).start()


root = tk.Tk()
root.title("Google Scholar Scraper")

# Input Label
label = tk.Label(root, text="Enter Search Term:")
label.pack(pady=10)

# Entry for search query
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Scrape button
button = tk.Button(root, text="Search", command=start_scrape_thread)  # Start thread on button press
button.pack(pady=20)

# Scrolled Text to display output
output_text = scrolledtext.ScrolledText(root, width=160, height=400, wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()