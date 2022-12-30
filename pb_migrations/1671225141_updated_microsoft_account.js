migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ypgrd7jw",
    "name": "points",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ypgrd7jw",
    "name": "points",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
})
