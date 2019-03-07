class FavoriteSpot < ApplicationRecord
  belongs_to :user
  belongs_to :turistic_spot
end
