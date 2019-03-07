class CreateCommentaries < ActiveRecord::Migration[5.1]
  def change
    create_table :commentaries do |t|
      t.references :user,  foreign_key: true
      t.text :content
      t.float :reputation
      t.references :commentable, polymorphic: true
      t.timestamps
    end
  end
end
