from flask import Blueprint, jsonify, request

from api.middleware import login_required, read_token
from api.models.db import db
from api.models.blog import Blog
from api.models.comment import Comment

blogs = Blueprint('blogs', 'blogs')

@blogs.route('/', methods=["POST"])
@login_required
def create():
  try:
    # print('SANITY CHECK FOR CREATE BLOG')
    data = request.get_json()
    # print('DATA: ', data)
    profile = read_token(request)
    data["profile_id"] = profile["id"]
    blog = Blog(**data)
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.serialize()), 201
  except:
    return jsonify(message="Failue"), 500

@blogs.route('/update/<id>', methods=["PATCH"])
@login_required
def update(id):
  try:
    data = request.get_json()
    profile = read_token(request)
    blog = Blog.query.filter_by(id=id).first()

    if blog.profile_id != profile["id"]:
      return 'Forbidden', 403

    for key in data:
      setattr(blog, key, data[key])

    db.session.commit()
    return jsonify(blog.serialize()), 200
  except:
    return jsonify(message="Failue"), 500

@blogs.route('/<id>/comment/new/', methods=["POST"])
@login_required
def createComment(id):
  try: 
    print('SANITY CHECK FOR CREATE COMMENT')
    data = request.get_json()
    print('DATA: ', data)
    profile = read_token(request)
    data["profile_id"] = profile["id"]
  # data["blog_id"] = id
    comment = Comment(**data)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.serialize()), 201
  except:
    return jsonify(message="Failue"), 500

@blogs.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  try:
    profile = read_token(request)
    blog = Blog.query.filter_by(id=id).first()

    if blog.profile_id != profile["id"]:
      return 'Forbidden', 403

    db.session.delete(blog)
    db.session.commit()
    return jsonify(message="Success"), 200
  except:
    return jsonify(message="Failue"), 500

# INDEX the cats
# conceptialize the route: api/cats
# define the Route
@blogs.route('/', methods=["GET"])
# build out controller
def index():
  try:
    blogs = Blog.query.all()
    return jsonify([blog.serialize() for blog in blogs]), 200
  except:
    return jsonify(message="Failue"), 500


# create a blog post
# @blogs.route('/create', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     form = BlogPostForm()
#     if form.validate_on_submit():
#         blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)
#         db.session.add(blog_post)
#         db.session.commit()
#         flash('Blog Post Created')
#         print('Blog Post Created')
#         return redirect(url_for('core.index'))
#     return render_template('create_post.html', form=form)