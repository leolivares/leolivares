require 'test_helper'

class TuristicSpotsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @turistic_spot = turistic_spots(:one)
  end

  test 'should get index' do
    get turistic_spots_url
    assert_response :success
  end

  test 'should get new' do
    get new_turistic_spot_url
    assert_response :success
  end

  test 'should create turistic_spot' do
    assert_difference('TuristicSpot.count') do
      post turistic_spots_url,
           params: { turistic_spot: {
             city_id: @turistic_spot.city_id,
             nombre: @turistic_spot.nombre,
             reputation: @turistic_spot.reputation
           } }
    end

    assert_redirected_to turistic_spot_url(TuristicSpot.last)
  end

  test 'should show turistic_spot' do
    get turistic_spot_url(@turistic_spot)
    assert_response :success
  end

  test 'should get edit' do
    get edit_turistic_spot_url(@turistic_spot)
    assert_response :success
  end

  test 'should update turistic_spot' do
    patch turistic_spot_url(@turistic_spot),
          params: { turistic_spot: { city_id: @turistic_spot.city_id,
                                     nombre: @turistic_spot.nombre,
                                     reputation: @turistic_spot.reputation } }
    assert_redirected_to turistic_spot_url(@turistic_spot)
  end

  test 'should destroy turistic_spot' do
    assert_difference('TuristicSpot.count', -1) do
      delete turistic_spot_url(@turistic_spot)
    end

    assert_redirected_to turistic_spots_url
  end
end
