from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title:str
    content: str
    published: bool = True
    rating : Optional[int] = None


my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, {"title" : "fav foods", "content" : "pizza", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
def find_post_index(id):
    for p in range(len(my_posts)):
        if my_posts[p]["id"] == id:
            return p
    return False

# order matters for path operations, as the program will look for the first match for path, the url

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


#retrieving social media posts
@app.get("/posts")
def get_posts():
    return {"Data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000000)
    my_posts.append(post_dict)
    
    print(post)
    #print(post.dict())
    
    #return {"new_post" : f"Title: {payload['title']}, Content: {payload['content']}"} ------ OLD
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail" : post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return {"post_detail" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}



