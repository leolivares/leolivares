var cursor = db.usuarios.find({}, {});
cursor.forEach(
  (element) => {
    try {
      var msj_cursor = db.mensajes.find({"uid": element["uid"]}, {})
      var likes = 0;
      msj_cursor.forEach(
        (msj_element) => {
          likes += msj_element["likes"];
        }
      )
      print("User ID: " + element["uid"] +
            " - Name: " + element["name"] +
            " - Likes: " + likes);
    }
    catch(e) {
      print("GG", e);
    }
  }
);
