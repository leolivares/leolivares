class CountryPost < ApplicationRecord
  belongs_to :country, dependent: :destroy
  belongs_to :post, dependent: :destroy
end
