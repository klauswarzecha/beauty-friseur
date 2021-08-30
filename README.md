# beauty - Crawling business data with a minimum of requests

## Background

The current project was created to demonstrate how business data
 can be collected from web portals in an unobtrusive way.

For this purpose two German beauty portals are scraped
 with a minimum of requests.

## Implementation

The project is realized in Python (3.9) and utilizes the [Scrapy](https://scrapy.org/)
 (2.5.0) framework. The latter offers a CrawlSpider class, in which the interaction
  of rules and callbacks can be used to visit each and every page on a portal.

In this project, however, it was crucial to avoid deep crawling!

The individual pages of companies on these portals were **never** accessed!

All business data including cosmetic services were collected from overview
 pages. In thew case of one portal, each request furnished roughly ten
 company entries. In the case of another portal, the overview pages for larger
 cities contained much more entries. For each of these entries, an
 [item](https://docs.scrapy.org/en/latest/topics/items.html) was
 yielded and exported.

## How to run

- Deploy a Scrapy container
- Deploy the project via scrapyd-deploy
- Start a crawler using curl

## Remarks

This project is a proof of principle. Both crawlers are fully functional.
However, there's neither a proxy middleware, nor any database connection.

Enjoy and keep in mind that less requests aren't necessarily a bad thing ;-)
