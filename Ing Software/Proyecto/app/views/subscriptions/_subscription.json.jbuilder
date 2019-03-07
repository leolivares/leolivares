json.extract! subscription, :id, :follower_Id, :followed_Id, :created_at, :updated_at
json.url subscription_url(subscription, format: :json)
