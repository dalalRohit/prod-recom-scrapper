import scrapy


class AmazonReviewsSpider(scrapy.Spider):

    # Spider name
    name = 'amazon'

    # Domain names to scrape
    allowed_domains = ['amazon.in']

    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.amazon.in/Samsung-Display-Storage-6000mAH-Battery/product-reviews/B07HGMQX6N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls = []

    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1, 100):
        start_urls.append(myBaseUrl+str(i))

    # Defining a Scrapy parser
    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        # Username
        username = data.css('.a-profile-name')
        # Profile
        a = profile = data.css('.a-profile::attr(href)').getall()
        for i in range(len(a)):
            a[i] = 'https://amazon.in/'+a[i]
        # User review date
        date = data.css('.review-date')

        # Collecting product star ratings
        star_rating = data.css('.review-rating')

        # Collecting user reviews
        comments = data.css('.review-text')

        # Collecting review title
        review_title = data.css('.review-title')

        # verified
        verified = data.css('span.a-color-state.a-text-bold')

        # helpful
        helpful = data.css('.cr-vote-text')
        count = 0

        # Combining the results
        for review in star_rating:
            yield{
                "Username": ''.join(username[count].xpath('.//text()').extract()).strip(),
                "Profile": ''.join(profile[count]).strip(),
                "Date": ''.join(date[count].xpath('.//text()').extract()).strip(),
                'Title': ''.join(review_title[count].xpath('.//text()').extract()).strip(),

                'Comment': ''.join(comments[count].xpath(".//text()").extract()).strip(),

                'Stars': ''.join(review.xpath('.//text()').extract()).strip(),
                'Helpful': ''.join(helpful[count].xpath('.//text()').extract()),
                'Verified': "".join(verified[count].xpath('.//text()').extract()).strip()
            }
            count = count+1
            '''
            next_page = response.css('.a-last a::attr(href)').getall()
            print('Next page', next_page)
            if(len(next_page) != 0):
                next_page = response.urljoin(next_page)
                print(next_page)
                # yield scrapy.Request('https://amazon.in'+next_page, callback=self.parse)
            '''
