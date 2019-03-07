class CommentDislike < ApplicationRecord
  belongs_to :commentary
  belongs_to :user
end
