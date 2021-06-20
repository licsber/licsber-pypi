def get_latest_doc(db, custom_filter, projection):
    return list(db.find(
        custom_filter
        , projection=projection
    ).sort([
        ('_id', -1)
    ]).limit(1))
