class Restaurant < ApplicationRecord
  belongs_to :city
  has_many :RestaurantPost, dependent: :destroy
end
