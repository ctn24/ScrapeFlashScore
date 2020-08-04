
from requests_html import HTMLSession

#Create the session
session = HTMLSession()

#Define our URL
url = 'https://www.flashscore.com/match/ttobio9E/#lineups;1'

# Use the session to get the data
r = session.get(url)

# Render the page, up the number on scrolldown to page down multiple times on a page
r.html.render(sleep=1, keep_page=True, scrolldown=1)
print(r.text)
# take the rendered html and find the element that we are interested in
videos = r.html.find('#video-title')

# Loop through those elements extracting the text and link
for item in videos:
    video = {
        'title': item.text,
        'link': item.absolute_links
    }
    print(video)


