from kafka.admin import KafkaAdminClient, NewTopic

# Conéctate al broker de Kafka
admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        client_id='mi_admin_client',
        api_version=(2, 8, 1)
)

for i in range(1, 2):
# Definir un nuevo topic con particiones
    topic = NewTopic(
        name=f"vehiculos_datos{i}",
        num_partitions=5,  # Número de particiones
        replication_factor=1  # Factor de replicación
    )

    # Crear el topic en el clúster
    admin_client.create_topics(new_topics=[topic], validate_only=False)

    print(f"Topic 'vehiculos_datos{i}' creado con particiones.")
    