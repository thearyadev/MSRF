migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "cmkw7ebk",
    "name": "username",
    "type": "text",
    "required": true,
    "unique": true,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wu9pgrbe",
    "name": "lastExec",
    "type": "date",
    "required": true,
    "unique": false,
    "options": {
      "min": "",
      "max": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "cmkw7ebk",
    "name": "email",
    "type": "text",
    "required": true,
    "unique": true,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wu9pgrbe",
    "name": "lastExec",
    "type": "date",
    "required": false,
    "unique": false,
    "options": {
      "min": "",
      "max": ""
    }
  }))

  return dao.saveCollection(collection)
})
