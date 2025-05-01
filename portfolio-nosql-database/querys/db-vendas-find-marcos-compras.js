// db-vendas-find-marcos-compras.js
db.vendas.find({ "nome": "Marcos" }, { "compras": 1, "_id": 0 }).pretty()
