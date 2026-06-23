# Kubernetes Assignment

## Repository Information

### Source Code Repository

Repository URL: https://github.com/srikanth104/hone-k8s-assignment

### Docker Hub Image

Docker Image URL: https://hub.docker.com/repository/docker/srikanth104/home-api

### Service API URL

Health Endpoint:
http://8.232.109.0/health

Employees Endpoint:
http://8.232.109.0/employees


---

# Requirement Understanding

The objective of this assignment is to design, containerize, and deploy a multi-tier application on Kubernetes consisting of:

1. Service API Tier
   * Exposes REST API endpoints.
   * Retrieves employee data from the database.
   * Supports rolling updates.
   * Supports self-healing.
   * Supports Horizontal Pod Autoscaling (HPA).
   * Is externally accessible using Kubernetes Ingress.
2. Database Tier
   * Stores employee records.
   * Supports persistent storage.
   * Is accessible only within the cluster.
   * Recovers automatically after pod recreation.

---

# Assumptions

* Google Kubernetes Engine (GKE Autopilot) is used as the Kubernetes platform.
* MySQL 8.0 is used as the database.
* Flask is used for the API implementation.
* Docker Hub is used as the container image registry.
* The application is intended for demonstration purposes and uses sample employee data.
* External access is provided through Kubernetes Ingress.

---

# Solution Overview

## Architecture

Internet
↓
Ingress
↓
home-api-service (ClusterIP)
↓
home-api Deployment (4 Replicas)
↓
mysql-service (ClusterIP)
↓
MySQL StatefulSet
↓
Persistent Volume Claim

### Components

#### API Tier

* Technology: Python Flask
* Replicas: 4
* Deployment Type: Deployment
* Rolling Update Strategy Enabled
* Health Checks:

  * Liveness Probe
  * Readiness Probe
* Horizontal Pod Autoscaler Configured

Endpoints:

GET /health

Returns application health status.

GET /employees

Returns employee records from MySQL database.

#### Database Tier

* Technology: MySQL 8.0
* Deployment Type: StatefulSet
* Replicas: 1
* Storage: Persistent Volume Claim (PVC)
* Internal Access Only

Database contains an employees table with sample records.

---

# Kubernetes Objects Used

## Namespace

* home

## ConfigMaps

* mysql-config
* mysql-init-script

## Secrets

* mysql-secret

## Deployments

* home-api

## StatefulSets

* mysql

## Services

* home-api-service
* mysql-service

## Ingress

* home-api-ingress

## Persistent Volume Claims

* mysql-pvc

## Horizontal Pod Autoscaler

* home-api-hpa

---

# Configuration Management

## ConfigMap Usage

Database connection details are externalized using Kubernetes ConfigMaps.

Configured Values:

* DB_HOST
* DB_PORT
* DB_NAME

This allows configuration changes without modifying application code.

## Secret Usage

Sensitive credentials are stored in Kubernetes Secrets.

Stored Values:

* DB_USER
* DB_PASSWORD

Passwords are never hardcoded in application code or deployment manifests.

---

# Persistence

Database persistence is achieved using a Persistent Volume Claim.

---

# Self-Healing Demonstration

## API Tier

Deleting an API pod:

kubectl delete pod <api-pod-name> -n home

Result:

* Kubernetes automatically recreates the pod.
* Application remains available.

## Database Tier

Deleting MySQL pod:

kubectl delete pod mysql-0 -n home

Result:

* StatefulSet recreates the pod.
* Existing employee data remains available due to persistent storage.

---

# Rolling Update Strategy

The API Deployment uses Kubernetes RollingUpdate strategy.

Configuration:

* maxUnavailable: 1
* maxSurge: 1

Benefits:

* Zero downtime deployments.
* Controlled rollout of application updates.
* Continuous application availability.

---

# Horizontal Pod Autoscaler (HPA)

Configured using CPU utilization metrics.

Configuration:

* Min Replicas: 4
* Max Replicas: 10
* Target CPU Utilization: 70%

Benefits:

* Automatic scaling during increased load.
* Cost optimization during low traffic periods.

---

# FinOps Considerations

## Resource Requests and Limits

API pods are configured with resource requests and limits.

Requests:

* CPU: 100m
* Memory: 128Mi

Limits:

* CPU: 500m
* Memory: 512Mi

These values ensure predictable resource allocation while preventing resource exhaustion.

## Cost Optimization Opportunities

### 1. Right-Sizing Resources

Resource requests and limits can be continuously adjusted based on observed CPU and memory utilization metrics.

### 2. Horizontal Pod Autoscaling

HPA automatically scales the API tier based on workload demand, preventing overprovisioning.

### 3. Internal Database Access

The MySQL database is exposed using a ClusterIP service instead of a public LoadBalancer, reducing infrastructure costs and improving security.

---

# Justification for Resources Utilized

## API Tier

The Flask application is lightweight and performs simple database read operations.

Selected Resources:

* CPU Request: 100m
* Memory Request: 128Mi

These values provide sufficient resources while minimizing infrastructure cost.

## Database Tier

MySQL requires higher memory allocation for reliable operation.

Selected Resources:

* Persistent Storage: 5Gi
* Single Replica StatefulSet

This configuration satisfies persistence requirements while maintaining simplicity and cost efficiency.

---

# Demonstration Checklist

The recorded demonstration includes:

* All Kubernetes resources deployed and running.
* API call retrieving employee records.
* API pod deletion and automatic regeneration.
* Database pod deletion and automatic regeneration.
* Data persistence verification.
* Rolling update strategy demonstration.
* Horizontal Pod Autoscaler configuration.
* FinOps considerations and resource optimization discussion.

---

# Conclusion

The solution successfully implements a production-style Kubernetes deployment using:

* Flask API Microservice
* MySQL Database
* StatefulSet
* Deployment
* ConfigMaps
* Secrets
* Persistent Storage
* Ingress
* Horizontal Pod Autoscaler
* Rolling Updates
* Self-Healing Capabilities