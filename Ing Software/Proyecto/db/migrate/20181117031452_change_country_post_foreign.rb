class ChangeCountryPostForeign < ActiveRecord::Migration[5.1]
  def change
  	remove_foreign_key :country_posts, :posts

  	add_foreign_key :country_posts, :posts, on_delete: :cascade
  end
end
