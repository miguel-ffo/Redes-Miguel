

echo "Iniciando bancos de dados"
cd banco_cliente
docker-compose -f docker-compose-cliente-db.yml up -d
cd ..
cd banco_relatorio
docker-compose -f docker-compose-relatorio-db.yml up -d
cd ..
cd banco-inventario
docker-compose -f docker-compose-inventario-db.yml up -d
cd ..

echo "Iniciando APIs"
cd inventario_project
docker-compose -f docker-compose-inventario.yml up -d
cd ..
cd relatorio_project
docker-compose -f docker-compose-relatorio.yml up -d
cd ..
cd cliente_project
docker-compose -f docker-compose-cliente.yml up -d
cd ..

echo "Iniciando Proxy"
cd proxy
docker-compose -f docker-compose-proxy.yml up -d
cd ..

echo "Iniciando Jadilson"
cd  jadilsonpaiva
docker-compose -f docker-compose-jadilson.yml up -d
cd ..