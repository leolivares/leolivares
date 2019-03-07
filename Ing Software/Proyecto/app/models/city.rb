class City < ApplicationRecord
  belongs_to :country
  has_many :posts, dependent: :destroy
  has_many :hotels, dependent: :destroy
  has_many :turistic_spots, dependent: :destroy
  has_many :restaurants, dependent: :destroy
end
