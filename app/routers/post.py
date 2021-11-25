from .. import models, schemas, oauth2 # .. to go up a directory
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("", response_model=List[schemas.PostOut]) #list because multiple posts
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ''):
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()  - to allow user to only retrive posts by the logged in user.
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return results

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #WITHOUT SQLALCHEMY:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # #we use %s,%s to sanatize means to protect out code from SQL injection.
    # #SQL injection means if we add post.title, post.content, etc directly instead of %s, a user can add...
    # #sql commands in those fields(title, content) and can access out code.
    # new_post = cursor.fetchone()
    # conn.commit() #this is to actually submit data to pg database.
    # return {"data": new_post}

    #WITH SQLALCHEMY:
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #or
    new_post = models.Post(user_id=current_user.id, **post.dict())# this will create and unpack the dictionary. Very imp when we have a lot of fields in our Post class.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    

# @app.get('/posts/latest')
# def get_latest_post():
#     latest_post = my_posts[len(my_posts) - 1]
    return {'details': latest_post}

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id))) #we need to convert id to string here coz whole statement is in string
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first() #.all will also work instead of .first but if we use .all it will keep looking for more posts with same id when we know there is only one. so, .first is more efficient.
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} was not found')

    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to Perform the action') - to allow only the logged in user access their own posts.

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'post with id: {id} was not found'}
    return post





@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    


    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ID does not exist')

    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to Perform the action')

    deleted_post.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) #first we find the id
    updated_post = post_query.first() #then we grab that post
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ID does not exist') #return 404 if found none
        
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized to Perform the action')

    post_query.update(post.dict(), synchronize_session=False) #update post by passing in our post as a dictionary
    db.commit() #commit changes

    return post_query.first()