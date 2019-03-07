class CommentDislikesController < ApplicationController
  before_action :authenticate_user!

  def update
    disliked = CommentDislike.where(user_id: current_user.id, commentary_id: params[:comment_id])
    liked = CommentLike.where(user_id: current_user.id, commentary_id: params[:comment_id])

    if disliked == []
      liked.destroy_all if liked != []
      CommentDislike.create(user_id: current_user.id, commentary_id: params[:comment_id])
    else
      disliked.destroy_all
    end
  end
end
