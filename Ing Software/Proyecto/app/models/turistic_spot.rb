class TuristicSpot < ApplicationRecord
  belongs_to :city
  has_many :favorite_posts, dependent: :destroy
  has_many :TuristicSpotPosts, dependent: :destroy
end
