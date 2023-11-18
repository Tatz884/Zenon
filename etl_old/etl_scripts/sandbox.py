es = Elasticsearch(['http://elasticsearch:9200'])
response = es.search(
    index="polish",
    body={
        "_source": ["word", "glosses"],  # Only retrieve the 'word' and 'glosses' fields
        "query": {
            "multi_match": {
                "query": "mam",
                "fields": ["forms.*"],
                "lenient": True
            }
        }
    }
)
hits = response["hits"]["hits"]
for hit in hits[:3]:
    print(hit["_source"])


    # df['tags_extracted'] = df['forms'].apply(extract_tags)
    # # print(df['tags_extracted'])

    # # 1. Convert the lists in 'tags_extracted' to tuple format
    # df['tuple_tags'] = df['tags_extracted'].apply(lambda x: tuple(map(tuple, x)))

    # # 2. Group by these tuples and 3. aggregate the words
    # grouped = df.groupby('tuple_tags')['word'].apply(list)

    # # 4. Print the results
    # for tags, words in grouped.items():
    #     print("Tags:", tags)
    #     print("Words:", words)
    #     print("--------")
    # unique_inner_lists = set(tuple(map(tuple, sublist)) for sublist in df['tags_extracted'])
    # for inner_tuple in unique_inner_lists:
    #     print(inner_tuple, end=",\n")




    # for knowing the tags

    # def extract_tags(data):
    #     return [item.get('tags', []) for item in data]