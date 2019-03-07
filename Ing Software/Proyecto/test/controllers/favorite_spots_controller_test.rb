require 'test_helper'

class FavoriteSpotsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @favorite_spot = favorite_spots(:one)
  end

  test 'should get index' do
    get favorite_spots_url
    assert_response :success
  end

  test 'should get new' do
    get new_favorite_spot_url
    assert_response :success
  end

  test 'should create favorite_spot' do
    assert_difference('FavoriteSpot.count') do
      post favorite_spots_url,
           params: { favorite_spot: { turistic_spot_id: @favorite_spot.turistic_spot_id,
                                      user_Id: @favorite_spot.user_Id } }
    end

    assert_redirected_to favorite_spot_url(FavoriteSpot.last)
  end

  test 'should show favorite_spot' do
    get favorite_spot_url(@favorite_spot)
    assert_response :success
  end

  test 'should get edit' do
    get edit_favorite_spot_url(@favorite_spot)
    assert_response :success
  end

  test 'should update favorite_spot' do
    patch favorite_spot_url(@favorite_spot),
          params: { favorite_spot: { turistic_spot_id: @favorite_spot.turistic_spot_id,
                                     user_Id: @favorite_spot.user_Id } }
    assert_redirected_to favorite_spot_url(@favorite_spot)
  end

  test 'should destroy favorite_spot' do
    assert_difference('FavoriteSpot.count', -1) do
      delete favorite_spot_url(@favorite_spot)
    end

    assert_redirected_to favorite_spots_url
  end
end
