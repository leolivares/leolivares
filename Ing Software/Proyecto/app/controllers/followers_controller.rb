class FollowersController < ApplicationController
  before_action :authenticate_user!

  def subscribe
    foll = Follower.where(user_id: params[:id], follower_id: current_user.id)
    count = foll.count

    if count == 0
      Follower.create(user_id: params[:id], follower_id: current_user.id)
    else
      foll.destroy_all
    end
  end
end
