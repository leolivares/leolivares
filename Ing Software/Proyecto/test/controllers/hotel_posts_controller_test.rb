require 'test_helper'

class HotelPostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @hotel_post = hotel_posts(:one)
  end

  test 'should get index' do
    get hotel_posts_url
    assert_response :success
  end

  test 'should get new' do
    get new_hotel_post_url
    assert_response :success
  end

  test 'should create hotel_post' do
    assert_difference('HotelPost.count') do
      post hotel_posts_url, params: { hotel_post: { hotel_id: @hotel_post.hotel_id } }
    end

    assert_redirected_to hotel_post_url(HotelPost.last)
  end

  test 'should show hotel_post' do
    get hotel_post_url(@hotel_post)
    assert_response :success
  end

  test 'should get edit' do
    get edit_hotel_post_url(@hotel_post)
    assert_response :success
  end

  test 'should update hotel_post' do
    patch hotel_post_url(@hotel_post), params: { hotel_post: { hotel_id: @hotel_post.hotel_id } }
    assert_redirected_to hotel_post_url(@hotel_post)
  end

  test 'should destroy hotel_post' do
    assert_difference('HotelPost.count', -1) do
      delete hotel_post_url(@hotel_post)
    end

    assert_redirected_to hotel_posts_url
  end
end
