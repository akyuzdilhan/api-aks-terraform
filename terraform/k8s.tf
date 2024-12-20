provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
}

resource "kubernetes_namespace" "app_namespace" {
  metadata {
    name = "automate-app"
  }

  depends_on = [azurerm_kubernetes_cluster.aks]
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "automate-app"
    namespace = kubernetes_namespace.app_namespace.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "automate-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "automate-app"
        }
      }

      spec {
        image_pull_secrets {
          name = "acr-secret"
        }

        container {
          name  = "automate-app"
          image = "${azurerm_container_registry.acr.login_server}/automate-api:latest"

          port {
            container_port = 8000
          }
        }
      }
    }
  }

  depends_on = [azurerm_kubernetes_cluster.aks]
}

resource "kubernetes_service" "app_service" {
  metadata {
    name      = "automate-app-service"
    namespace = kubernetes_namespace.app_namespace.metadata[0].name
  }

  spec {
    selector = {
      app = "automate-app"
    }

    type = "LoadBalancer"

    port {
      port        = 8000
      target_port = 8000
    }
  }

  depends_on = [azurerm_kubernetes_cluster.aks]
}