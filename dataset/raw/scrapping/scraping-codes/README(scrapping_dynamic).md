# Journals Scrapper

## Explanation

This scrapper generates CSV files from digital journals with the following information:  
* Title  
* Date  
* URL  

## How to use

1. Create a csv file and name it with journal abbreviation. (This should be done for all journal source types) For example: *psb_output.csv*  

2. Insert the following columns manually into the blank CSV file, it should have only the following single line at the start: 

``` title, date, url ```

3. Make sure to install all pip dependencies:  
    * pip install requests
    * pip install beautifulsoup4
    * pip install pandas    

4. In the main function, you can use the **get_articles_from_journal** function to scrape single page or the **iterate_get_articles_from_journal** function to scrape a range of pages  
    * ***get_articles_from_journal(source, page=1)***
        * *source* is the journal abbreviation
        * *page* is the target page
        * Example: The following code will scrape articles from the following link: https://pv.org.br/noticias/page/1  
        * ``` get_articles_from_journal("pv") ```  

    * ***iterate_get_articles_from_journal(source, start_page, end_page)***
        * *source* is the journal abbreviation
        * *start_page* is the start index of range of pages
        * *end_page* is the end index of range of pages
        * Example: The following code will scrape articles from all pages starting from https://www.mdb.org.br/noticias/page/2/ to https://www.mdb.org.br/noticias/page/10/
        * ``` iterate_get_articles_from_journal("mdb", 2, 10) ```

5. Finally, executes the python file
        
## Currently available sources

* "pv" - https://pv.org.br/noticias/
* "psb" - https://psb40.org.br/noticias/
* "mdb" - https://www.mdb.org.br/noticias/

### Thank you for using this scrapper
