# common_link_finder.py

### _features_
- Accepts the text file consists of URL(s) needs to be processed to find out the common links and content from anchor tag.

### _usage_
```
common_link_finder.py [-h] [-p PROCESSCOUNT] filepath targetpath

positional arguments:
  filepath              path of the text file to be processed
  targetpath            target path where generated csv files will be stored

optional arguments:
  -h, --help                                    show this help message and exit
  -p PROCESSCOUNT, --processcount PROCESSCOUNT  [int] number of processes
```
for example:
```
$ python3 common_link_finder.py "/Users/urls.txt" "/Users/"
```
If any of the passed path during executing the script is incorrect, you will get below error:
```
error: one of the given path does not exist
```

### _output_
- It will generate 2 csv files at the given target path, 'common_link_report_.csv' and 'url_status.csv'
- 'common_link_report.csv' will consists of these columns:
  | href | anchor_text | total_occurrence |
  |------|-------------|------------------|
  |https://xyz.com/home| Home | 2         |

- 'url_status.csv' will consists of below columns which is actually capturing the status code for each URL. If an invalid URL is present in the passed text file, then it will come as 'invalid_url'
  | url_passed | status_code |
  |------------|-------------|
  |https://xyz.com/home| 200 |
