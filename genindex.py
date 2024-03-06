#!/usr/bin/env python3

import os
import subprocess

from html.parser import HTMLParser


class TitleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.inside_title_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.inside_title_tag = True

    def handle_data(self, data):
        if self.inside_title_tag:
            self.title = data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self.inside_title_tag = False


def extract_html_title(html_file):
    extractor = TitleExtractor()
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()
        extractor.feed(html_content)
    return extractor.title


def get_file_creation_time(filename):
    command = f"git log --format=%aI {filename} | head -n 1"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    creation_time = result.stdout.read().decode().strip()
    return creation_time


def generate_md_list(directory):
    md_files = [
        file
        for file in os.listdir(directory)
        if file.endswith(".md") and file != "index.md"
    ]
    md_files.sort(key=lambda x: get_file_creation_time(x), reverse=True)
    html_list = "<ul>\n"
    c = 0
    for file in md_files:
        html = file.replace(".md", ".html")
        title = extract_html_title(html)
        date = get_file_creation_time(file)
        print(f"{c} - {date} - {file} -  {title}")
        html_list += f'<li>{date[:10]}<a href="{html}">{title}</a></li>\n'
        c += 1
    html_list += "</ul>\n"
    return html_list


def generate_index_md(directory, md_list):
    with open(os.path.join(directory, "index.txt"), "r") as f:
        index_content = f.read()
    updated_content = index_content.replace("BLOGITEMS", md_list)
    with open(os.path.join(directory, "index.md"), "w") as f:
        f.write(updated_content)


if __name__ == "__main__":
    directory = "."
    md_list = generate_md_list(directory)
    generate_index_md(directory, md_list)
