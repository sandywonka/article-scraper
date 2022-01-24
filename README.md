# Sonar
News Portal Scraping Bot Using Python and Integrated with MySQL Database

# Tools
- Python 3.8.3

## Installation
Create virtual environment for python.
```bash
virtualenv venv
```
Activating the virtual environment.
```bash
source ../venv/scripts/activate
```
Install list of packages inside requirements.txt
```bash
pip install -r requirements.txt
```

## Usage

MySQL
```sql
CREATE TABLE prog_test.news_article (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '',
  url varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  content longtext COLLATE utf8mb4_unicode_520_ci,
  summary text COLLATE utf8mb4_unicode_520_ci,
  article_ts bigint(20) NOT NULL DEFAULT '0' COMMENT 'published timestamp of article',
  published_date date DEFAULT NULL,
  inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY UNIK (url)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;
```
Run program from git/cmd
```bash
python controller.py
```

Or simply run controller.py
