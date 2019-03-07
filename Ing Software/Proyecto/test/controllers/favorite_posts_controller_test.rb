require 'test_helper'

class FavoritePostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @favorite_post = favorite_posts(:one)
  end

  test 'should get index' do
    get favorite_posts_url
    assert_response :success
  end

  test 'should get new' do
    get new_favorite_post_url
    assert_response :success
  end

  test 'should create favorite_post' do
    assert_difference('FavoritePost.count') do
      post favorite_posts_url,
           params: { favorite_post: { post_Id: @favorite_post.post_Id,
                                      user_Id: @favorite_post.user_Id } }
    end

    assert_redirected_to favorite_post_url(FavoritePost.last)
  end

  test 'should show favorite_post' do
    get favorite_post_url(@favorite_post)
    assert_response :success
  end

  test 'should get edit' do
    get edit_favorite_post_url(@favorite_post)
    assert_response :success
  end

  test 'should update favorite_post' do
    patch favorite_post_url(@favorite_post),
          params: { favorite_post: { post_Id: @favorite_post.post_Id,
                                     user_Id: @favorite_post.user_Id } }
    assert_redirected_to favorite_post_url(@favorite_post)
  end

  test 'should destroy favorite_post' do
    assert_difference('FavoritePost.count', -1) do
      delete favorite_post_url(@favorite_post)
    end

    assert_redirected_to favorite_posts_url
  end
end
