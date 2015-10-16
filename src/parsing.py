from BeautifulSoup import BeautifulSoup

ROOT_LIST_ITEM_TAG_CLASS = "oos_listItem oos_20plus"
PHONE_NUMBER_TAG_CLASS = "oos_previewTitle"
COMMENT_COUNT_TAG_CLASS = "oos_previewSide"
BODY_TAG_CLASS = "oos_previewBody"

def parse_comment_count(tag):
    for comment_count in tag.findAll("div", {"class": COMMENT_COUNT_TAG_CLASS}):
        comment_count = comment_count.string
        return comment_count    

def parse_phone_number(tag):
    for phone_number in tag.findAll("a", {"class": PHONE_NUMBER_TAG_CLASS}):
        full_number = phone_number.string
        number_parts = full_number.split("-")
        area_code = number_parts[0]
        just_number = ''.join(number_parts[1:])
        return (full_number.replace("-", ""), area_code)

def parse_body_tag(tag):
    for body_tag in tag.findAll("div", {"class": BODY_TAG_CLASS}):
        body = body_tag.contents[0]
        return body
    

def parse_page(content):
    results = []
    soup = BeautifulSoup(content)
    for tag in soup.findAll(lambda tag: tag.name=="li" and ("class", ROOT_LIST_ITEM_TAG_CLASS) in tag.attrs):
        result = {}
        result['phone_number'], result['area_code'] = parse_phone_number(tag)
        result['comment_count'] = parse_comment_count(tag)
        result['body'] = parse_body_tag(tag)
        results.append(result)
    return results
