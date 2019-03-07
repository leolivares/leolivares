json.extract! restaurant, :id, :city_id, :nombre, :reputation, :created_at, :updated_at
json.url restaurant_url(restaurant, format: :json)
