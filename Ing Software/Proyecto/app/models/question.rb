class Question < ApplicationRecord
  belongs_to :survey, optional: true
  has_many :responces, dependent: :destroy

  accepts_nested_attributes_for :responces, reject_if: :all_blank
end
