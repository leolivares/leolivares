class Hotel < ApplicationRecord
  belongs_to :city
  has_many :hotel_posts, dependent: :destroy
end
