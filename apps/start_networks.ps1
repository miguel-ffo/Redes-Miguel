echo "rede jadilson"
docker network create --subnet=10.10.10.0/26 jadilson_api_network

echo "proxy"
docker network create --subnet=10.10.10.64/27 proxy_network

echo "api cliente"
docker network create --subnet=10.10.10.96/27 cliente_api_network

echo "api inventario"
docker network create --subnet=10.10.10.128/27 inventario_api_network

echo "api relatorio"
docker network create --subnet=10.10.10.160/27 relatorio_api_network

echo "bancos de dados"
docker network create --subnet=10.10.10.192/29 db_cliente_network
docker network create --subnet=10.10.10.200/29 db_inventario_network
docker network create --subnet=10.10.10.208/29 db_relatorio_network

echo "backup"
docker network create --subnet=10.10.10.216/29 cliente_backup_network
docker network create --subnet=10.10.10.224/29 inventario_backup_network
docker network create --subnet=10.10.10.232/29 relatorio_backup_network