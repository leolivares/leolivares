class HotelPost < ApplicationRecord
  belongs_to :hotel, dependent: :destroy
  belongs_to :post, dependent: :destroy
end
