json.extract! request, :id, :user_id, :country_id, :state, :reason, :created_at, :updated_at
json.url request_url(request, format: :json)
