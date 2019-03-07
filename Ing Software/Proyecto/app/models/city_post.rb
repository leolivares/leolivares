class CityPost < ApplicationRecord
  belongs_to :city
  belongs_to :post
end
