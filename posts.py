def get_posts(query, page, client):
    return client.get(f"posts.json?tags={query}&page={page}")[0]
