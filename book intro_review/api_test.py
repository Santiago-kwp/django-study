import config
client_id = config.client_id
client_key = config.cliend_key

def search_book(query):
    from urllib.request import Request, urlopen
    from urllib.parse import quote
    import json

    url = 'https://openapi.naver.com/v1/search/book.json'
    option = '&d_dafr=20190101&display=10&d_catg=100030010'
    query = '?query='+quote(query)
    url_query = url + query + option

    #Open API 검색 요청 개체
    request = Request(url_query)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_key)

    #검색 요청 및 처리
    response = urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
        return json.loads(response_body.decode('utf-8'))
    else:
        return "Error code:"+rescode

for book in search_book('파이썬')['items']:
    title = book['title'].replace('<b>','').replace('</b>','')
    image = book['image']
    author = book['author']
    description = book['description']
    print(title)