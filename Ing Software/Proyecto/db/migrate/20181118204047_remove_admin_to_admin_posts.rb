class RemoveAdminToAdminPosts < ActiveRecord::Migration[5.1]
  def change
  	remove_column :admin_posts, :admin_id
  end
end
