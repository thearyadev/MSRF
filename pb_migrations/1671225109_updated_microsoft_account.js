migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "qzfrfi8w",
    "name": "password",
    "type": "text",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // remove
  collection.schema.removeField("qzfrfi8w")

  return dao.saveCollection(collection)
})
