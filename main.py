from fastapi import FastAPI
from typing import List
from database import get_posts, get_posts_by_tag_names, get_tags
from models import IPost, ITag, PostsResponse, PostsResponseMeta, SelectedTags
from utils import get_tags_from_string

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=PostsResponse)
async def posts(tags: str = ''):
    selected_tags = get_tags_from_string(tags) if tags else None
    posts_results=get_posts(selected_tags).all()

    return PostsResponse(
        meta=PostsResponseMeta(
            count=len(posts_results),
            selected_tags=selected_tags if selected_tags else SelectedTags()
        ),
        posts=posts_results
    )



@app.get("/posts_tagged")
async def posts_tagged(tag_names):
    return get_posts_by_tag_names(tag_names.split(",")).all()


@app.get("/tags", response_model=List[ITag])
async def tags():
    return get_tags().all()

# seed_tags(7)
# get_posts_by_tag_name('customer')
# get_posts_by_tag_names(['half', 'customer', 'stuff'])
# get_posts_by_tag_id(4)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app)
