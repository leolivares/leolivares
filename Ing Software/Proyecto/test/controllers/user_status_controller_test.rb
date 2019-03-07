require 'test_helper'

class UserStatusControllerTest < ActionDispatch::IntegrationTest
  test 'should get index' do
    get user_status_index_url
    assert_response :success
  end
end
