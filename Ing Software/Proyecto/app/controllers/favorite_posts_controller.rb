class FavoritePostsController < ApplicationController
  before_action :authenticate_user!, except: [:show]
  before_action :authenticate_admin!, only: [:show]
  # GET /favorite_posts
  # GET /favorite_posts.json
  def index
    @favorite_posts = FavoritePost.all
  end

  # GET /favorite_posts/1
  # GET /favorite_posts/1.json
  def show
    @fav_posts = FavoritePost.all
  end

  # GET /favorite_posts/new
  def new
    @favorite_post = FavoritePost.new
  end

  def update
    @post_id = params[:post_id]
    @user_id = params[:user_id]

    favorites = FavoritePost.where(user_id: current_user.id, post_id: params[:post_id])

    if favorites == []
      FavoritePost.create(user_id: current_user.id, post_id: params[:post_id])
    else
      favorites.destroy_all
    end
  end
end
