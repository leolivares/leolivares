require 'test_helper'

class CommentariesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @commentary = commentaries(:one)
  end

  test 'should get index' do
    get commentaries_url
    assert_response :success
  end

  test 'should get new' do
    get new_commentary_url
    assert_response :success
  end

  test 'should create commentary' do
    assert_difference('Commentary.count') do
      post commentaries_url,
           params: { commentary: { content: @commentary.content,
                                   post_id: @commentary.post_id,
                                   reputation: @commentary.reputation,
                                   user_id: @commentary.user_id } }
    end

    assert_redirected_to commentary_url(Commentary.last)
  end

  test 'should show commentary' do
    get commentary_url(@commentary)
    assert_response :success
  end

  test 'should get edit' do
    get edit_commentary_url(@commentary)
    assert_response :success
  end

  test 'should update commentary' do
    patch commentary_url(@commentary),
          params: { commentary: { content: @commentary.content,
                                  post_id: @commentary.post_id,
                                  reputation: @commentary.reputation,
                                  user_id: @commentary.user_id } }
    assert_redirected_to commentary_url(@commentary)
  end

  test 'should destroy commentary' do
    assert_difference('Commentary.count', -1) do
      delete commentary_url(@commentary)
    end

    assert_redirected_to commentaries_url
  end
end
