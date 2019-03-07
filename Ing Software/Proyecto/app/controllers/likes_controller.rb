class LikesController < ApplicationController
  before_action :authenticate_user!

  def show
    @liked_posts = Like.all
  end

  def update
    liked = Like.where(user_id: current_user.id, post_id: params[:post_id])
    disliked = Dislike.where(user_id: current_user.id, post_id: params[:post_id])

    if liked == []
      if disliked != []
        disliked.destroy_all
        Like.create(user_id: current_user.id, post_id: params[:post_id])
        Post.where(id: params[:post_id]).find_each do |post|
          post.update(reputation: post.reputation + 2)
        end

      else
        Like.create(user_id: current_user.id, post_id: params[:post_id])
        Post.where(id: params[:post_id]).find_each do |post|
          post.update(reputation: post.reputation + 1)
        end

      end

    else
      liked.destroy_all
      Post.where(id: params[:post_id]).find_each do |post|
        post.update(reputation: post.reputation - 1)
      end
    end
  end
end
