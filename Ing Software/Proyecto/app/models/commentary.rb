class Commentary < ApplicationRecord
  belongs_to :post
  belongs_to :user
  has_many :comment_likes, dependent: :destroy
  has_many :comment_dislikes, dependent: :destroy
  validates :content, length: { minimum: 1, maximum: 50 }

  def self.create_count
    kliks = Commentary.group('DATE(created_at)').count
  end
end
