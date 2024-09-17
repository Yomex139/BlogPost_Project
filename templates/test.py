#
# @app.route("/post/<int:post_id>")
# @login_required
# def show_post(post_id):
#     is_admin = current_user.id == 1
#     requested_post = db.get_or_404(BlogPost, post_id)
#     return render_template("post.html", post=requested_post, admin=is_admin)
#
#
#
# {% include "header.html" %}
#
# <!-- Page Header-->
# <header class="masthead" style="background-image: url('{{post.img_url}}')">
#   <div class="container position-relative px-4 px-lg-5">
#     <div class="row gx-4 gx-lg-5 justify-content-center">
#       <div class="col-md-10 col-lg-8 col-xl-7">
#         <div class="post-heading">
#           <h1>{{ post.title }}</h1>
#           <h2 class="subheading">{{ post.subtitle }}</h2>
#           <span class="meta"
#             >Posted by
#             <a href="#">{{ post.author.name }}</a>
#             on {{ post.date }}
#           </span>
#         </div>
#       </div>
#     </div>
#   </div>
# </header>
#
# <!-- Post Content -->
# <article>
#   <div class="container px-4 px-lg-5">
#     <div class="row gx-4 gx-lg-5 justify-content-center">
#       <div class="col-md-10 col-lg-8 col-xl-7">
#         {{ post.body|safe }}
#         <!--TODO: Only show Edit Post button if user id is 1 (admin user) -->
#         {% if admin %}
#         <div class="d-flex justify-content-end mb-4">
#           <a
#             class="btn btn-primary float-right"
#             href="{{url_for('edit_post', post_id=post.id)}}"
#             >Edit Post</a
#           >
#         </div>
#         {% endif %}
#         <!-- Comments Area -->
#         <!-- TODO: Add a CKEditor for commenting below -->
#         <div class="comment">
#           <!-- TODO: Show all the comments on a post -->
#           <ul class="commentList">
#             <li>
#               <div class="commenterImage">
#                 <img src="../static/assets/img/default-profile.jpg" />
#               </div>
#               <div class="commentText">
#                 <p>Some comment</p>
#                 <span class="date sub-text">comment author name</span>
#               </div>
#             </li>
#           </ul>
#         </div>
#       </div>
#     </div>
#   </div>
# </article>
#
# {% include "footer.html" %}

#
#
# {% include "header.html" %}
#
# <!-- Page Header-->
# <header
#   class="masthead"
#   style="background-image: url('../static/assets/img/home-bg.jpg')"
# >
#   <div class="container position-relative px-4 px-lg-5">
#     <div class="row gx-4 gx-lg-5 justify-content-center">
#       <div class="col-md-10 col-lg-8 col-xl-7">
#         <div class="site-heading">
#           <h1>Angela's Blog</h1>
#           <span class="subheading">A collection of random musings.</span>
#         </div>
#       </div>
#     </div>
#   </div>
# </header>
#
# <!-- Main Content -->
# <div class="container px-4 px-lg-5">
#   <div class="row gx-4 gx-lg-5 justify-content-center">
#     <div class="col-md-10 col-lg-8 col-xl-7">
#       <!-- Post preview -->
#       {% for post in all_posts %}
#       <div class="post-preview">
#         <a href="{{ url_for('show_post', post_id=post.id) }}">
#           <h2 class="post-title">{{ post.title }}</h2>
#           <h3 class="post-subtitle">{{ post.subtitle }}</h3>
#         </a>
#         <p class="post-meta">
#           Posted by
#           <a href="#">{{ post.author }}</a>
#           on {{ post.date }}
#           <!-- Show delete button only if user is admin (ID is 1) -->
#           {% if admin %}
#           <a href="{{ url_for('delete_post', post_id=post.id) }}">✘</a>
#           {% endif %}
#         </p>
#       </div>
#       {% endfor %}
#
#       <!-- Divider -->
#       <hr class="my-4" />
#
#       <!-- New Post -->
#       <!-- Show Create Post button only if user is admin (ID is 1) -->
#       {% if admin %}
#       <div class="d-flex justify-content-end mb-4">
#         <a class="btn btn-primary float-right" href="{{ url_for('add_new_post') }}">Create New Post</a>
#       </div>
#       {% endif %}
#
#       <!-- Pager -->
#       <div class="d-flex justify-content-end mb-4">
#         <a class="btn btn-secondary text-uppercase" href="#!">Older Posts →</a>
#       </div>
#     </div>
#   </div>
# </div>
#
# {% include "footer.html" %}
import datetime
from datetime import date
year = date.today().year
print(year)
