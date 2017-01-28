from io import BytesIO
import random
import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_courses_list():
    courses_list = []
    base_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    base_url_content = requests.get(base_url)
    xml_content = base_url_content.content.translate(None, b'\n')
    content_of_parse = etree.iterparse(BytesIO(xml_content))
    for action, elem in content_of_parse:
        if elem.text != ' ' and elem.text is not None:
             courses_list.append(elem.text)
    return courses_list          


def get_20_randomly_courses(list_of_courses):
    number_of_courses = 20
    randomly_selected_courses = random.sample(courses_list, number_of_courses)
    return randomly_selected_courses


def get_course_info(selected_courses):
    courses_info = []
    for course in randomly_selected_courses:
        course_page = requests.get(course)   
        soup = BeautifulSoup(course_page.content)
        name = soup.find('div', class_ = "course-title")
        date = soup.find('div', class_ = "startdate")
        language = soup.find('div', class_ = "language-info")
        rating = soup.find('div', class_ = "ratings-text bt3-visible-xs")
        courses_info.append([course,
                             name.text,
                             date.text if date else 'No',
                             language.text if language else 'No',
                             rating.text if rating else 'No'
                            ])
    return courses_info


def output_courses_info_to_xlsx(filepath, courses_info):
    book = Workbook()
    sheet = book.active
    sheet.append(['URL', 'Title', 'Start date', 'Language', 'Rating'])
    for course in courses_info:
        sheet.append(course)
    book.save('{}/courses.xlsx'.format(filepath))


if __name__ == '__main__':
    print('Please wait')
    courses_list = get_courses_list()
    randomly_selected_courses = get_20_randomly_courses(courses_list)
    list_of_courses_info = get_course_info(randomly_selected_courses)
    folder_filepath = input('Enter the path to the folder where you want to save the file xlsx:\n')
    output_courses_info_to_xlsx(folder_filepath, list_of_courses_info)
    print('Saved')
