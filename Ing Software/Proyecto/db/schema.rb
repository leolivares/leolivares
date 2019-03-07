# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20181118204047) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "admin_posts", force: :cascade do |t|
    t.bigint "post_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["post_id"], name: "index_admin_posts_on_post_id"
  end

  create_table "admins", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.inet "current_sign_in_ip"
    t.inet "last_sign_in_ip"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_admins_on_email", unique: true
    t.index ["reset_password_token"], name: "index_admins_on_reset_password_token", unique: true
  end

  create_table "answers", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "user_id"
    t.bigint "responce_id"
    t.index ["responce_id"], name: "index_answers_on_responce_id"
    t.index ["user_id"], name: "index_answers_on_user_id"
  end

  create_table "cities", force: :cascade do |t|
    t.bigint "country_id"
    t.string "name"
    t.text "description"
    t.float "latitude"
    t.float "longitude"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["country_id"], name: "index_cities_on_country_id"
  end

  create_table "city_posts", force: :cascade do |t|
    t.bigint "city_id"
    t.bigint "post_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["city_id"], name: "index_city_posts_on_city_id"
    t.index ["post_id"], name: "index_city_posts_on_post_id"
  end

  create_table "comment_dislikes", force: :cascade do |t|
    t.bigint "commentary_id"
    t.bigint "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["commentary_id"], name: "index_comment_dislikes_on_commentary_id"
    t.index ["user_id"], name: "index_comment_dislikes_on_user_id"
  end

  create_table "comment_likes", force: :cascade do |t|
    t.bigint "commentary_id"
    t.bigint "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["commentary_id"], name: "index_comment_likes_on_commentary_id"
    t.index ["user_id"], name: "index_comment_likes_on_user_id"
  end

  create_table "commentaries", force: :cascade do |t|
    t.bigint "user_id"
    t.text "content"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.index ["post_id"], name: "index_commentaries_on_post_id"
    t.index ["user_id"], name: "index_commentaries_on_user_id"
  end

  create_table "countries", force: :cascade do |t|
    t.string "name"
    t.text "description"
    t.integer "subscribers"
    t.float "latitude"
    t.float "longitude"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "country_posts", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.bigint "country_id"
    t.index ["country_id"], name: "index_country_posts_on_country_id"
    t.index ["post_id"], name: "index_country_posts_on_post_id"
  end

  create_table "dislikes", force: :cascade do |t|
    t.bigint "user_id"
    t.bigint "post_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["post_id"], name: "index_dislikes_on_post_id"
    t.index ["user_id"], name: "index_dislikes_on_user_id"
  end

  create_table "favorite_posts", force: :cascade do |t|
    t.bigint "post_id"
    t.bigint "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["post_id"], name: "index_favorite_posts_on_post_id"
    t.index ["user_id"], name: "index_favorite_posts_on_user_id"
  end

  create_table "favorite_spots", force: :cascade do |t|
    t.bigint "turistic_spot_id"
    t.bigint "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["turistic_spot_id"], name: "index_favorite_spots_on_turistic_spot_id"
    t.index ["user_id"], name: "index_favorite_spots_on_user_id"
  end

  create_table "followers", force: :cascade do |t|
    t.bigint "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "follower_id"
    t.index ["user_id"], name: "index_followers_on_user_id"
  end

  create_table "hotel_posts", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.bigint "hotel_id"
    t.index ["hotel_id"], name: "index_hotel_posts_on_hotel_id"
    t.index ["post_id"], name: "index_hotel_posts_on_post_id"
  end

  create_table "hotels", force: :cascade do |t|
    t.text "nombre"
    t.float "reputation", default: 0.0
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "city_id"
    t.index ["city_id"], name: "index_hotels_on_city_id"
  end

  create_table "likes", force: :cascade do |t|
    t.bigint "user_id"
    t.bigint "post_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["post_id"], name: "index_likes_on_post_id"
    t.index ["user_id"], name: "index_likes_on_user_id"
  end

  create_table "moderators", force: :cascade do |t|
    t.bigint "user_id"
    t.bigint "country_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["country_id"], name: "index_moderators_on_country_id"
    t.index ["user_id"], name: "index_moderators_on_user_id"
  end

  create_table "modify_followers", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "post_surveys", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.bigint "survey_id"
    t.index ["post_id"], name: "index_post_surveys_on_post_id"
    t.index ["survey_id"], name: "index_post_surveys_on_survey_id"
  end

  create_table "posts", force: :cascade do |t|
    t.bigint "user_id"
    t.text "content"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "image"
    t.text "title"
    t.integer "type_post", default: 0
    t.float "reputation", default: 0.0
    t.integer "upvote", default: 0
    t.integer "downvote", default: 0
    t.text "body"
    t.text "info"
    t.index ["user_id"], name: "index_posts_on_user_id"
  end

  create_table "posts_tags", id: false, force: :cascade do |t|
    t.bigint "post_id"
    t.bigint "tag_id"
    t.index ["post_id"], name: "index_posts_tags_on_post_id"
    t.index ["tag_id"], name: "index_posts_tags_on_tag_id"
  end

  create_table "questions", force: :cascade do |t|
    t.string "title"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "survey_id"
    t.index ["survey_id"], name: "index_questions_on_survey_id"
  end

  create_table "requests", force: :cascade do |t|
    t.bigint "user_id"
    t.bigint "country_id"
    t.string "state"
    t.string "reason"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["country_id"], name: "index_requests_on_country_id"
    t.index ["user_id"], name: "index_requests_on_user_id"
  end

  create_table "responces", force: :cascade do |t|
    t.string "option"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "question_id"
    t.index ["question_id"], name: "index_responces_on_question_id"
  end

  create_table "restaurant_posts", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.bigint "restaurant_id"
    t.index ["post_id"], name: "index_restaurant_posts_on_post_id"
    t.index ["restaurant_id"], name: "index_restaurant_posts_on_restaurant_id"
  end

  create_table "restaurants", force: :cascade do |t|
    t.text "nombre"
    t.float "reputation", default: 0.0
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "city_id"
    t.index ["city_id"], name: "index_restaurants_on_city_id"
  end

  create_table "subscriptions", force: :cascade do |t|
    t.bigint "follower_id"
    t.bigint "followed_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["followed_id"], name: "index_subscriptions_on_followed_id"
    t.index ["follower_id"], name: "index_subscriptions_on_follower_id"
  end

  create_table "surveys", force: :cascade do |t|
    t.string "title"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "user_id"
    t.bigint "post_id"
    t.index ["post_id"], name: "index_surveys_on_post_id"
    t.index ["user_id"], name: "index_surveys_on_user_id"
  end

  create_table "taggings", force: :cascade do |t|
    t.bigint "post_id"
    t.bigint "tag_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["post_id"], name: "index_taggings_on_post_id"
    t.index ["tag_id"], name: "index_taggings_on_tag_id"
  end

  create_table "tags", force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "turistic_spot_posts", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "post_id"
    t.bigint "turistic_spot_id"
    t.index ["post_id"], name: "index_turistic_spot_posts_on_post_id"
    t.index ["turistic_spot_id"], name: "index_turistic_spot_posts_on_turistic_spot_id"
  end

  create_table "turistic_spots", force: :cascade do |t|
    t.text "nombre"
    t.float "reputation", default: 0.0
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "city_id"
    t.index ["city_id"], name: "index_turistic_spots_on_city_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "name", null: false
    t.integer "reputation", default: 0, null: false
    t.string "avatar"
    t.string "type"
    t.string "category"
    t.bigint "country_id"
    t.integer "active", default: 1
    t.string "provider"
    t.string "uid"
    t.index ["country_id"], name: "index_users_on_country_id"
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "admin_posts", "posts"
  add_foreign_key "answers", "responces"
  add_foreign_key "answers", "users"
  add_foreign_key "cities", "countries"
  add_foreign_key "city_posts", "cities"
  add_foreign_key "city_posts", "posts"
  add_foreign_key "comment_dislikes", "commentaries"
  add_foreign_key "comment_dislikes", "users"
  add_foreign_key "comment_likes", "commentaries"
  add_foreign_key "comment_likes", "users"
  add_foreign_key "commentaries", "users"
  add_foreign_key "country_posts", "countries"
  add_foreign_key "country_posts", "posts", on_delete: :cascade
  add_foreign_key "dislikes", "posts"
  add_foreign_key "dislikes", "users"
  add_foreign_key "favorite_posts", "posts"
  add_foreign_key "favorite_posts", "users"
  add_foreign_key "favorite_spots", "turistic_spots"
  add_foreign_key "favorite_spots", "users"
  add_foreign_key "followers", "users"
  add_foreign_key "hotel_posts", "hotels"
  add_foreign_key "hotel_posts", "posts"
  add_foreign_key "hotels", "cities"
  add_foreign_key "likes", "posts"
  add_foreign_key "likes", "users"
  add_foreign_key "moderators", "countries"
  add_foreign_key "moderators", "users"
  add_foreign_key "post_surveys", "posts"
  add_foreign_key "post_surveys", "surveys"
  add_foreign_key "posts", "users"
  add_foreign_key "posts_tags", "posts"
  add_foreign_key "posts_tags", "tags"
  add_foreign_key "questions", "surveys"
  add_foreign_key "requests", "countries"
  add_foreign_key "requests", "users"
  add_foreign_key "responces", "questions"
  add_foreign_key "restaurant_posts", "posts"
  add_foreign_key "restaurant_posts", "restaurants"
  add_foreign_key "restaurants", "cities"
  add_foreign_key "subscriptions", "users", column: "followed_id"
  add_foreign_key "subscriptions", "users", column: "follower_id"
  add_foreign_key "surveys", "posts"
  add_foreign_key "surveys", "users"
  add_foreign_key "taggings", "posts"
  add_foreign_key "taggings", "tags"
  add_foreign_key "turistic_spot_posts", "posts"
  add_foreign_key "turistic_spot_posts", "turistic_spots"
  add_foreign_key "turistic_spots", "cities"
  add_foreign_key "users", "countries"
end
