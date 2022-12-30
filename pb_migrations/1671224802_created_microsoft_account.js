migrate((db) => {
  const collection = new Collection({
    "id": "tgdhdtyn6cccf80",
    "created": "2022-12-16 21:06:42.032Z",
    "updated": "2022-12-16 21:06:42.032Z",
    "name": "microsoft_account",
    "type": "base",
    "system": false,
    "schema": [
      {
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
      },
      {
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
      },
      {
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
      }
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": "",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("tgdhdtyn6cccf80");

  return dao.deleteCollection(collection);
})
