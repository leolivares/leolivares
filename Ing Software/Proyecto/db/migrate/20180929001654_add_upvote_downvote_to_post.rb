class AddUpvoteDownvoteToPost < ActiveRecord::Migration[5.1]
  def change
    add_column :posts, :upvote, :integer, default: 0
    add_column :posts, :downvote, :integer, default: 0
  end
end
