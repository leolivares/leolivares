class RemoveCommentablesFromCommentaries < ActiveRecord::Migration[5.1]
  def change
  	remove_column :commentaries, :commentable_type
  	remove_column :commentaries, :commentable_id
  	remove_column :commentaries, :reputation
  	add_reference :commentaries, :post, index: true
  end
end
