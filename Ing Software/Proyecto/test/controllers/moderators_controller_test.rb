require 'test_helper'

class ModeratorsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @moderator = moderators(:one)
  end

  test 'should get index' do
    get moderators_url
    assert_response :success
  end

  test 'should get new' do
    get new_moderator_url
    assert_response :success
  end

  test 'should create moderator' do
    assert_difference('Moderator.count') do
      post moderators_url, params: { moderator: { country_id: @moderator.country_id, user_id: @moderator.user_id } }
    end

    assert_redirected_to moderator_url(Moderator.last)
  end

  test 'should show moderator' do
    get moderator_url(@moderator)
    assert_response :success
  end

  test 'should get edit' do
    get edit_moderator_url(@moderator)
    assert_response :success
  end

  test 'should update moderator' do
    patch moderator_url(@moderator), params: { moderator: { country_id: @moderator.country_id,
                                                            user_id: @moderator.user_id } }
    assert_redirected_to moderator_url(@moderator)
  end

  test 'should destroy moderator' do
    assert_difference('Moderator.count', -1) do
      delete moderator_url(@moderator)
    end

    assert_redirected_to moderators_url
  end
end
