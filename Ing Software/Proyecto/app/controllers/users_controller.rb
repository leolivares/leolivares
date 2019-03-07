class UsersController < ApplicationController
  include Pagy::Backend
  def show
    Pagy::VARS[:items] = 10
    @user = User.find(params[:id])
    @pagy_post, @my_posts = pagy(Post.where('user_id = ?', params[:id]), page_param: :page_posts)

    @favs = FavoritePost.where(user_id: params[:id]).pluck(:post_id)
    @pagy_favs, @my_favs = pagy(Post.where(id: @favs), page_param: :page_favs)

    @user_posts = Post.distinct.where(user_id: params[:id]).pluck(:id)
    @likes_p = Like.distinct.where(post_id: @user_posts).count
    @dislikes_p = Dislike.distinct.where(post_id: @user_posts).count
    @reputation = (@likes_p + @dislikes_p).zero? ? 0 : ((@likes_p.to_f / (@likes_p + @dislikes_p)) * 5).round(2)

    # @prueba = Post.select("sum(posts.reputation) as rep").where(:user_id => params[:id]).group("posts.user_id")
    # puts "ver"
    # puts @prueba[0].rep

    @complete_stars = @reputation.to_i
    @extra = (@reputation - @complete_stars)
    @half_star = @extra >= 0.5 && @complete_stars < 5 ? 1 : 0
    @empty_stars = 5 - (@complete_stars + @half_star)

    @comments = {}
    @points = {}
    @my_posts.each do |post|
      @likes = Like.distinct.where(post_id: post.id).count
      @dislikes = Dislike.distinct.where(post_id: post.id).count
      @points[post.id] = @likes - @dislikes
      @comments[post.id] = Commentary.where(post_id: post.id).count
    end

    @fav_comments = {}
    @fav_points = {}
    @my_favs.each do |post|
      @likes = Like.distinct.where(post_id: post.id).count
      @dislikes = Dislike.distinct.where(post_id: post.id).count
      @fav_points[post.id] = @likes - @dislikes
      @fav_comments[post.id] = Commentary.where(post_id: post.id).count
    end

    @own_profile = false
    @subscribed = false
    if user_signed_in?
      @own_profile = true if current_user.id == @user.id
      if current_user
        @subscription = Follower.where(user_id: @user.id, follower_id: current_user.id).count
        if @subscription > 0
          @subscribed = true
        end
      end
    end
  end
end
