module PostsHelper
  def render_tags(tags)
    tags.gsub(/\w+/) { |word| link_to word, "/posts/tag/#{word}" }.html_safe
  end
end
