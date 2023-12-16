import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from docx import Document

def save_document(doc, folder_path, file_name):
    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construct the full path for the document
    doc_path = os.path.join(folder_path, file_name)

    # Save the document to the specified path
    doc.save(doc_path)
course_urls = [
    "https://dentistup.tn/courses/interception-en-omni-pratique",
    "https://dentistup.tn/courses/implantation-immediate",
    "https://dentistup.tn/courses/la-piezographie-mandibulaire",
    "https://dentistup.tn/courses/prothese-sur-implants",
    "https://dentistup.tn/courses/new-la-chirurgie-de-pose-dimplant",
]
cleaned_course_names = []
for docx_file in course_urls:
        course_name = docx_file.split('/')[-1].replace('-', ' ')
        pattern = r'[^a-zA-Z]'
        course_name = course_name.lower()
        course_name = re.sub(pattern, ' ', course_name)
        cleaned_course_names.append(course_name)
chrome_driver_path = "chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
i=0
for index, course_url in enumerate(course_urls):

    driver.get(course_url)
    time.sleep(3)
    div_elements = driver.find_elements(By.CLASS_NAME, "elementor-element")
    course_content = ""
    for div_element in div_elements:
        if "elementor-widget-text-editor" in div_element.get_attribute("class"):
            course_content += div_element.text.strip() + "\n" + "=" * 30 + "\n"
    doc = Document()
    doc.add_paragraph(course_content)
    doc_path = f"plus_dinforamtion_{course_url.split('/')[-1]}.docx"
    folder_path=f"courses//{cleaned_course_names[i]}"
    save_document(doc, folder_path, doc_path)
    print(f"Saved content from '{course_url}' to '{doc_path}'")
    i += 1

driver.quit()
