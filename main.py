import requests
import lxml.html

# Get website and store into HtmlElement object with lxml
BASE_URL = "https://store.steampowered.com/explore/new/"
response = requests.get(BASE_URL)
doc = lxml.html.fromstring(response.content)

# Return all divs from HTML that have id=tab_newreleases_content
# xpath gives a list of all divs in the HTML page with the matching content
# "//" tells lxml that we want to look for all tags that match our filter
new_releases = doc.xpath("//div[@id='tab_newreleases_content']")[0]

# Within new_releases, we look for tab_item_name
# "." tells lxml we only want the tags that are the children of the new_releases tag
# /text() tells lxml we only want the text contained in the tag
titles = new_releases.xpath(".//div[@class='tab_item_name']/text()")

# Get prices (discount_final_price)
prices = new_releases.xpath(".//div[@class='discount_final_price']/text()")

# Get tags for each game
tags = [tag.text_content() for tag in new_releases.xpath(".//div[@class='tab_item_top_tags']")]
tags = [tag.split(", ") for tag in tags]

# Get platforms for each game
platforms_div = new_releases.xpath(".//div[@class='tab_item_details']")
total_platforms = []

for game in platforms_div:
    # Instead of using [@class='platform_img'], we use the contains method in case the spans have other classes
    temp = game.xpath(".//span[contains(@class, 'platform_img')]")
    # get method gets attribute of a tag (class from span)
    # split on whitespace between "platform_img" and the platform, get last item in split list (actual platform)
    # Example: "platform_img win" -> ["platform_img", "win"] -> "win"
    platforms = [t.get("class").split(" ")[-1] for t in temp]
    # If there are separators in the list, get rid of them
    if "hmd_separator" in platforms:
        platforms.remove("hmd_separator")
    total_platforms.append(platforms)

# Return a JSON response to turn into a web-based API
output = []
for info in zip(titles, prices, tags, total_platforms):
    resp = {
        "title": info[0],
        "price": info[1],
        "tags": info[2],
        "platforms": info[3]
    }
    output.append(resp)


