from scrape import ScrapeQuotes

quotes = ScrapeQuotes()
quotes.scrape()
quotes.to_csv(filename="./quotes.csv")
