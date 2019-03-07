class TuristicSpotPost < ApplicationRecord
  belongs_to :turistic_spot, dependent: :destroy
  belongs_to :post, dependent: :destroy
end
