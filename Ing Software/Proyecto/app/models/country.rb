class Country < ApplicationRecord
  has_many :posts, dependent: :destroy
  has_many :cities, dependent: :destroy
  has_many :country_posts, dependent: :destroy
end
