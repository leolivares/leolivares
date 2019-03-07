class CommentLikesController < ApplicationController
  before_action :authenticate_user!

  def update
    liked = CommentLike.where(user_id: current_user.id, commentary_id: params[:comment_id])
    disliked = CommentDislike.where(user_id: current_user.id, commentary_id: params[:comment_id])

    if liked == []
      disliked.destroy_all if disliked != []
      CommentLike.create(user_id: current_user.id, commentary_id: params[:comment_id])
    else
      liked.destroy_all
    end
  end
end
