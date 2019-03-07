class User < ApplicationRecord
  mount_uploader :avatar, AvatarUploader
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable
  has_many :posts, dependent: :destroy
  has_many :surveys, dependent: :destroy
  has_many :likes, dependent: :destroy
  has_many :dislikes, dependent: :destroy
  has_many :favorite_posts, dependent: :destroy
  has_many :favorite_spots, dependent: :destroy
  has_many :commentaries, dependent: :destroy
  has_many :followed, class_name: 'Subscription', foreign_key: 'followed_id',
                      dependent: :destroy, inverse_of: :commentable
  has_many :follower, class_name: 'Subscription', foreign_key: 'follower_id',
                      dependent: :destroy, inverse_of: :commentable
  has_many :comment_likes, dependent: :destroy
  has_many :comment_dislikes, dependent: :destroy
  has_many :followers, dependent: :destroy
end
