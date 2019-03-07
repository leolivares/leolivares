class Survey < ApplicationRecord
  belongs_to :user
  belongs_to :post
  has_many :questions, dependent: :destroy

  accepts_nested_attributes_for :questions, reject_if: :all_blank
end
