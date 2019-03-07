class AdminController < ApplicationController
  before_action :authenticate_admin!
  def home; end

  def stats
    # Post Count
    data_p = Post.create_count
    stat = Hash[(Date.today - 6..Date.today).to_a.product([0])]
    stat.each { |k, _v| stat[k] = data_p[k] if data_p[k] }

    data_c = Commentary.create_count
    stat_c = Hash[(Date.today - 6..Date.today).to_a.product([0])]
    stat_c.each { |k, _v| stat_c[k] = data_c[k] if data_c[k] }
    @data = {
      labels: stat.keys.to_a,
      datasets: [
        {
          label: 'Publicaciones',
          backgroundColor: 'transparent',
          borderColor: 'rgba(220,53,69,0.75)',
          borderWidth: 3,
          pointStyle: 'circle',
          pointRadius: 5,
          pointBorderColor: 'transparent',
          pointBackgroundColor: 'rgba(220,53,69,0.75)',
          data: stat.values.to_a
        },
        {
          label: 'Comentarios',
          backgroundColor: 'transparent',
          borderColor: 'rgba(40,167,69,0.75)',
          borderWidth: 3,
          pointStyle: 'circle',
          pointRadius: 5,
          pointBorderColor: 'transparent',
          pointBackgroundColor: 'rgba(40,167,69,0.75)',
          data: stat_c.values.to_a
        }
      ]
    }
    @options = {}

    # Post distribution
    cop = CountryPost.count
    cip = CityPost.count
    hop = HotelPost.count
    rep = RestaurantPost.count
    pop = TuristicSpotPost.count

    cop_t = CountryPost.where(created_at: Time.zone.now.beginning_of_day..Time.zone.now.end_of_day).count
    cip_t = CityPost.where(created_at: Time.zone.now.beginning_of_day..Time.zone.now.end_of_day).count
    hop_t = HotelPost.where(created_at: Time.zone.now.beginning_of_day..Time.zone.now.end_of_day).count
    rep_t = RestaurantPost.where(created_at: Time.zone.now.beginning_of_day..Time.zone.now.end_of_day).count
    pop_t = TuristicSpotPost.where(created_at: Time.zone.now.beginning_of_day..Time.zone.now.end_of_day).count

    dist_total = {
      'Country' => cop,
      'City' => cip,
      'Hotel' => hop,
      'Restaurant' => rep,
      'Turistic Spot' => pop
    }
    dist_today = {
      'Country' => cop_t,
      'City' => cip_t,
      'Hotel' => hop_t,
      'Restaurant' => rep_t,
      'Turistic Spot' => pop_t
    }

    @data_r = {
      labels: dist_today.keys.to_a,
      datasets: [
        {
          label: 'Total',
          backgroundColor: 'transparent',
          borderColor: 'rgba(220,53,69,0.75)',
          borderWidth: 3,
          pointStyle: 'circle',
          pointRadius: 5,
          pointBorderColor: 'transparent',
          pointBackgroundColor: 'rgba(220,53,69,0.75)',
          data: dist_total.values.to_a
        },
        {
          label: 'Hoy',
          backgroundColor: 'transparent',
          borderColor: 'rgba(40,167,69,0.75)',
          borderWidth: 3,
          pointStyle: 'circle',
          pointRadius: 5,
          pointBorderColor: 'transparent',
          pointBackgroundColor: 'rgba(40,167,69,0.75)',
          data: dist_today.values.to_a
        }
      ]
    }
    @options_r = {
      scales: {
        ticks: {
          beginAtZero: true,
          stepSize: 1
        }
      }
    }
    # Best subs
    begin
      country_q = CountryPost.group(:country_id).count.max
      @best_country = Country.find(country_q[0])
      @best_country_q = country_q[1]
    rescue StandardError
      @best_country = nil
      @best_country_q = 0
    end
    begin
      city_q = CityPost.group(:city_id).count.max
      @best_city = City.find(city_q[0])
      @best_city_q = city_q[1]
    rescue StandardError
      @best_city = nil
      @best_city_q = 0
    end
    begin
      restaurant_q = RestaurantPost.group(:restaurant_id).count.max
      @best_restaurant = Restaurant.find(restaurant_q[0])
      @best_restaurant_q = restaurant_q[1]
    rescue StandardError
      @best_restaurant = nil
      @best_restaurant_q = 0
    end
    begin
      hotel_q = HotelPost.group(:hotel_id).count.max
      @best_hotel = Hotel.find(hotel_q[0])
      @best_hotel_q = hotel_q[1]
    rescue StandardError
      @best_hotel = nil
      @best_hotel_q = 0
    end
    begin
      poi_q = TuristicSpotPost.group(:turistic_spot_id).count.max
      @best_poi = TuristicSpot.find(poi_q[0])
      @best_poi_q = poi_q[1]
    rescue StandardError
      @best_poi = nil
      @best_poi_q = 0
    end
  end

  def users
    @users = User.all
  end

  def ban_user
    user = User.find_by(id: params[:id])
    user.active = 0
    user.save
    redirect_to(admin_users_path)
  end

  def unban_user
    user = User.find_by(id: params[:id])
    user.active = 1
    user.save
    redirect_to(admin_users_path)
  end
end
