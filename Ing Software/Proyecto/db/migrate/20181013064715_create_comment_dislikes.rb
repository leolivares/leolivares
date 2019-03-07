class CreateCommentDislikes < ActiveRecord::Migration[5.1]
  def change
    create_table :comment_dislikes do |t|
      t.references :commentary, foreign_key: true
      t.references :user, foreign_key: true

      t.timestamps
    end
  end
end
