from flask import request, Blueprint, g
from ..shared.Authentication import Auth
from ..models.PostModel import PostModel, PostSchema
from ..models.LikeModel import LikeModel, LikeSchema
from ..models.NewsfeedModel import NewsfeedModel, NewsfeedSchema
from src.jsonResponse import custom_response

like_api = Blueprint('like', __name__)
post_schema = PostSchema()
like_schema = LikeSchema()
newsfeed_schema = NewsfeedSchema()

@like_api.route('/like_post/<int:post_id>', methods=['GET'])
@Auth.auth_required
def like_post(post_id):
    post = PostModel.get_one_post(post_id)
    if not post: return custom_response({'error': 'Post not found.'}, 400)
    if g.user.get('id') == post.get_id(): return custom_response({'error': 'Is your post.'}, 400)
    if LikeModel.get_one_if_liked(post.get_id(), g.user.get('id')): return custom_response({'error': 'Post already liked.'}, 400)
    like = LikeModel(post_id, g.user.get('id'))
    like.save()
    news = NewsfeedModel("like", like.id, g.user.get('id'))
    news.save()
    return custom_response({'success': 'Post liked.'}, 200)

@like_api.route('/delete_like_post/<int:like_id>', methods=['GET'])
@Auth.auth_required
def delete_like_post(like_id):
    like = LikeModel.get_one_like_by_user_id(like_id, g.user.get('id'))
    if not like: return custom_response({'error': 'You not liked this post.'}, 400)
    news = NewsfeedModel.get_one_news_by_user_id(like.get_id(), g.user.get('id'))
    if not news: return custom_response({'error': 'You not liked this news.'}, 400)
    like.delete()
    news.delete()
    return custom_response({'success': 'Post unliked.'}, 200)