require 'test_helper'

class RestaurantPostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @restaurant_post = restaurant_posts(:one)
  end

  test 'should get index' do
    get restaurant_posts_url
    assert_response :success
  end

  test 'should get new' do
    get new_restaurant_post_url
    assert_response :success
  end

  test 'should create restaurant_post' do
    assert_difference('RestaurantPost.count') do
      post restaurant_posts_url, params: { restaurant_post: { restaurant_id: @restaurant_post.restaurant_id } }
    end

    assert_redirected_to restaurant_post_url(RestaurantPost.last)
  end

  test 'should show restaurant_post' do
    get restaurant_post_url(@restaurant_post)
    assert_response :success
  end

  test 'should get edit' do
    get edit_restaurant_post_url(@restaurant_post)
    assert_response :success
  end

  test 'should update restaurant_post' do
    patch restaurant_post_url(@restaurant_post), params: { restaurant_post:
      { restaurant_id: @restaurant_post.restaurant_id } }
    assert_redirected_to restaurant_post_url(@restaurant_post)
  end

  test 'should destroy restaurant_post' do
    assert_difference('RestaurantPost.count', -1) do
      delete restaurant_post_url(@restaurant_post)
    end

    assert_redirected_to restaurant_posts_url
  end
end
