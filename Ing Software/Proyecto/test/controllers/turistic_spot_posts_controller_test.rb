require 'test_helper'

class TuristicSpotPostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @turistic_spot_post = turistic_spot_posts(:one)
  end

  test 'should get index' do
    get turistic_spot_posts_url
    assert_response :success
  end

  test 'should get new' do
    get new_turistic_spot_post_url
    assert_response :success
  end

  test 'should create turistic_spot_post' do
    assert_difference('TuristicSpotPost.count') do
      post turistic_spot_posts_url, params: { turistic_spot_post:
        { turistic_post_id: @turistic_spot_post.turistic_post_id } }
    end

    assert_redirected_to turistic_spot_post_url(TuristicSpotPost.last)
  end

  test 'should show turistic_spot_post' do
    get turistic_spot_post_url(@turistic_spot_post)
    assert_response :success
  end

  test 'should get edit' do
    get edit_turistic_spot_post_url(@turistic_spot_post)
    assert_response :success
  end

  test 'should update turistic_spot_post' do
    patch turistic_spot_post_url(@turistic_spot_post), params:
    { turistic_spot_post: { turistic_post_id: @turistic_spot_post.turistic_post_id } }
    assert_redirected_to turistic_spot_post_url(@turistic_spot_post)
  end

  test 'should destroy turistic_spot_post' do
    assert_difference('TuristicSpotPost.count', -1) do
      delete turistic_spot_post_url(@turistic_spot_post)
    end

    assert_redirected_to turistic_spot_posts_url
  end
end
