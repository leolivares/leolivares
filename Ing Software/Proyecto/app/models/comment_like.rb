class CommentLike < ApplicationRecord
  belongs_to :commentary
  belongs_to :user
end
