from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import feedparser

rss_feeds = {
    'Tuko News': 'https://www.tuko.co.ke/rss/all.rss',
    'Nation Media': 'https://nation.africa/rss'
}

def home_view(request):

    news = []
    for source, feed in rss_feeds.items():
        parsed_feeds = feedparser.parse(feed)
        entries = []
        for entry in parsed_feeds.entries:
            entry = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "published_parsed": entry.published_parsed,
                "source": source
            }
            entries.append(entry)
        
        entries = sorted(entries, key=lambda x: x['published_parsed'], reverse=True)
        news.extend(entries)

    p_news = Paginator(news, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p_news.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p_news.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p_news.page(p_news.num_pages)
    context = {'page_obj': page_obj}

    context = {
        'news': p_news,
        'page_obj': page_obj
    }

    return render(request, 'home.html', context)
