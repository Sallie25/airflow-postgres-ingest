# Airflow PostgreSQL Ingest

A production-ready, containerized data ingestion pipeline that orchestrates NYC taxi data loading into PostgreSQL using Apache Airflow. This project demonstrates best practices for building scalable, reproducible data pipelines with Docker and Airflow.

## Overview

This project provides a complete data pipeline solution that:
- **Orchestrates** data workflows using Apache Airflow
- **Containerizes** ingestion logic for reproducibility and scalability
- **Manages** PostgreSQL databases with pgAdmin UI
- **Automates** scheduled ingestion of NYC taxi datasets
- **Separates** concerns between orchestration, execution, and storage

Perfect for data engineers building ETL/ELT pipelines, learning Airflow orchestration, or establishing data infrastructure.

---

## Architecture

The system follows a **microservices architecture** where each component has a distinct responsibility:

```
┌──────────────────────────────────┐
│   Airflow Scheduler (Orchestration) │
│   ├─ Schedules DAGs              │
│   └─ Triggers tasks              │
└────────────────┬──────────────────┘
                 │ triggers
                 ▼
        ┌────────────────┐
        │ Ingest Container│
        │ (Docker)       │
        └────────────┬───┘
                     │ writes
                     ▼
        ┌────────────────────┐
        │ PostgreSQL Database │
        │ (ny_taxi)          │
        └────────────────────┘
                     ▲
                     │ manages
                     │
        ┌────────────────────┐
        │   pgAdmin UI       │
        │ (Database Manager) │
        └────────────────────┘
```

### Key Components

| Component | Purpose | Port |
|-----------|---------|------|
| **PostgreSQL (pgdatabase)** | Primary data warehouse for taxi datasets | 5432 |
| **pgAdmin** | Web-based PostgreSQL management interface | 8085 |
| **Airflow Metadata DB** | Stores DAG execution history and state | Internal |
| **Airflow Scheduler** | Executes scheduled DAGs and tasks | Internal |
| **Airflow Webserver** | UI for monitoring, triggering, and managing workflows | 8080 |
| **Ingestion Container** | Custom Docker image running the Python ingestion script | On-demand |

---

## Project Structure

```
airflow-postgres-ingest/
│
├── 01_simple_postgres_pipeline.py    # Core ingestion script
├── Dockerfile                         # Build image for ingestion container
├── docker-compose.yaml                # Full stack orchestration
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
├── LICENSE                            # MIT License
├── README.md                          # This file
│
└── dags/
    └── taxi_ingestion_dag.py         # Airflow DAG definition
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- At least 2GB free RAM
- ~5GB free disk space (for taxi data and PostgreSQL)

### 1. Clone the Repository

```bash
git clone https://github.com/Sallie25/airflow-postgres-ingest.git
cd airflow-postgres-ingest
```

### 2. Build the Ingestion Container

```bash
docker build -t taxi-ingest:latest .
```

### 3. Start All Services

```bash
docker compose up -d
```

This starts:
- PostgreSQL database
- pgAdmin interface
- Airflow metadata database
- Airflow scheduler and webserver

### 4. Initialize Airflow (if first time)

```bash
docker compose exec airflow-webserver airflow db init
```

---

## Accessing Services

### Airflow UI
- **URL**: http://localhost:8080
- **Username**: admin
- **Password**: admin

From here you can:
- View DAG definitions
- Trigger pipeline runs manually
- Monitor execution logs
- Set up schedules

### pgAdmin
- **URL**: http://localhost:8085
- **Email**: admin@admin.com
- **Password**: root

#### Connect to PostgreSQL Database:
1. Right-click "Servers" → "Register" → "Server"
2. **General Tab**:
   - Name: `ny_taxi`
3. **Connection Tab**:
   - Host: `pgdatabase`
   - Username: `root`
   - Password: `root`
   - Database: `ny_taxi`
4. Click "Save"

---

## CLI Parameters

The ingestion script accepts the following parameters:

```bash
--year              Year for taxi data (default: 2021)
--month             Month for taxi data (default: 1)
--pg_user           PostgreSQL username (default: root)
--pg_pass           PostgreSQL password (default: root)
--pg_host           PostgreSQL host (default: localhost)
--pg_port           PostgreSQL port (default: 5432)
--pg_db             PostgreSQL database name (default: ny_taxi)
--target_table      Target table for taxi data (default: yellow_taxi_data)
--zone_table        Taxi zone lookup table (default: taxi_zone_lookup)
--chunksize         CSV chunk size (default: 100000)
```

---

## Running the Ingestion Pipeline

### Option 1: Manual Execution via Docker

```bash
docker run --network airflow-postgres-ingest_default \
  taxi-ingest:latest \
  --pg_user=root \
  --pg_pass=root \
  --pg_host=pgdatabase \
  --pg_port=5432 \
  --pg_db=ny_taxi \
  --year=2021 \
  --month=1
```

### Option 2: Via Airflow DAG (Recommended)

The DAG is already set up in `dags/taxi_ingestion_dag.py`. To use it:

1. Enable the DAG in Airflow UI
2. Trigger manually or wait for scheduled execution (monthly)

---

## Troubleshooting

### Issue: Docker network not found

```bash
docker compose down
docker compose up -d
```

### Issue: Airflow shows "No DAGs"

Ensure `dags/` folder exists and DAG files are in the correct location:
```bash
mkdir -p dags
```

### Issue: PostgreSQL connection refused

Check if PostgreSQL is running:
```bash
docker compose ps
```

If not running:
```bash
docker compose restart pgdatabase
```

### Issue: Airflow webserver won't start

Check logs:
```bash
docker compose logs airflow-webserver
```

---

## Best Practices Implemented

✅ **Containerization**: All components run in isolated Docker containers
✅ **Infrastructure as Code**: docker-compose.yaml defines entire stack
✅ **Parameterization**: CLI arguments enable flexible configuration
✅ **Chunked Processing**: Efficient memory management for large datasets
✅ **Progress Tracking**: tqdm provides real-time ingestion progress
✅ **Type Safety**: Explicit dtype definitions prevent type coercion issues
✅ **Separation of Concerns**: Orchestration (Airflow) separate from execution (container)
✅ **Reproducibility**: Identical setup across different environments

---

## Future Enhancements

- [ ] Support for multiple data sources (green, for-hire vehicles)
- [ ] Data validation and quality checks
- [ ] Error handling and retry logic in DAG
- [ ] Notifications on failure/success
- [ ] Data transformation and aggregation tasks
- [ ] Integration with data warehouse (BigQuery, Snowflake)
- [ ] Monitoring and alerting
- [ ] Automated backups
- [ ] CI/CD pipeline for image builds

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Support

For issues, questions, or suggestions, please open a GitHub issue in this repository.

---

## Acknowledgments

- Built with [Apache Airflow](https://airflow.apache.org/)
- Data sourced from [DataTalksClub](https://github.com/DataTalksClub)
- Inspired by modern data engineering practices

---

**Last Updated**: June 2026
