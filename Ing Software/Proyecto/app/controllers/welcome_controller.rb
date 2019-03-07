class WelcomeController < ApplicationController
  protect_from_forgery with: :exception
  layout 'welcome_layout'
  include Pagy::Backend
  def index
    @posts = Post.all
    @image_posts = Post.where(type_post: 2)
    @pagy_post, @recent_posts = pagy(Post.order('created_at DESC'))

    @points = {}
    @comments = {}
    @recent_posts.each do |post|
      @likes = Like.distinct.where(post_id: post.id).count
      @dislikes = Dislike.distinct.where(post_id: post.id).count
      @points[post.id] = @likes - @dislikes
      @comments[post.id] = Commentary.where(post_id: post.id).count
    end

    @points_image = {}
    @comments_image = {}
    @image_posts.each do |post|
      @likes_i = Like.distinct.where(post_id: post.id).count
      @dislikes_i = Dislike.distinct.where(post_id: post.id).count
      @points_image[post.id] = @likes_i - @dislikes_i
      @comments_image[post.id] = Commentary.where(post_id: post.id).count
    end
    if @points_image.empty?
      @best_post = nil
    else
      @best_post = Post.find(@points_image.key(@points_image.values.max))
      @featured_image_posts = Post.where(type_post: 2).order(:reputation).limit(3).offset(1)
    end

    pre_country_posts = CountryPost.pluck(:post_id)
    @country_posts = Post.where(id: pre_country_posts)
    @country_posts_images = Post.where(id: pre_country_posts, type_post: 2)

    pre_city_posts = CityPost.pluck(:post_id)
    @city_posts = Post.where(id: pre_city_posts)
    @city_posts_images = Post.where(id: pre_city_posts, type_post: 2)

    pre_hotel_posts = HotelPost.pluck(:post_id)
    @hotel_posts = Post.where(id: pre_hotel_posts)
    @hotel_posts_images = Post.where(id: pre_hotel_posts, type_post: 2)

    pre_restaurant_posts = RestaurantPost.pluck(:post_id)
    @restaurant_posts = Post.where(id: pre_restaurant_posts)
    @restaurant_posts_images = Post.where(id: pre_restaurant_posts, type_post: 2)

    pre_turistic_spot_posts = TuristicSpotPost.pluck(:post_id)
    @turistic_spot_posts = Post.where(id: pre_turistic_spot_posts)
    @turistic_spot_posts_images = Post.where(id: pre_turistic_spot_posts, type_post: 2)

    if current_user
      following = Follower.where(follower_id: current_user.id).pluck(:user_id)
      @feed_posts = Post.where(user_id: following)
      @feed_posts_images = Post.where(user_id: following, type_post: 2)
    end

    admins_pick = AdminPost.order('created_at DESC').limit(3).pluck(:post_id)
    @admin_posts = Post.where(id: admins_pick)
  end

  def test
    @image_posts = Post.where(type_post: 2)
  end
end
