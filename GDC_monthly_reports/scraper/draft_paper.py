obj_list = dc.documents.search('project:225200', mentions=True)

obj_list_2 = dc.documents.search('user:17279 "Prison Sentence In Years"', sort='title', page=1, per_page=50, mentions=True)
for search_result in obj_list_2:
    this_dict = {}
    this_dict['title'] = search_result.title
    search_result.access = 'public'
    search_result.put()
    search_mentions = search_result.mentions
    page_number = search_mentions[1].page
    this_dict['page_number'] = page_number
    this_dict['id'] = search_result.id
    time.sleep(3)
    print(f"{this_dict['title']}\t{this_dict['id']}\t{this_dict['page_number']}")
