import argparse
import requests
import re
import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor


def createcsv(path, content, m):
    with open(path, m, newline="") as csvfile:
        csvfile_write = csv.writer(csvfile)
        csvfile_write.writerow(content)


def linkopener(link):
    temp_list = []
    url_status = []

    # pattern for 1 - extracting links and content from anchor tag and 2 - URL validation
    link_content_pattern = r'<a href="(.*?)".*>(.*)</a>'
    url_validation_pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9(" \
                             r")@:%_\+.~#?&//=]*)"
    print(f"fetching all anchor links and content from {link}....")

    # collecting all anchor tag(s) links and contents after validating the url
    try:
        if re.match(url_validation_pattern, link):
            req = requests.get(link)
            req.raise_for_status()
            result = re.findall(link_content_pattern, req.text)
            temp_list.extend(result)
            url_status = [link, req.status_code]
        else:
            print(f"failed: {link} is not a valid url")
            url_status = [link, "invalid url"]
    except requests.exceptions.RequestException as e:
        print(e)
    return temp_list, url_status


def commonlinkfinder(master_list, path):
    temp_dict = {}
    for link in master_list:
        if temp_dict.get(link[1]):
            temp_dict[link[1]][1] += 1
            if temp_dict[link[1]][0] != link[0]:
                temp_dict[link[1]][0] += "\n"+link[0]
        else:
            temp_dict[link[1]] = [link[0], 1]

    for key, value in temp_dict.items():
        createcsv(
                    path,
                    [value[0], key, value[1]],
                    "a"
                 )


if __name__ == "__main__":
    master_list = []

    # execution start time(performance measurement related)
    start = time.perf_counter()

    # creating instance of ArgumentParser Class and argument for the path of the text file and number of processes
    parser = argparse.ArgumentParser(description="This script is used to find the common links in given URL(s)")
    parser.add_argument("filepath", help="path of the text file to be processed")
    parser.add_argument("targetpath", help="target path where generated csv files will be stored")
    parser.add_argument("-p", "--processcount", type=int, help="[int] number of processes")
    args = parser.parse_args()

    # checking whether passed path exists or not and accordingly will proceed
    if os.path.exists(args.filepath) and os.path.exists(args.targetpath):
        with open(args.filepath) as file:
            file_read = file.readlines()
            file_read = [text.strip() for text in file_read if not text.isspace()]

        # opening each url in a separate thread using function linkopener
        with ThreadPoolExecutor(max_workers=args.processcount) as executor:
            final_result = executor.map(linkopener, file_read)

        # creating script related csv files
        createcsv(
                    os.path.join(args.targetpath, "common_link_report.csv"),
                    ['href', 'anchor_text', 'total_occurence'],
                    "w"
                 )
        createcsv(
                    os.path.join(args.targetpath, "url_status.csv"),
                    ['url_passed', 'status_code'],
                    "w"
                 )

        # merging data fetched from each website in one list
        for i in final_result:
            master_list.extend(i[0])
            createcsv(
                        os.path.join(args.targetpath, "url_status.csv"),
                        i[1],
                        "a"
                     )

        # passing master_list in commonlinkfinder function
        commonlinkfinder(master_list, os.path.join(args.targetpath, "common_link_report.csv"))
        print("success: data generated in common_link_report.csv and url_status.csv")
    else:
        print("error: one of the given path does not exist")

    # execution stop time(performance measurement related)
    stop = time.perf_counter()
    print(f"finished in {round(stop - start, 4)} second(s)")
