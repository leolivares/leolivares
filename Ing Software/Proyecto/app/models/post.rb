class Post < ApplicationRecord
  mount_uploader :image, ImageUploader
  belongs_to :user
  has_many :surveys, dependent: :destroy
  has_many :favorite_posts, dependent: :destroy
  has_many :likes, dependent: :destroy
  has_many :dislikes, dependent: :destroy

  # has_many :commentaries, as: :commentable, dependent: :destroy, inverse_of: :commentable
  has_many :commentaries, dependent: :destroy
  has_many :taggings, dependent: :destroy
  has_many :tags, through: :taggings

  validates :title, length: { minimum: 2, maximum: 50 }
  validates :content, length: { maximum: 200 }
  accepts_nested_attributes_for :surveys

  def update_content(content)
    update(content: content)
  end

  def self.search(search)
    if search
      @q = "%#{search}%"
      @posts = Post.where('title LIKE ? or content LIKE ?', @q, @q)
    else
      find(:all)
    end
  end

  def self.search_tag(search)
    if search
      @q = "%#{search}%"
      @posts = Post.all_tags.split(',').include? search
    else
      find(:all)
    end
  end

  def all_tags=(names)
    self.tags = names.split(',').map do |name|
      Tag.where(name: name).first_or_create!
    end
  end

  def all_tags
    tags.map(&:name).join(', ')
  end

  def self.tagged_with(name)
    Tag.find_by!(name: name).posts
  end

  def self.create_count
    kliks = Post.group('DATE(created_at)').count
  end
end
