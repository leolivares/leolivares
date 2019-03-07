class Answer < ApplicationRecord
  belongs_to :user
  belongs_to :responce

  validates :responce_id, uniqueness: { scope: :user_id,
                                        message: 'User has already logged an answer to this question' }
end
