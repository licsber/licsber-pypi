def get_latest_doc(db, custom_filter, projection):
    doc = list(db.find(
        custom_filter
        , projection=projection
    ).sort([
        ('_id', -1)
    ]).limit(1))

    if doc:
        return doc[0]
