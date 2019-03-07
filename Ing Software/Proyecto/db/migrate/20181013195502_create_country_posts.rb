class CreateCountryPosts < ActiveRecord::Migration[5.1]
  def change
    create_table :country_posts do |t|

      t.timestamps
    end
  end
end
