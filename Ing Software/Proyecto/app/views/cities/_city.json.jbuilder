json.extract! city, :id, :country_id, :name, :description, :latitude, :longitude, :created_at, :updated_at
json.url city_url(city, format: :json)
