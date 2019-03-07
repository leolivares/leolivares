class DislikesController < ApplicationController
  before_action :authenticate_user!

  def show
    @disliked_posts = Dislike.all
  end

  def update
    disliked = Dislike.where(user_id: current_user.id, post_id: params[:post_id])
    liked = Like.where(user_id: current_user.id, post_id: params[:post_id])

    if disliked == []
      if liked != []
        liked.destroy_all
        Dislike.create(user_id: current_user.id, post_id: params[:post_id])
        Post.where(id: params[:post_id]).find_each do |post|
          post.update(reputation: post.reputation - 2)
        end

      else
        Dislike.create(user_id: current_user.id, post_id: params[:post_id])
        Post.where(id: params[:post_id]).find_each do |post|
          post.update(reputation: post.reputation - 1)
        end

      end

    else
      disliked.destroy_all
      Post.where(id: params[:post_id]).find_each do |post|
        post.update(reputation: post.reputation + 1)
      end
    end
  end
end
