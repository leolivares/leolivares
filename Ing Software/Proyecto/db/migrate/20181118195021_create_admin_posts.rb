class CreateAdminPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :admin_posts do |t|
      t.references :admin, foreign_key: true
      t.references :post, foreign_key: true
      t.timestamps
    end
  end
end
