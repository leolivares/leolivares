json.extract! hotel, :id, :city_id, :nombre, :reputation, :created_at, :updated_at
json.url hotel_url(hotel, format: :json)
