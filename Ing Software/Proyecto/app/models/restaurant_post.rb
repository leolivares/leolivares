class RestaurantPost < ApplicationRecord
  belongs_to :restaurant, dependent: :destroy
  belongs_to :post, dependent: :destroy
end
