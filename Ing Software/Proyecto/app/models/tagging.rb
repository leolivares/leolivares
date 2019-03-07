class Tagging < ApplicationRecord
  belongs_to :post
  belongs_to :tag

  def self.search(name)
    if name
      @q = "%#{name}%"
      @posts = Tagging.where('tag_id LIKE ?', @q)
    else
      find(:all)
    end
  end
end
