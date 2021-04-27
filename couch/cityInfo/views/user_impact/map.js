function (doc) {
	if (doc.text == null) {
		  emit([doc.user.id, doc._id],
		{followers: doc.user.followers_count,
		  textlength: doc.full_text.split(" ").length});
	} else {
		 emit([doc.user.id, doc._id],
		{followers: doc.user.followers_count,
		  textlength: doc.text.split(" ").length});
	}
}

