def batch_update(db, batch, field_name, field_value):
    if not batch:
        return

    ids = [i['_id'] for i in batch]
    return db.update_many({
        '_id': {'$in': ids},
    }, {
        '$set': {field_name: field_value}
    })
